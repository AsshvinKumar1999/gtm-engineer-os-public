# Post 002, Medium version

**Title:** Deduplicating Two Public Signals: A Buyer-List Generator for Job Applications
**Subtitle:** Joining SEC Form D filings with public ATS job APIs to build lists that are
checkable by the person receiving them.
**Canonical URL:** the Substack version is the original. Link it.
**Tags:** #python #secedgar #gtmengineering #automation #data
**Slot:** Monday build log, technical version. Same facts, mechanism-first.
**Status:** drafted. Needs Asshvin's approval before publishing.

---

## The problem with outbound job applications

Every job application asks the same question in different words: *why should we hire you?*
The applicant answers with a story. The reader gets a hundred of these a week and learns
to skim.

There is a different kind of message that gets read, and it is not a better story. It is a
different kind of object. Instead of a claim, you hand over an artifact the reader can
verify in ninety seconds.

For a GTM engineer, there is a natural candidate for that artifact: a list of companies
that recently raised money **and** are currently hiring for a role that the target company
sells into.

## Two signals, one join

The data has to satisfy three properties at once: free, dated, and hard to fake.

**SEC Form D** satisfies all three. Private US companies must file a Form D after a
qualifying raise. It is public, it carries a filing date and a dollar amount, and it is
legally required, so it cannot be faked without committing a crime. It is also a large
amount of noise: about half of Form D filers are funds and SPVs that file because they
are legally required to, not because they operate a business.

**Public ATS APIs** (Greenhouse, Lever, Ashby) satisfy free and dated trivially. They are
a weaker fit on "hard to fake" in the sense that a company can post a role it does not
intend to fill, but in practice that is rare and not worth defending against.

The join is what creates the signal. A raise alone says a company might buy. A job post
alone says a company might need something. A company that did both inside the same
window is telling you what it is trying to fix and confirming it can pay for the fix.

## The pipeline

```
SEC EDGAR daily index  (30 days)
  → parse each filing, keep operating companies
  → dedupe by CIK, keep latest filing
  → parse full Form D, classify industry
  → keep tech companies
  → probe public ATS boards by company slug
  → score roles against a buyer signature
  → write gift sheet
```

Three details that decide whether the output is honest.

**Dedupe by CIK before scoring.** A company files several Form Ds in a month. Scoring
filings instead of companies inflates every count downstream.

**Filter to operating companies before classifying.** The fund/SPV regex is the single
most important line in the pipeline. On this run it removed 3,251 filings down to 1,089
real companies, which is a 66% cut before anything else happens.

**Score roles, not companies.** The buyer signature is a regex over job titles. A company
matches when it has at least one live role matching the signature. This is what makes the
output a list of *buyers* rather than a list of companies that raised.

## The deduplication bug that would have made this post a lie

Running five buyer profiles against the same set of filings produced 44 rows. But the same
company appears in multiple sheets when it happens to match multiple signatures.

Deduplicated by name: **18 unique companies**.

A naive implementation ships "44 companies" and is wrong by 2.4x. And a naive
implementation that reports both numbers without explaining the gap is worse, because the
reader cannot tell which one to trust.

The fix is trivial (a dict keyed on company name) and the reason it matters is not
technical. If you send a hiring manager "44 companies" and they check three of them and
find duplicates, the rest of your work stops being credible. Deduplication is not a
detail. It is the difference between a list and a receipt.

## Verification is the product

Every row in the output carries two links: the filing on sec.gov, and the live job post.
Nothing is a summary. The reader can click through to the primary source on every claim.

Board matching is recorded per row, because the two methods have different evidentiary
weight:

| Method | ATS | What it means |
|---|---|---|
| `name-verified` | Greenhouse | The board's own company name matches the filing |
| `slug-only` | Ashby, Lever | The board was matched by URL slug |

On this run: 6 of the 44 rows are name-verified (3 unique companies, since one
appears in four sheets) and 38 are slug-only. Both are worth
sending. A slug match is a lead, a name match is a fact, and the sheet says which is
which.

## Results from a real 30-day window

Window 2026-10-10 to 2026-11-08, no paid data, no API keys.

| Stage | Count |
|---|---|
| Form D filings | 3,251 |
| Operating companies (funds removed) | 1,089 |
| Tech companies, deduped by CIK | 297 |
| Companies with a locatable job board | 27 |
| Open roles | 719 |
| Raised AND hiring the target role | 12 |

Five buyer signatures, run against the same filings:

| Buyer signature | Matches | Unique companies |
|---|---|---|
| ML / AI / inference engineering | 11 | — |
| Voice / AI / NLP / agent engineering | 9 | — |
| Community / social / brand / growth | 9 | — |
| Sales team (AE, SDR, BDR, RevOps) | 9 | — |
| SAP / ERP / systems engineering | 6 | — |
| **Total rows** | **44** | **18 after dedupe** |

Total raised across the 18 unique companies: $1,908,732,450. 231 matching live roles.

The single largest: Modal Labs, $601,892,375 on 2026-10-20, hiring Forward Deployed
Engineers for ML. It appears in four of the five sheets, because one company can
genuinely be a buyer of several things. Overlap across signatures is signal, not noise.

## What this does not prove

Being precise about the limits is more useful than being precise about the results.

- **27 of 297.** Three quarters of the tech companies had no locatable job board. They
  are not absent from the population; they are absent from my ability to locate them.
- **Slug matching is inference.** 38 of 44 rows are matched by URL slug. The likelihood
  that a given slug-matched board is the wrong company is low but not zero.
- **Nothing has been sent.** The lists exist. Whether a hiring manager wants one is
  untested.
- **The 530 "Other" bucket was not reviewed by hand.** The filter is regex on title, so
  it misses roles whose titles do not say what they are.

## Implementation notes

Standard library only. The two things that would otherwise need dependencies are XML
parsing (`xml.etree`) and concurrency (`concurrent.futures`). SEC's fair-access rules ask
for a contact in the user agent and under ten requests per second, which the script
honors with a delay between calls.

Runtime is dominated by the SEC fetch, roughly six minutes for a 30-day window. The ATS
probing runs across a small thread pool.

```python
# The dedupe that decides whether the output is honest
unique = {}
for sheet in sheets:          # 5 buyer signatures, same filings
    for row in sheet:
        unique.setdefault(row["company"], row)   # one company, one buyer
# 44 rows in -> 18 companies out
```

## Why this shape

The output is a list, not a pitch, because a list is verifiable and a pitch is not. Every
claim links to a primary source the recipient can open. If the list is wrong, they can
see exactly where, which means the failure mode is bounded and specific rather than
"trust me."

For a GTM engineer specifically, this is the same argument as a good outbound email: a
permissionless value proposition. It is worth something to the reader whether or not they
ever reply, and it demonstrates competence without requiring the reader to take your
claims on faith.

---

Source code and the run files are in the public repo. The original version of this post,
with the full narrative, is on my Substack.

If you have built something similar, I would like to read it. What did you send, and did
they reply?
