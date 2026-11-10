---
name: editorial-gate
description: Rebuild bloated LLM output into a 30-second exec read, run a deterministic AI-tell lint, and write approval plans in plain English with reconciled numbers. Use for exec briefs, reports, posts, client decks, and any plan a non-engineer must approve.
---
# Editorial Gate

## Reader lock
Ask who reads it, their role, where it lands (text = 4 sentences; Slack = no markdown headings; doc = sections).

## Five-question frame (score each section 1–5; default verdict CUT)
Importance (specific to THIS reader) · Necessity · Actionability · Action mechanism (verb + artifact + owner + by-when) · Layering (answer first).
keep ≥4.0 with no score <3 · rewrite 3–4 · cut <3 · unanswered → inject.

## Shape
H1 one-sentence thesis · 3-line recommendation · H2s by priority, each ending "So what:" · Next steps (3–5). Hard cap 60% of the original words.

## Charts (first match wins; ~70% of the time: no chart)
single number → none · ratio → bold in prose · ≤5 time points → sparkline · ≤7 categories → sorted horizontal bar · 8–25 → dot plot · pie → bar, always. Bind values to the CSV, never to prose.

## Voice
15–22-word sentences with short punches, contractions, active, concrete nouns, ship/build/pull/run, no hedging, 9th grade. Never mention the tool that made it.

## Lint (blocking)
`python scripts/lint_ai_tells.py <file>`; one auto-retry with the hit list, then halt and show the human. Never silently bypass.

## Plain Plan Mode (for anything someone approves)
📦 deliverable · 💵 money · ⚠ caution · ❓ question only you can answer · 👉 your move. No file paths or commands in the plan. Every number traces to a run or is labeled an estimate; **per-item × count must equal the headline total.**
