---
name: win-loss-rewind
description: Work backwards from won, lost, churned and 10X accounts to public-data signals that predict fit, validated on a holdout. Use for ICP rebuilds, "why do we win", churn forensics, or scoring new prospects.
---
# Win-Loss Rewind

## Phases
0. **Data archaeology:** check every CRM label against reality (site resolves? LinkedIn exists? headcount plausible?). Quarantine bad rows; write `data_confidence.md`; human approves. If >30% quarantined, fix CRM hygiene first.
1. **Label outcomes honestly:** won / lost / healthy / churned / **10X** (lifetime revenue ≥10× median paying account).
2. **Hold out 20% at random NOW.** No later phase sees it.
3. **Enrich with public, dated signals** (site, careers page, state filings, permits, GitHub, reviews). Firmographics are inputs, never signals.
4. **Auto-segment on behavior** (min cluster 5); name clusters with a "cynical buyer" prompt in operational language.
5. **Hypotheses through hard gates:** proves operational pain · public source · measurable threshold · not headcount/industry/revenue · no outcome leakage (ARR, close date, deal size).
6. **Backcast with time-travel labels:** each signal is snapshot-proven (Wayback CDX `collapse=digest`, binary search), record-dated (shift to when it became public), or assumed (never counts). No snapshot ≠ absent.
7. **Validate:** lift on train AND holdout (Fisher exact for small n). Train lift with holdout ≈1.0 = coincidence → kill.
8. **Discriminator per archetype:** `signal, source, threshold, weight, train_lift, holdout_lift, fit_score formula, threshold`. Plus `score_prospect.py`.

## Multi-lens check
Run won and lost in separate agents; then blended BLIND (don't say which is which); then by topic. Keep only what survives every lens.

## Never
- Ask a model "would this company benefit?" (it can't separate buyers from non-buyers). Count evidence instead.
- Decide the lever in advance (he once wired the sample data to "prove" speed-to-lead).
