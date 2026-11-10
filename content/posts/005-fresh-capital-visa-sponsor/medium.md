# Post 005, Medium version

**Title:** Joining SEC Form D with DOL H-1B Wage Filings: A Three-Signal Buyer Pipeline
**Subtitle:** Matching companies that raised money against companies that have sponsored
H-1B workers before, and checking the match against live job boards.
**Canonical URL:** the Substack version is the original. Link it.
**Tags:** #python #secedgar #dollabor #dataengineering #automation
**Slot:** Monday build log, technical version. Same facts, mechanism-first.
**Status:** drafted and gated. Needs Asshvin's approval before publishing.

---

## The problem with a two-signal join

The standard public-data GTM pipeline joins two signals: a funding event and a hiring
event. A company that raised money and is hiring for the role your product serves.

That join is good, and it is also noisy in a specific way. Every company that raises money
is a candidate, whether or not they have ever dealt with the constraint your buyer cares
about. For H-1B sponsorship, that constraint is the whole ballgame: the employer's legal
and payroll machinery has to be ready, and the timeline is months longer than a normal hire.

The Department of Labor publishes the signal that shows readiness. Every Labor Condition
Application (LCA) is an employer's statement of the job and the wage it intends to pay for
an H-1B worker. The Office of Foreign Labor Certification posts a full quarter of them as
a free spreadsheet. Roughly 250 MB for FY2026 Q3.

An employer appearing in that file, with certified status, has sponsored this kind of role
before. That is a third signal, and it converts a hiring event into a specific situation.

## The pipeline

```
SEC EDGAR daily index  (2026-10-08 to 2026-11-06)
  → parse each filing, keep operating companies (drop funds, SPVs)
  → dedupe by CIK, keep latest filing
  → parse full Form D, classify industry
  → keep tech companies
  → probe public ATS boards (Greenhouse, Lever, Ashby) by company slug
  → collect open roles per board
  → read the company's EIN from the SGML header of its own filing
  → join DOL H-1B index by EIN, fall back to normalized employer name
  → flag roles whose title overlaps a sponsored title
  → write sponsors.csv, roles.csv, summary.json
```

The index build is the expensive step and it happens once:

```
LCA_Disclosure_Data_FY2026_Q3.xlsx
  → keep VISA_CLASS == "H-1B" and CASE_STATUS == "Certified"
  → group by employer tax ID (FEIN), falling back to a normalized name
  → per employer: certified count, last decision date, top titles, top SOC codes,
    states, median annual wage
  → write sponsors.json  { by_fein: {...}, by_name: {...} }
```

## The join key is the whole design

The single decision that determines the quality of this pipeline is the key.

The SEC filing's SGML header carries the filer's EIN. The DOL disclosure row carries the
employer's FEIN. Both are the same nine-digit tax ID for the same legal entity. Joining on
it is exact.

The fallback is a normalized employer name: lowercase, strip punctuation, strip
`Inc / LLC / Corp / Co / Ltd / PBC / LP / LLP`, remove whitespace.

```python
SUFFIX_RE = re.compile(r"\b(inc|incorporated|llc|l\.l\.c|corp|corporation|co|company|ltd|limited|pbc|lp|llp)\b\.?", re.I)

def norm_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", SUFFIX_RE.sub("", (s or "").lower()))
```

This fallback looks reasonable and it is where the bugs live. It is used in exactly one
case: when the filing's header yielded no EIN, or the EIN is absent from the index. Every
row records which route produced it, in the `match` column: `EIN` or `name-only`.

On this run: 23 of 24 sponsors matched by EIN, 1 by name only.

I audited what the name route would have done on its own, across all 24 sponsors:

| Name-only join outcome | Count |
|---|---|
| Lands on the same tax ID the EIN route found | 22 |
| Lands on a different tax ID | 0 |
| Finds nothing at all | 1 |
| Run matched by name, so no tax ID to compare | 1 |

The "finds nothing" row is `Get Vocal, PBC`. The SEC filing says "Get Vocal, PBC". The DOL
employer name is "Get Vocal PBC dba Vocal Media". A legal DBA suffix breaks the key, so a
name-only join loses the company entirely while the EIN join keeps it.

The "no tax ID to compare" row is `Overwatch Data, Inc.`, the one sponsor with no EIN in
its filing header. Name matching was the only route available, so I checked that row by
hand.

## The similarity test, and where it breaks

A role is flagged as "similar to something they sponsored before" when its title shares at
least two meaningful words with one of the titles on the employer's DOL record. Words are
lowercased, must be at least four characters, and a stop list removes seniority and
department words.

```python
STOP = {"senior", "staff", "lead", "principal", "junior", "associate", "manager",
        "director", "head", "with", "team", "remote", "the", "and", "for", "level",
        "intern", "global", "group"}

def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", (s or "").lower()) if len(w) >= 4 and w not in STOP}

same_kind = any(len(words(job_title) & words(sponsored_title)) >= 2
                for sponsored_title in record["top_titles"])
```

