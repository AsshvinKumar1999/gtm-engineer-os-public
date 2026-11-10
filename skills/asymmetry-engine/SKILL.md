---
name: asymmetry-engine
description: Mine a customer corpus (transcripts, back-end samples, public web) into 5 candidate insights a buyer would pay to receive. Use when asked "what should we say", "find our PVP", "what do we know that buyers don't", or before writing any outbound campaign.
---
# Asymmetry Engine

Goal: manufacture more information about the buyer's situation than the buyer has, then ship it as a gift usable without a reply.

## Inputs (ask for what's missing; messy is fine, "we can't answer that" is itself a finding)
- `/transcripts/` customer calls (sales, onboarding, QBR, support). Whisper any untranscribed recordings.
- `/schema/` DDL of back-end tables >10k rows + `/samples/` ~200 rows each (anonymize).
- `/web/` each customer's site, press, jobs, funding (Exa/Parallel/cheap SERP).
- `/acquired/` any cheap third-party data.

## Step 0: the questions
Write answers to `work/asymmetry-brief.md` before running agents:
1. If your next best customer kidnapped your engineers with root on your data, what 3 queries would they run?
2. What do we know about the buyer's situation that they would *pay* to learn?
3. What keeps this buyer up at 3 a.m., in dollars?

## Step 1: four parallel subagents (separate contexts, write to disk)
- **A Transcript Miner:** cluster questions customers already asked → top 10 by frequency, one verbatim quote each (quote must be an exact substring; verify in code).
- **B Data-First Perspective:** role-play a buyer about to ship {specific product/decision}; read schema + samples → 10 questions whose answers would change that decision.
- **C Dollar-Pain Scanner:** last 18 months of customer-side money events (settled lawsuits, shut product lines, layoffs, fired execs, regulator actions, missed launches), ranked by $ with primary-source links.
- **D Synthesizer:** combine A+B+C into 5 candidates of the form:
  "Across our {N} customers, {X} did {thing}. {Y} of those experienced {outcome}. The distinguishing factor was {single variable}."
  Each must cite a real number, be useful to a non-buyer, be forwardable.

## Step 2: generate → push back → validate
- Kill the 4 that read like a slide deck. Ask the model for the count, threshold and source behind the survivor.
- If none survive, raise C's dollar threshold and rerun (usually 3 runs).
- Take the survivor to one real customer (or an ex-customer employee): "Would you want to know this?" Listen to the no.

## Guardrails
- Aggregate; never expose one customer's specifics to another.
- Sort by buyer pain magnitude, never by your product features.
- Output: `work/asymmetry-candidates.md` (5 candidates + supporting numbers + verdict). Then hand to `pvp-writer`.
