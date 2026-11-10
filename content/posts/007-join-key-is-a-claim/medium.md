# Post 007, Medium version

**Title:** A Join Key Is a Claim About Identity: Auditing Entity Resolution Against a
50,307-Employer Index
**Subtitle:** A framework for choosing, testing and publishing the key that decides what
counts as the same entity in a data pipeline.
**Canonical URL:** the Substack version is the original. Link it.
**Tags:** #dataengineering #entityresolution #datascience #python #audit
**Slot:** Friday framework, technical version. Same facts, mechanism-first.
**Status:** drafted and gated. Needs Asshvin's approval before publishing.

---

## The decision you make once and never revisit

A pipeline that joins two datasets resolves the question of what counts as the same
real-world entity. That resolution is a **join key**, and it is decided once, usually
quietly, and then carried into every number the pipeline produces.

Keys come in two kinds:

- **Strong keys.** A tax ID, a domain, a registry number. Issued by an authority,
  unique by construction.
- **Weak keys.** A name, a title, a city. Chosen by a human or a registry, not guaranteed
  unique.

The two are not interchangeable, and the difference is measurable. This post gives the
framework, and the measurement that produced it from a real pipeline.

## The framework

**A join key is a claim about identity. Make the claim you can defend.**

Three obligations follow from it.

**1. Know how much your key fails to distinguish.** For every key in your index, count how
many distinct identifiers are stored under it. A key held by more than one identifier does
not identify an entity; it identifies a group.

**2. Know how much your key hides.** Storage is not neutral. A key held by multiple
identifiers keeps one and drops the rest. Remove the identifier your index kept and ask
whether any other route reaches it. If not, those entities are invisible, and the pipeline
cannot tell you they are missing.

**3. Test the alternative across the whole population.** Not the rows the alternative
matched. Every row. A fallback path cannot be evaluated on the rows it succeeded on,
because it was selected for handling those rows.

Plus a fourth obligation, on time rather than identity:

**4. Publish the coverage ceiling with the number.** A count without the window it covers
is not a measurement.

## The pipeline

The pipeline joins two free public sources:

- **SEC Form D filings**: companies that recently raised money.
- **DOL H-1B wage filings (LCAs)**: employers that filed a certified wage application,
  with job title, wage and worksite state.

The strong key is the employer's tax ID. The SEC filing's SGML header carries the filer's
EIN; the DOL disclosure row carries the employer's FEIN. Same nine-digit identifier for the
same legal entity.

The weak key is a normalized employer name:

```python
SUFFIX_RE = re.compile(r"\b(inc|incorporated|llc|l\.l\.c|corp|corporation|co|company|ltd|limited|pbc|lp|llp)\b\.?", re.I)

def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", SUFFIX_RE.sub("", (s or "").lower()))
```

Every output row carries the route that produced it (`match`: `EIN` or `name-only`), so
the claim is inspectable per row.

## Obligation 1: how much does the key fail to distinguish?

The index: 437,496 disclosure rows read, 392,175 certified H-1B applications kept,
50,307 employers.

| Measure | Value |
|---|---|
| Employers in the index | 50,307 |
| Keys by tax ID | 50,307 |
| Keys by employer name | 51,137 |
| Employers reachable through more than one name | 881 |
| Employers with no name route at all | 271 |
| Normalized names carried by two or more tax IDs | 219 |
| Raw names carried by two or more tax IDs | 91 |

**219 names are carried by two or more distinct tax IDs.** Different tax IDs are different
legal entities, so those 219 names do not identify a company.

## Obligation 2: how much does the key hide?

A name index stores one record per name. That is what a dictionary does, and it is the
mechanism by which entities disappear.

```python
for n in e["names"]:
    by_name.setdefault(norm_name(n), rec)
```

The audit re-derives the loss by removing, for each shared name, the identifier the index
kept, then testing whether any other spelling reaches it.

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

| Measure | Value |
|---|---|
| Tax IDs hidden behind a shared name | 227 |
| Hidden tax IDs with no other name route | 223 |

Examples from the collision list, with the certified filing counts per tax ID:

| Normalized name | Tax IDs | Filings per tax ID | Name index keeps |
|---|---|---|---|
| magnaelectronics | 823701316, 980442576 | 6, 33 | 980442576 |
| aarete | 262000001, 824403675 | 3, 1 | 262000001 |
| aevexaerospace | 205208340, 330860431 | 1, 1 | 330860431 |
| barclaysservices | 133714398, 510407971 | 388, 78 | 133714398 |

For 223 entities, a name lookup returns a different company and there is no second route.

## Obligation 3: test the alternative across the whole population

The counterfactual: replay a name-only join over all 24 sponsors from the 2026-11-08 run.

| Name-only join outcome | Count |
|---|---|
| Lands on the same tax ID the EIN route found | 22 |
| Lands on a different tax ID | 0 |
| Finds nothing at all | 1 |
| Run matched by name, so no tax ID to compare | 1 |

The dropped company is `Get Vocal, PBC`:

```python
norm_name("Get Vocal, PBC")                # 'getvocal'
norm_name("Get Vocal PBC dba Vocal Media")  # 'getvocaldbavocalmedia'
```

The `dba` suffix survives normalization as extra characters, the keys do not match, and a
name lookup returns nothing while the EIN join keeps the company.

**The methodological point is the important one.** The single name-only match the
pipeline made was correct. Every fact about the fallback's behaviour came from the 23 rows
it never reached. A fallback evaluated only on its successes will always look better than
it is.

Also worth noting: a 23-of-24 success rate on the rows the fallback touched is not a
strong result, it is a small sample. The measurement that matters is the population, not
the hits.

## Obligation 4: publish the coverage ceiling

The same discipline applied to time. The DOL publishes quarterly; this index covers FY2026
Q3.

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

129 days of the sponsorship signal are out of reach, and zero employers have a filing
after the ceiling, because the index is a quarterly snapshot and the quarter ends there.
"Had sponsored before" means "sponsored before 2026-06-30, observed on 2026-11-08".

## The framework as a checklist

Before a join key ships, four questions:

1. **How many entities does the key fail to distinguish?** Count keys held by more than
   one identifier. Here: 219 of 50,307.
2. **How many entities does the key hide entirely?** Remove the identifier the index
   keeps, then test for another route. Here: 223 with no other route.
3. **What would the alternative key have done over the whole population?** Not over the
   rows it caught. Here: 22 same, 0 different, 1 missing, of 24.
4. **Where does the data stop?** Max date in the index against the end of the window the
   run claims to cover. Here: 129 days.

Question 3 is the one teams skip, because question 1 and 2 are answered by reading the
index once and question 3 requires running something.

## Implementation notes

The audit is one script, `audit_identity.py`, reading the same `sponsors.json` the run
reads, writing `identity-audit.json` beside the run files. Every number in this post is
read from that file.

The pipeline's cost of using the strong key properly: one SEC filing-header request per
company, 0.12 seconds between requests, SEC fair-access rules honoured. The DOL source
file is 251,850,891 bytes.

## What this does not prove

- **No name-based version was shipped.** The counterfactual was measured, not built.
- **22 correct out of 24 is 22 out of 24.** One run, one window, one pipeline.
- **The 219 shared names were not resolved to legal entities.** The collision was
  measured; who is who was not adjudicated.
- **223 hidden tax IDs have no other route inside this index.** Whether another source
  reaches them is untested.
- **Nothing has been sent to a company or a person.**

---

Source code and the run files are in the public repo. The original version of this post,
with the full narrative, is on my Substack.

If you have a join key you trust, I would like to read how you tested it. What did you
run against, and what did it cost?
