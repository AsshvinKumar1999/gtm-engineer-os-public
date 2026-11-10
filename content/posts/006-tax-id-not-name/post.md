# Post 006: I matched companies by tax ID. The names would have lied to me.

**Status:** all three versions drafted and gated. Graphic not yet rendered. Nothing published.
**Slot:** Wednesday teardown.
**Source of every number:** the identity and coverage audit of the Play 06 index
(`plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/identity-audit.json`, regenerate
with `python3 plays/06-fresh-capital-visa-sponsor/audit_identity.py`) and the Play 06 run
files it measures (`summary.json`, `sponsors.csv`). Run date: **2026-11-08**.

---

## Facts and their sources

| Claim | Value | Source file |
|---|---|---|
| Rows read from the DOL H-1B disclosure file | 437,496 | audit `index.rows_read` |
| Certified H-1B applications kept | 392,175 | audit `index.certified_h1b` |
| Employers in the index | 50,307 | audit `index.employers` |
| Index keys by tax ID | 50,307 | audit `index.by_fein_entries` |
| Index keys by employer name | 51,137 | audit `index.by_name_entries` |
| Extra name keys on top of one per employer | 830 | audit `index.extra_name_keys_vs_employers` |
| Employers reachable through more than one name | 881 | audit `index.employers_reachable_by_more_than_one_name` |
| Employers with no name route at all | 271 | audit `index.employers_with_no_name_route` |
| Normalized names carried by two or more tax IDs | 219 | audit `index.normalized_names_shared_by_two_or_more_tax_ids` |
| Raw names carried by two or more tax IDs | 91 | audit `index.raw_names_shared_by_two_or_more_tax_ids` |
| Tax IDs hidden behind a shared name | 227 | audit `index.tax_ids_hidden_behind_a_shared_name` |
| Hidden tax IDs with no other name route | 223 | audit `index.hidden_tax_ids_with_no_other_name_route` |
| Sponsors matched by tax ID in the run | 23 | Play 06 `summary.json` → `by_ein` |
| Sponsors matched by name only | 1 | Play 06 `summary.json` → audit `matched_by_name_only` |
| Name-only join lands on the same tax ID | 22 | audit `run.name_route_would_land_on_same_tax_id` |
| Name-only join lands on a different tax ID | 0 | audit `run.name_route_would_land_on_a_different_tax_id` |
| Name-only join finds nothing | 1 | audit `run.name_route_would_find_nothing` |
| Run matched by name, so no tax ID to compare | 1 | audit `run.name_route_found_nothing_for_a_run_with_no_tax_id` |
| Sponsors whose DOL name differs from their SEC name | 10 | audit `run.sponsors_whose_dol_name_differs_from_sec_name` |
| Newest decision date anywhere in the index | 2026-06-30 | audit `coverage.newest_decision_date_in_index` |
| Earliest decision date in the index | 2025-10-01 | audit `coverage.earliest_decision_date_in_index` |
| Employers with a filing after the ceiling | 0 | audit `coverage.employers_with_a_filing_after_the_ceiling` |
| Gap from the ceiling to the end of the filing window | 129 days, 4.2 months | audit `coverage.days_between_ceiling_and_window_end` |

## What was checked by hand
- The collision list was walked name by name against the index, and every shared name was
  confirmed to point at exactly one tax ID through the name index.
- The 227 hidden tax IDs were re-derived by taking each shared name and removing the tax
  ID the name index kept, then checking whether any other spelling reaches it.
- The name-only join was replayed over all 24 sponsors, not over the ones that happened to
  match, and the one row that found nothing was traced back to the SEC name and the DOL
  name that differ.
- The coverage ceiling was taken from the maximum decision date in the index, not from the
  quarter label on the file name.

## What was NOT done
- I did not re-run the pipeline against a corrected name index. I measured what the name
  route would have done; I did not ship a name-based version.
- The 91 raw-name collisions and the 219 normalized-name collisions are different counts
  of different things. I have not built a list of which legal entities sit behind each one.
- I did not verify whether the 10 sponsors whose DOL name differs from their SEC name are
  the same legal entity. The tax ID says they are; the names do not.
- The audit measures the index that exists on disk. It does not measure a fresher quarter.

---

## Caption (paste into LinkedIn)

**Two companies can share a name. A tax ID cannot. So I matched on the tax ID, and then I checked how much that decision mattered.**

I built a pipeline that joins SEC filings to Department of Labor H-1B wage filings. Company raised money, company has sponsored H-1B workers before, company is hiring now.

The join has to happen on something. There are two candidates: the employer's name, or the employer's tax ID.

I used the tax ID. Then I went and checked whether the name would have worked anyway.

The index holds 50,307 employers from 437,496 disclosure rows.

**219 of those names are carried by two or more different tax IDs.**

Name lookup keeps one tax ID per name. So the other one disappears. 227 tax IDs are hidden behind a shared name this way, and 223 of them have no other spelling to find them by.

**Here is what that would have cost on my own run.** I replayed a name-only join over all 24 sponsors:
→ 22 land on the same tax ID
→ 1 finds nothing at all
→ 1 had no tax ID to compare

The one that finds nothing is Get Vocal, PBC. The SEC filing says "Get Vocal, PBC". The Labor Department says "Get Vocal PBC dba Vocal Media". A legal DBA suffix breaks the key, so the name route loses the company and the tax ID route keeps it.

**What I learned:**
• **A name is a label. A tax ID is a fact.** 219 labels are shared. None of the tax IDs are.
• **A fallback that returns the wrong answer is worse than no fallback.** A name route that silently picks one of two tax IDs is a guess dressed as a join.
• **Check what your fallback is worth.** I ran the name route over all 24 sponsors, not the 1 it happened to catch.
• **Publish the ceiling.** My index stops at 2026-06-30 and my filing window ends 2026-11-06. That is 129 days of blind spot, and I would rather say that than let "has sponsored before" sound current.

**The cost of doing it right:** reading the tax ID out of the SEC filing header, one request per company, 0.12 seconds apart, and the SEC's fair access rules honoured.

Full audit and the numbers. Link in the comments.

What is the thing you match on that you have never checked for collisions?

---

## First comment
The identity audit, the collision list and the source code: https://asshvinkumar1999.github.io/gtm-signal-plays/?utm_source=linkedin

## Attachment
Animated build log: one name key in the middle, 219 names splitting into two tax IDs, 227 going
dark. TODO: render from `identity-audit.json` → `index.collisions`.
