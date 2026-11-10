---
name: dossier-builder
description: Build one verified, timeline-ordered dossier per account from CRM, calls, billing, product and support data, with a math-first data audit before it. Use before any churn, win-loss, expansion or ICP analysis.
---
# Dossier Builder (with auditor)

Trust hierarchy when systems disagree: **customer actions > customer voice > CRM-derived state.** The dossier DESCRIBES; it never scores or predicts.

## Wave 0: Audit (math in code, AI calls the verdict)
Order is fixed: domains → joins → revenue → sanity.
- Python writes numbers to disk (`orphan_rate`, `match_count`, fill rates, duplicate-concept columns, LastModified distributions, self-parent loops). The model only labels pass / warning / soft fail / hard fail with one sentence.
- Output `audit/overrides.json`: `do_not_use_fields` (with reason), `tenant_domain`, `primary_id_system`, `rejected_joins`.
- Exclude names containing Fake/Test/Demo/Sandbox at PULL time. Log source counts; fail loud on zero.

## Waves 1–6 (pause after each; show findings; ask the human what looks wrong)
1. **System discovery:** per system: vendor, access, record count, primary key, known issues. Pick ONE canonical join key.
2. **Identity linking:** strip your own company domain before email-domain joins. Require ≥2 of: ID match, domain match, fuzzy name ≥0.92. Six verdicts (keep-auth, keep-email-verified, reject-auth, reject-email-conflict, pending-tiebreaker, indeterminate). 100-row random spot-check by the human.
3. **Revenue & key fields:** one agent per field. >10% disagreement on >5% of rows = a conversation, never averaging.
4. **Timeline assembly:** drop rejected events; provenance on every event; prospect mode splits pre/post first engagement (anti-leakage).
5. **Critique trio in parallel:** statistician, RevOps, outlier hunter (flags rows whose numbers contradict each other).
6. **Render:** each field tagged verified / inferred / fuzzy / missing; <40% confidence → "unavailable".

## Tests before fan-out
Run 3 accounts by hand: one rich, one metadata-only, one thin. Thin accounts must come back "Insufficient data", never a story. Use the strong model on thin accounts.
