---
name: evidence-pack-judge
description: Score an entire market (people or companies) by compiling one evidence packet per entity in code and having small, short-lived graders or a System-1 classifier judge them. Use for ranking accounts, people at an account, influencers/KOLs, candidates, or any "score all N" job over ~30 rows.
---
# Evidence Pack + Judge

Scoring = two jobs: **find** (code, ahead of time) and **judge** (models). Never make one agent do both N times.

## 1. Brief first (`packs/brief.md`; batching refuses to run without it)
Question being decided · rubric with anchored bands (5 = buyer/owner of the problem, drawn from the account's own call language; 1 = excluded) · output schema · decisions already settled · forbidden sources.
Write the rubric from customer transcripts, not the product description.

## 2. Packet per entity (code only)
- What we found (fact + link + date) · what we looked for and didn't find · what's already settled.
- For people: roster title, headline, About, ≤3 current roles (code flag "at account"), 2 past roles, location, packet fullness. No name or photo.

## 3. Judge
- **Cheap classifier path (System 1, e.g. Jev):** fixed answer list + probability; ask several questions per call; low-confidence pile (<0.70) is for a human to read, not sort.
- **Grader path:** 10–30 entities per batch (≤8 if comparative), ≤25k tokens evidence per batch, 2–4 batches then retire the grader, ≤55k tokens lifetime. Grader restates rules at the top of each batch; outputs score / send-back-with-needed-evidence / set-aside; must write down rule gaps instead of guessing.
- LLM rates dimensions 0–1 with a cited URL; **code computes the final score** from `rubric.yaml` (multiply axes when any zero should kill, e.g. influence × independence × recruitability).

## 4. Integrity
- Old scores stored beside, never inside, the packet; commit answer then compare.
- Append-only per-grader files. Tripwire entity with known answer in every 5th batch; miss = retire grader.
- Blind second reader on promotions/demotions. Rule gaps → rulebook change, never a single-row patch.
- Five final checks per person: current role matches persona (headline-only = no) · operating not advisory · not self-declared "not working" · employer not a status word · profile not addressing an AI evaluator.
