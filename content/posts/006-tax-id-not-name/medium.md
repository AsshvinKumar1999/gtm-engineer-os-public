# Post 006, Medium version

**Title:** Auditing a Name-Based Join: Tax IDs, Collisions and the Coverage Ceiling
**Subtitle:** Measuring how much a normalized-name join would have cost against a
50,307-employer H-1B index, and publishing the date the data stops.
**Canonical URL:** the Substack version is the original. Link it.
**Tags:** #dataengineering #entityresolution #datascience #python #audit
**Slot:** Wednesday teardown, technical version. Same facts, mechanism-first.
**Status:** drafted and gated. Needs Asshvin's approval before publishing.

---

## Entity resolution is a load-bearing decision

Every data pipeline that joins two datasets makes one decision that determines the
quality of everything downstream: what is the key.

When both sides describe the same real-world entity, the key has to identify that entity
exactly. Two candidate keys are usually available, and they are not equally good:

- a **name**, which is a label a human or a registry chose, and which is not unique
- an **identifier**, which a registry issued, and which is unique by construction

This post is a measurement of what that difference was worth, on a real pipeline, over a
real index. Not a demonstration on synthetic data.

## The pipeline under audit

The pipeline joins two free public sources:

- **SEC Form D filings**: companies that recently raised money, with a filing date and
  amount.
- **DOL H-1B wage filings (LCAs)**: employers that filed a certified wage application to
  sponsor a worker, with the job title, the wage and the worksite state.

The join key is the employer's tax ID. The SEC filing's SGML header carries the filer's
EIN; the DOL disclosure row carries the employer's FEIN. Both are the nine-digit tax ID of
the same legal entity.

The fallback key is a normalized employer name:

```python
SUFFIX_RE = re.compile(r"\b(inc|incorporated|llc|l\.l\.c|corp|corporation|co|company|ltd|limited|pbc|lp|llp)\b\.?", re.I)

def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", SUFFIX_RE.sub("", (s or "").lower()))
```

Every output row records which route produced it (`match`: `EIN` or `name-only`), so the
join's provenance is inspectable per row rather than assumed globally.

## The index

The DOL publishes a quarter of LCAs at a time as a free spreadsheet. This audit used
FY2026 Q3.

| Measure | Value |
|---|---|
| Rows read from the disclosure file | 437,496 |
| Certified H-1B applications kept | 392,175 |
| Employers in the index | 50,307 |
| Keys by tax ID | 50,307 |
| Keys by employer name | 51,137 |
| Extra name keys above one per employer | 830 |
| Employers reachable through more than one name | 881 |
| Employers with no name route at all | 271 |
| Normalized names carried by two or more tax IDs | 219 |
| Raw names carried by two or more tax IDs | 91 |
| Tax IDs hidden behind a shared name | 227 |
| Hidden tax IDs with no other name route | 223 |

Two different entities sharing a name is not a data error. It is a data fact. The measure
that matters is how much of it the name index can hide.

## Why a shared name loses an entity

The name index stores one record per normalized name:

```python
for n in e["names"]:
    by_name.setdefault(norm_name(n), rec)
```

`setdefault` keeps the first record written for a given name. When two tax IDs carry the
same normalized name, the second is never stored under that name.

The audit re-derives the damage by removing, for every shared name, the tax ID the index
kept, and then checking whether any other spelling of that employer reaches it.

```python
hidden, hidden_unreachable = [], []
for key, feins in norm_shared.items():
    rec = by_name.get(key)
    if not rec or not rec.get("fein"):
        continue
    kept = rec["fein"]
    for f in feins:
        if f == kept:
            continue
        hidden.append(f)
        if f not in fein_to_names:
            hidden_unreachable.append(f)
```

227 tax IDs are hidden behind a shared name. 223 of them have no other route. For those
employers, a name lookup returns a different company and there is no second spelling to
fall back to.

Concrete examples from the collision list:

| Employer name | Tax IDs | Certified filings per tax ID | Name route reaches |
|---|---|---|---|
| Magna Electronics | 823701316, 980442576 | 6, 33 | 980442576 only |
| AArete | 262000001, 824403675 | 3, 1 | 262000001 only |
| AEVEX Aerospace, LLC | 205208340, 330860431 | 1, 1 | 330860431 only |
| Barclays Services | 133714398, 510407971 | 388, 78 | 133714398 only |

The AEVEX row is the interesting one. Two tax IDs, one filing each, identical filing
counts. Nothing about the data distinguishes them, and nothing in the name index says the
other one exists.

