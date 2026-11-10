# Post 005: 8 companies that just raised money, hired H-1B workers before, and are hiring now

**Status:** all three versions drafted and gated. Graphic not yet rendered. Nothing published.
**Slot:** Monday build log.
**Source of every number:** the Play 06 run of 2026-11-08
(`plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/summary.json`, `sponsors.csv`,
`roles.csv`), the Play 01 run it read
(`plays/01-fresh-capital-open-role/out/30d-2026-11-08/summary.json`), and the identity
audit written for this post
(`plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/identity-audit.json`,
regenerate with `python3 plays/06-fresh-capital-visa-sponsor/audit_identity.py`).
Run date: **2026-11-08**. Filing window: **2026-10-08 to 2026-11-06**.

---

## Facts and their sources

| Claim | Value | Source file |
|---|---|---|
| Form D filings in the window | 3,673 | Play 01 `summary.json` → `form_d_new` |
| Operating companies after funds and SPVs are removed | 1,203 | Play 01 `summary.json` → `operating` |
| Tech companies, one row per company | 328 | Play 01 `summary.json` → `tech` |
| Tech companies with a job board Play 01 could find | 30 | Play 01 `summary.json` → `with_board` |
| Tech companies checked against the H-1B index | 328 | Play 06 `summary.json` → `tech_companies` |
| Tax IDs read out of the SEC filing headers | 302 | Play 06 `summary.json` → `ein_found` |
| Companies that had filed H-1B wage paperwork before | 24 | Play 06 `summary.json` → `sponsors` |
| Matched on the company's tax ID | 23 | Play 06 `summary.json` → `by_ein` |
| Matched on company name only | 1 | Play 06 `summary.json` → audit `matched_by_name_only` |
| Times the name fallback was tried | 305 | audit `run.name_route_attempts` |
| Times the name fallback matched | 1 | audit `run.name_route_hits` |
| Of the 24 sponsors, how many had a job board I could find | 8 | audit `run.sponsors_with_a_job_board_found` |
| Sponsors whose names differ at the DOL and at the SEC | 10 | audit `run.sponsors_whose_dol_name_differs_from_sec_name` |
| Open roles on those 8 job boards | 563 | Play 06 `summary.json` → `roles_at_sponsors` |
| Roles that look like the work they filed for before | 55 | Play 06 `summary.json` → `roles_similar_to_sponsored` |
| Sponsors with a role like a sponsored one open | 6 | Play 06 `summary.json` → `tier1_similar_role_open` |
| Sponsors with only other roles open | 2 | Play 06 `summary.json` → `tier2_other_roles_open` |
| Sponsors with no job board found | 16 | Play 06 `summary.json` → `tier3_no_open_roles_found` |
| Roles from the two biggest contributors to the 55 | 42 | audit `run.top_two_flagged_roles` |
| Their share of the 55 | 76.4% | audit `run.top_two_share_of_flags_percent` |
| Modal roles flagged against one sponsored title | 13 | audit `run.modal_flags_from_one_generic_title` |
| Modal roles flagged in total | 18 | audit `run.modal_flags` |
| Sponsors with exactly one certified filing behind them | 12 | audit `run.sponsors_with_exactly_one_certified_filing` |
| Legora open roles | 318 | audit `run.legora_roles` |
| All 8 job boards were matched by URL slug, not by name | 8 of 8 | Play 01 `accounts.csv` → `board_match` = `slug-only` |

## What was checked by hand
- Every number above is read from the run files, not typed from memory.
- I opened all 8 job boards and checked the company name and the locations on them against
  the SEC filing behind the match.
- The 55 "looks like the work they sponsored before" roles were recounted from `roles.csv`
  by company, and the 42 and the 76.4% were recomputed from that recount.
- The 13 Modal roles matched against "Member of Technical Staff" were listed one by one and
  confirmed to be the only sponsored title that matched on those rows.
- All 8 boards were matched by URL slug. A slug match is a lead, not a fact, so every one
  of the 8 was checked against the filing by hand.

## What was NOT done
- No company was contacted. No recruiter was emailed. Nobody has received this list.
- The 16 sponsors with no job board found were not verified by hand. Play 01 found a board
  for only 30 of the 328 tech companies, so "no board found" is a limit on my search, not a
  statement that those 16 are not hiring.
- A certified wage filing is a first step, not a granted visa. Nothing here says a visa
  was granted, or that any of these 8 will sponsor anyone.
- The H-1B index used in this run stops at a decision date of 2026-06-30, so a company that
  filed paperwork after that date is not in this list.
- I did not run this play again after the run date, so every "now" in the post means
  "as of 2026-11-08".

---

## Caption (paste into LinkedIn)

**Job hunting in tech? I found 8 companies that just raised money, filed H-1B paperwork before, and are hiring now.**

I built a free workflow that finds them. No paid tools, no API keys.

Three public signals, joined:
→ SEC Form D. When a US company raises money it files a short notice. Public, dated, hard to fake.
→ Department of Labor H-1B wage filings. Every certified filing names the employer, the job and the state.
→ Live job posts. Greenhouse, Lever and Ashby all publish their boards without a login.

So the workflow asks one question:

**"Did this company raise money, file H-1B paperwork for this kind of job before, and is it hiring for it now?"**

Money says they can pay. A wage filing says they have done this before. A job post says what they want.

I ran it on 30 days of filings, 2026-10-08 to 2026-11-06.

3,673 filings → 1,203 real companies, funds removed → 328 tech companies → 24 that had filed H-1B paperwork before → 8 with a job board I could find → 563 open roles → 55 that look like the work they filed for before.

I opened all 8 job boards and checked them against the filings by hand.

**The surprise:** 42 of those 55 roles come from just two companies. Commure and Modal Labs. My "55" is mostly two employers.

**What I learned:**
• **A role looks similar when two words overlap.** 13 of Modal's 18 hits matched on one sponsored title, "Member of Technical Staff". Read the words before you trust the match.
• **Half the list is one filing deep.** 12 of the 24 have exactly one certified filing behind them. Still real, still thin.
• **The name fallback fired 305 times and caught 1 company.** Everything else matched on the company's tax ID.
• **It cost $0.** Free data, no signup.

**Hiring someone who needs visa sponsorship?**
The same Department of Labor file lists every employer that filed H-1B paperwork, with the roles and the wage. It is free, and it is the record of who has done this before.

Big thank you to Jordan Crawford, whose writing on public data got me started.

The 8 companies, the 563 roles and the source code are in the first comment.

What would you want next, the companies hiring now or the ones filing paperwork?

---

## First comment
The 8 companies, the 563 roles and the source code: https://asshvinkumar1999.github.io/gtm-signal-plays/?utm_source=linkedin

## Attachment
Animated build log: 3,673 filings draining into 24 sponsor cards, 8 lighting up with open roles.
TODO: render from `out/30d-2026-11-08/summary.json` and `roles.csv`.
