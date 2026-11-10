# Personal Brand Playbook for a GTM Engineer

Built from how Jordan Crawford went from zero to a top-50 Substack in under two months, and adapted for you.

## 1. Pick your category of one (week 1)
Jordan never competes with other GTM engineers; nobody cross-shops him. Narrow until it sounds like a joke, then go deeper.

Fill this in (keep it in `brand/positioning.md`):
- **I find the list no vendor sells for ___ (one vertical or one market).**
- **I sell exactly three things:** ___, ___, ___. Everything else is a no.
- **The opinion the market disagrees with:** ___ (Thiel test).
- **My unfair data:** the public records / market / corpus I know better than anyone.

Strong options for you, based on where Jordan is thin:
1. **The non-US public-data GTM engineer** (e.g. India: MCA21 filings, GST, Udyam MSME, FSSAI, CDSCO, RERA, GeM tenders, BSE/SEBI disclosures). He is US-only; this is a lane he can't easily enter.
2. **One vertical, measured over time** (e.g. clinics, logistics, manufacturing). He hops verticals weekly; you publish the same play's results month after month.
3. **The enterprise-safe AI GTM engineer:** official APIs, human-labeled answer keys, published accuracy *and* cost per right answer.

## 2. The content engine (weeks 1–2)
Rule: **never invent the scenario.** Only write what you actually built, with receipts.

Set up:
- `brand/voice/style-guide.md`: record 5 of your own calls or Looms, transcribe, extract how you open, transition and close; sentence length; words you use.
- `brand/voice/anti-patterns.md`: your kill list (start from `scripts/lint_ai_tells.py`).
- A session-capture habit: at the end of every build session, ask Claude: "Summarize what I built today, the number that mattered, what broke, and the principle. Append to `brand/log/YYYY-MM-DD.md`." When 3+ entries share a topic, that's a post.

Post template (his, proven):
1. **Title:** a specific number + an outcome ("I scored every parking lot in America for $45"). First 33 characters must stand alone (Gmail mobile).
2. **Hook:** person + situation + tension. No summaries.
3. **Story with receipts:** what you tried, the real numbers, what broke.
4. **The named principle** in one line ("Diagnose first. Scrape second.").
5. **Honest limits:** what this doesn't prove.
6. **The recipe:** a paste-into-Claude-Code prompt (What I did / What you want / Use these tools / Watch for / If you get stuck).
7. **One CTA.**

Run `python scripts/lint_ai_tells.py` on every draft. Write the first draft yourself; let the model edit.

## 3. Proof assets (weeks 2–6)
Ship one free, genuinely useful public asset every 2 weeks. Each one is a lead magnet and a credibility receipt:
- An open-source skill on GitHub (start with one from `skills/`, adapted to your niche).
- A free dataset or sheet (e.g. "every ___ in ___ that was fined in 2026").
- A vendor benchmark in your niche (run 5–10 tools on the same 200 rows, publish accuracy + cost per right answer, disclose conflicts).
- A named list ("15 RevOps leaders in ___ worth following") that also builds relationships.

## 4. Distribution (ongoing)
- **LinkedIn:** 3 posts/week, each a compressed build log with one number and one image (a real table/chart screenshot, not stock art). Comment thoughtfully on 10 posts/day from people in your target market.
- **Newsletter (Substack or similar):** 1 deep post/week. Cross-post the free half to LinkedIn.
- **Guest posts and co-authored frameworks:** borrow audiences (Jordan did Topline; co-built "Find a Rep" with Matt Braley). Pitch one operator per month: "Your framework + my build."
- **Live builds:** offer a free 45-minute "bring a real problem, I build it live" session monthly. Record it. That's a post and a video.
- **Plant seeds:** do one small free build per week for someone (no ask). The person you helped for free is the one who calls you first.
- **Event promotion like his Chicago play:** when you speak anywhere, find your connections within driving distance, rank by fit × engagement, and send each a doc where you actually ran your tool on their company.

## 5. Monetization ladder (when you have ~500 engaged readers)
Free (see the shift) → paid recipes (see the build) → tools/skills installed (run it) → done-for-you data jobs → advisory with equity for select companies. Add discount-code partnerships with the vendors you genuinely use, and disclose them.

## 6. What to measure monthly
Followers/subscribers from target roles (not total) · inbound conversations started · free builds shipped · assets published · paid conversions · one testimonial collected.

## 7. Your first 30 days
| Week | Ship |
|---|---|
| 1 | Positioning doc. 5 recorded calls → style guide. First build log post (something you built this week, real numbers). |
| 2 | Open-source one skill on GitHub with a README and worked example. Post about it. |
| 3 | Run the asymmetry engine on a real dataset in your niche; publish the most interesting finding as a free post + sheet. |
| 4 | First live build (5–20 people). Publish the recording + recipe. Pitch one guest post. |

Use the recurring review task's suggestions each week to pick what to build next.
