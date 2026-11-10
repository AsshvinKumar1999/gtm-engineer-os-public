# Post 007: Two roots make a truth, and a join key is a claim about identity

**Status:** all three versions drafted and gated. Graphic not yet rendered. Nothing published.
**Slot:** Friday framework.
**Source of every number:** the identity and coverage audit of the Play 06 index
(`plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/identity-audit.json`, regenerate
with `python3 plays/06-fresh-capital-visa-sponsor/audit_identity.py`) and the Play 06 run
files it measures. Run date: **2026-11-08**.

---

## Facts and their sources

| Claim | Value | Source file |
|---|---|---|
| Employers in the DOL H-1B index | 50,307 | audit `index.employers` |
| Normalized names carried by two or more tax IDs | 219 | audit `index.normalized_names_shared_by_two_or_more_tax_ids` |
| Tax IDs hidden behind a shared name | 227 | audit `index.tax_ids_hidden_behind_a_shared_name` |
| Hidden tax IDs with no other name route | 223 | audit `index.hidden_tax_ids_with_no_other_name_route` |
| Employers with no name route at all | 271 | audit `index.employers_with_no_name_route` |
| Employers reachable through more than one name | 881 | audit `index.employers_reachable_by_more_than_one_name` |
| Sponsors matched by tax ID in the run | 23 | Play 06 `summary.json` → `by_ein` |
| Sponsors matched by name only | 1 | Play 06 `summary.json` → audit `matched_by_name_only` |
| Name-only join lands on the same tax ID | 22 | audit `run.name_route_would_land_on_same_tax_id` |
| Name-only join lands on a different tax ID | 0 | audit `run.name_route_would_land_on_a_different_tax_id` |
| Name-only join finds nothing | 1 | audit `run.name_route_would_find_nothing` |
| Run matched by name, so no tax ID to compare | 1 | audit `run.name_route_found_nothing_for_a_run_with_no_tax_id` |
| Newest decision date anywhere in the index | 2026-06-30 | audit `coverage.newest_decision_date_in_index` |
| Employers with a filing after the ceiling | 0 | audit `coverage.employers_with_a_filing_after_the_ceiling` |
| Gap from the ceiling to the end of the filing window | 129 days, 4.2 months | audit `coverage.days_between_ceiling_and_window_end` |
| Form D filings in the window | 3,673 | Play 01 `summary.json` → `form_d_new` |
| Tech companies checked against the H-1B index | 328 | Play 06 `summary.json` → `tech_companies` |
| Companies with prior certified H-1B filings | 24 | Play 06 `summary.json` → `sponsors` |
| Sponsors with a job board I could find | 8 | audit `run.sponsors_with_a_job_board_found` |
| Sponsors with no job board found | 16 | audit `run.sponsors_with_no_job_board_found` |

## What was checked by hand
- The 219 shared names were each confirmed to point at exactly one tax ID through the
  name index, and the hidden tax IDs were re-derived from the index rather than counted
  by eye.
- The name-only join was replayed across all 24 sponsors, and the single row that found
  nothing was traced back to the SEC company name and the DOL employer name that differ.
- The coverage ceiling was taken as the maximum decision date in the index, not from the
  quarter label on the file name.

## What was NOT done
- The 219 shared names were not individually resolved to legal entities. I measured the
  collision, I did not adjudicate who is who.
- I did not ship a name-based version to compare against. The counterfactual was measured
  over the existing run.
- 223 of the 227 hidden tax IDs have no other name route, but I did not check whether any
  of them are reachable through a route outside this index entirely.
- Nothing here has been sent to a company or a person.

---

## Caption (paste into LinkedIn)

**The rule I keep coming back to: a join key is a claim about identity. Make the claim you can defend.**

Two companies can share a name. A tax ID cannot.

Here is where that came from. I joined SEC filings to Department of Labor H-1B filings to find companies that raised money, have sponsored H-1B workers before, and are hiring now.

I had to pick a key. Name or tax ID. I picked the tax ID, then I checked how much that choice actually mattered, because "I picked the better one" is not a reason.

The index holds 50,307 employers.

**219 of their names are carried by two or more different tax IDs.**

Different tax IDs mean different legal entities. So 219 names in this index do not identify one company. They identify two or more.

And a name index keeps one tax ID per name, because that is how a dictionary works. So the other one is not stored. 227 tax IDs are hidden behind a shared name. 223 of them have no other spelling that reaches them.

**Then I replayed a name-only join across all 24 sponsors in my own run.**
→ 22 land on the same tax ID
→ 1 finds nothing at all
→ 1 had no tax ID to compare

**The rule I keep coming back to:** a name is a label. A tax ID is a fact. Join on the fact.

Two things I would put next to that rule:
• **Test the fallback across the whole population.** The one name match my pipeline made was correct. The information was in the other 23 rows, the ones the fallback never reached.
• **Publish the ceiling with the number.** My index stops at 2026-06-30 and my filing window ends 2026-11-06. 129 days of blind spot. If I do not say that, "has sponsored before" sounds current and it is not.

**Here is what I am actually saying.** When you pick a join key, you are making a claim about what counts as the same thing. Names make a weak claim. Tax IDs make a strong one. And the right way to find out which claim you are making is to test the alternative against every row, not the rows that worked.

Big thank you to Jordan Crawford, whose writing on public data got me started.

The audit, the collision list and the numbers are in the first comment.

What do you join on, and have you ever tested the alternative against your whole population?

---

## First comment
The audit script, the collision list and the run files: https://asshvinkumar1999.github.io/gtm-signal-plays/?utm_source=linkedin

## Attachment
Animated build log: one shared name splitting into two tax IDs, one going dark, the ceiling
date appearing on every row. TODO: render from `identity-audit.json`.