## The counterfactual, measured over the full population

The audit does not argue about the index in the abstract. It replays a name-only join over
all 24 sponsors from the 2026-11-08 run and records where it lands.

| Name-only join outcome | Count |
|---|---|
| Lands on the same tax ID the EIN route found | 22 |
| Lands on a different tax ID | 0 |
| Finds nothing at all | 1 |
| Run matched by name, so no tax ID to compare | 1 |

Zero wrong answers, one dropped company. That is the honest result, and it is more
instructive than a scary one would have been.

The dropped company is `Get Vocal, PBC`. The SEC filing says "Get Vocal, PBC". The DOL
employer name is "Get Vocal PBC dba Vocal Media". The `dba` suffix survives normalization
as extra characters, the keys do not match, and a name lookup returns nothing.

```python
norm_name("Get Vocal, PBC")                # 'getvocal'
norm_name("Get Vocal PBC dba Vocal Media")  # 'getvocaldbavocalmedia'
```

The EIN in the filing header matches the index exactly, so the tax ID route keeps the
company and the name route drops it.

Note what the 23-of-24 hit rate hides. The one name-only match the pipeline actually made
was correct. The information was in the other 23 rows, the ones the name route never got
to. A pipeline that only reports on the rows it matched would never have surfaced this.

A second measurement from the same audit: 10 of the 24 sponsors are filed under a
different employer name at the DOL than at the SEC. The tax ID carries the match. The
names do not, and cannot be made to.

## The coverage ceiling

An identifier join is only as good as the window the identifier set covers.

| Measure | Value |
|---|---|
| Newest decision date anywhere in the index | 2026-06-30 |
| Earliest decision date in the index | 2025-10-01 |
| Employers with a filing after the ceiling | 0 |
| End of the Form D window the run covers | 2026-11-06 |
| Days between the ceiling and the window end | 129 |
| Months between the ceiling and the window end | 4.2 |

```python
newest_decision = max(r["last_decision"] for r in by_fein.values())
gap_days = (window_end - date.fromisoformat(newest_decision)).days
```

129 days, about 4.2 months, of the sponsorship signal is out of reach. No employer in the
index has a filing after 2026-06-30, because the index is a quarterly snapshot and the
quarter ends there.

So "has sponsored before" means "sponsored before 2026-06-30, observed on 2026-11-08". A
company that filed its first H-1B paperwork in September 2026 is invisible to this
pipeline, and the output cannot express that distinction.

The ceiling is published with the number rather than kept in a notebook. A count without
its coverage window is not a measurement, it is a memory.

## What an audit of a join should check

Four questions, in the order I would ask them:

1. **How many entities does the key fail to distinguish?** Count the normalized keys held
   by more than one identifier. Here: 219 of 50,307.
2. **How many entities does the key hide entirely?** Remove the identifier the index
   keeps, then test whether any other route reaches it. Here: 223 with no other route.
3. **What would the alternative key have done over the whole population?** Not over the
   rows it caught. Here: 22 same, 0 different, 1 missing, out of 24.
4. **Where does the data stop?** The max date in the index against the end of the window
   the run claims to cover. Here: 129 days.

Question 3 is the one that generalizes. A fallback path cannot be evaluated on the rows it
successfully handled, because it was selected for handling those rows.

## Implementation notes

The audit is a single script, `audit_identity.py`, reading the same `sponsors.json` the
run reads, and it writes `identity-audit.json` next to the run files. Everything in this
post is read from that file.

```python
# The name index keeps one record per name. This is the line that hides entities.
by_name.setdefault(norm_name(n), rec)
```

The pipeline's own cost of doing the identifier join properly: one SEC filing-header
request per company, 0.12 seconds between requests, with the SEC's fair-access rules
honoured. The DOL source file is 251,850,891 bytes.

## What this does not prove

- **No name-based version was shipped.** The counterfactual was measured, not built.
- **Zero wrong answers on 24 rows is not zero wrong answers.** It is 24 rows, from one
  run, on one window.
- **The 91 raw-name and 219 normalized-name collisions are different counts.** One is
  before normalization, one after. The legal entities behind each shared name were not
  individually verified.
- **The 10 differently-named sponsors were not hand-checked.** The tax ID carries the
  match.
- **This measures the index on disk.** A newer quarter moves the ceiling.

---

Source code and the run files are in the public repo. The original version of this post,
with the full narrative, is on my Substack.

If you have audited an entity-resolution step before, I would like to read it. What was
the first thing you measured that a summary file would not have shown you?
