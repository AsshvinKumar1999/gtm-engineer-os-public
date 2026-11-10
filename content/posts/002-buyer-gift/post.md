# Post 002: I built the buyer list for 5 companies I want to work for

**Status:** caption drafted and linted. Graphic not yet rendered. Substack and Medium versions to follow.
**Slot:** Monday build log.
**Source of every number:** `plays/01-fresh-capital-open-role/out/30d-2026-11-09/summary.json`,
`gift-summary.json`, and the five files in `gifts/`. Nothing here is estimated.

---

## Facts and their sources

| Claim | Value | Source file |
|---|---|---|
| Form D filings scanned | 3,251 | `summary.json` → `form_d_new` |
| After removing funds and SPVs | 1,089 | `summary.json` → `operating` |
| Tech companies, one per company | 297 | `summary.json` → `tech` |
| Companies with a public job board | 27 | `summary.json` → `with_board` |
| Open roles found | 719 | `summary.json` → `open_roles` |
| Companies that raised AND hire the target role | 12 | `summary.json` → `tier1` |
| Gift matches, 5 buyer profiles | 11 + 9 + 6 + 9 + 9 = 44 | `gift-summary.json` |
| Unique companies across all 5 sheets | 18 | `gifts/*.md`, deduped by name |
| Total raised by those 18 companies | $1,908,732,450 | `gifts/*.md`, deduped by name |
| Matching live roles across all 5 sheets | 231 | `gifts/*.md` |
| Name-verified board matches | 6 (3 unique companies) | `gifts/*.md` |

Filing window: 2026-10-10 to 2026-11-08. Data cost: $0.

## What was checked by hand
- Every number above is read from the run files, not typed from memory.
- The dedupe to 18 unique companies was done by name, because one company appears in
  several sheets when it fits more than one buyer profile (Legora appears in all five).
- Board matching is split into `name-verified` (Greenhouse confirms the company name)
  and `slug-only` (Ashby/Lever matched by URL slug). The sheets say which is which.
- Every Form D link in the sheets points at the actual filing on sec.gov.

## What was NOT done
- No company was contacted. No recruiter was emailed. The list exists; nobody knows yet.
- The 530 roles in the "Other" bucket were not reviewed by hand.
- Only 27 of 297 tech companies had a public job board findable by slug. The other 270
  are not missing companies; they are companies whose board we could not locate.
- No paid data was used. No API key. No scraping behind a login.

---

## Caption (paste into LinkedIn)

**Hiring manager: here's a list of 18 companies that just raised $1.9B and are hiring your buyers.**

I ran my own playbook against five companies I want to work for. Here is what came back.

The play takes two public signals and joins them:
→ SEC Form D, which every private US company must file after it raises money
→ Live job posts on Greenhouse, Lever and Ashby, which no one has to pay for

If a company raised AND is hiring the role its product serves, that is a real buying reason. Money says they can buy. A job post says what they are trying to fix.

Last 30 days of filings:
3,251 filings → 1,089 real companies (funds and SPVs removed) → 297 tech companies → 27 with a findable job board → 719 open roles → 12 hiring for the target role.

Then I ran it five more times, once per company, each with a different buyer signature.

Baseten sells inference. So I looked for companies that raised and are hiring ML engineers. 11 of them.
Bluejay sells evals for voice and text agents. So I looked for voice, AI and agent engineers. 9.
Nectar sells community-led growth. Raised and hiring community, social or brand roles. 9.
Wispr Flow sells dictation into sales teams. Raised and hiring a sales team. 9.
FlowGen Labs sells GTM engineering to companies mid-migration. Raised and hiring SAP, ERP or systems roles. 6.

44 matches across 5 sheets. 18 unique companies, because some of them fit more than one profile. $1.9B raised between them. 231 live job posts.

**The surprise:** Modal Labs raised $601M on 2026-10-20 and is hiring Forward Deployed Engineers for ML in New York and London. It shows up in four of my five lists. One public filing, five different buys.

**What I learned:**
• **Two signals are a play.** A raise alone is noise. A job post alone is noise. Both, in the same window, is a reason to talk.
• **Dedupe by name.** 44 matches was 18 companies. A company that fits four profiles is one buyer, not four.
• **Say how you matched the board.** 6 of my matches are name-verified. The rest are slug-matched. A reader deserves to know which is which.
• **The unverified list is still worth $0.** A slug match is a lead. A name match is a fact. Both are better than a guess.

Every number above is read from the run file. Every filing links to sec.gov. I checked the dedupe and the totals by hand.

Full play and the source code on my site. Link in the comments.

Would you send this to a hiring manager, or would you read it and ignore it?

---

## First comment
The full play, the five gift sheets and the source code: https://asshvinkumar1999.github.io/gtm-signal-plays/

## Attachment
Animated build log: `out/graphic.mp4` (0.41 MB) and `out/graphic.gif` (0.87 MB).
Canvas 1080x1350, LinkedIn 4:5. Every tile is one real filing from the run file; the
five wires carry the packets into the five buyer lists.

Data block in `graphic.html` is bound to `summary.json` and `aggregate.json`.