The count of two shared words is a low bar. On this run it produced 55 flagged roles
across 563 open roles.

The failure mode is concentrated, and it is worth writing about precisely. Grouping the 55
by company:

| Company | Flagged roles | Open roles on its board |
|---|---|---|
| Commure, Inc. | 24 | 78 |
| Modal Labs, Inc. | 18 | 44 |
| Contoro Inc. | 5 | 11 |
| Multiply Labs, Inc. | 4 | 13 |
| Legora, Inc. | 3 | 318 |
| Clasp, Inc. | 1 | 6 |

42 of the 55 flags, 76.4%, come from Commure and Modal. And 13 of Modal's 18 flags match
on exactly one sponsored title, "Member of Technical Staff", against roles like "Member of
Technical Staff, Research, Inference" and "Member of Technical Staff, Storage, Stockholm".

The count of shared words is a proxy for similarity, and a generic sponsored title matches
a large slice of one company's board. A stricter test would require at least one
distinctive token rather than any two tokens.

Note also the inverse: Legora has 318 open roles on its board and 3 flags. Role count and
role similarity are independent properties. Any dashboard that implies otherwise is
showing you volume.

## The coverage ceiling

This is the number that decides how much the output can be trusted.

The DOL file is quarterly. The newest decision date anywhere inside the FY2026 Q3 index is
2026-06-30. The Form D window this run covers ends 2026-11-06.

That is 129 days, about 4.2 months, where the sponsorship signal cannot see anything.
Zero employers in the index have a filing after the ceiling.

So "has sponsored before" really means "sponsored before 2026-06-30, as of a 2026-11-08
run". A company that filed its first H-1B paperwork in September 2026 is invisible to this
pipeline. I publish the ceiling with the number because a reader who does not know it will
read the list as current.

## What the run does not cover

**Job board discovery is the binding constraint, not the sponsorship signal.** The ATS
probing looks for Greenhouse, Lever and Ashby by company slug. On this run it found a
board for 30 of the 328 tech companies. 16 of the 24 sponsors had no board found, and
their tier is `no open roles found`. That is a statement about my lookup, not about their
hiring. Any company posting to Workday, Jobvite or a custom careers page is missing from
this pipeline entirely.

**Board identity is inferred, not confirmed.** Greenhouse boards can be name-verified
against the board's own metadata. Lever and Ashby match by slug only. On this run all 8
boards were slug-only, and I checked all 8 by hand against the filing. An unattended rerun
would not have that check.

**A certified LCA is not a visa.** It is an employer's certified wage filing. It shows
readiness to sponsor. It says nothing about whether a petition was filed, granted, or
whether anyone was hired.

## Results from the 2026-11-08 run

Window 2026-10-08 to 2026-11-06. No paid data, no API keys.

| Stage | Count |
|---|---|
| Form D filings | 3,673 |
| Operating companies (funds removed) | 1,203 |
| Tech companies, deduped by CIK | 328 |
| Tax IDs read from filing headers | 302 |
| Companies with prior certified H-1B filings | 24 |
| Sponsors with a job board found | 8 |
| Open roles on those boards | 563 |
| Roles flagged similar to a sponsored title | 55 |
| Sponsors hiring for a similar role (tier 1) | 6 |
| Sponsors hiring for other roles (tier 2) | 2 |
| Sponsors with no board found (tier 3) | 16 |

Every sponsor row carries the EIN the match was made on, the `match` route, the count of
certified filings behind it, the last decision date, the sponsored titles, the states, and
the median wage. Every role row carries the sponsoring company's EIN, the Form D amount
and filing date, and the sponsored titles it was compared against.

## Reproducibility

The index build reads a 250 MB Excel file with `python-calamine` and takes a while. The
run itself fetches 302 filing headers from SEC at 0.12 seconds apart and probes job boards
through a thread pool. Both write plain CSV and JSON, so the numbers in the post can be
recomputed from the files rather than trusted.

I also wrote a separate audit script for this pipeline that measures the things a summary
file cannot tell you: how many employers the index holds, how many names collide across
tax IDs, and where the coverage ceiling sits.

```python
# the number that decides how the output can be read
newest_decision = max(r["last_decision"] for r in by_fein.values())
gap_days = (window_end - date.fromisoformat(newest_decision)).days
```

That gap is 129 days. It is the difference between a list and a snapshot of a list.

## What this does not prove

- **Nobody has received this list.** Whether a hiring manager wants one is untested.
- **16 of the 24 sponsors are unresolved, not inactive.** No board found is not no hiring.
- **The 55 flags are a weak similarity score.** Two shared words, and 13 of them are one
  generic title.
- **12 of the 24 sponsors have exactly one certified filing.** One form is not a pattern.
- **4.2 months of the sponsorship signal is out of reach.** The ceiling is published above.

---

Source code and the run files are in the public repo. The original version of this post,
with the full narrative, is on my Substack.

If you have built a similar join over government filings, I would like to read it. What
was your join key, and what did it cost you when the key was ambiguous?
