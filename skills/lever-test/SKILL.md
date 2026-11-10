---
name: lever-test
description: Test whether a candidate business habit actually causes an outcome, with the right statistics for small counts — Wilson intervals, a 95% lever test, a tie band, and a maturity window read from your own data. Use before claiming a tactic works, before ranking reps/accounts/sources, or when someone proposes a lever in advance.
---

# Lever Test

Most GTM "insights" are a number that happened. This skill decides whether a habit
actually changes an outcome, and refuses to rank anything the data cannot separate.

**The rule that survived:** never decide the lever in advance. Test every candidate
habit the same way, then let the data pick.

---

## Step 0 — the control variable goes on the outside

Before comparing anything, decide what confounds it. If reps get different mixes of
lead sources, the rep with more partner leads looks better for reasons that have
nothing to do with the rep.

**Put the control variable on the outside loop.** Compare reps *inside one lead
source at a time*, then pool. Lead source before rep scorecard, always.

**The fair metric vs the headline metric.** Use two numbers and label them:

- **Fair measure** — deals won per 100 leads. Same denominator for everyone.
- **Headline** — dollars per 100 leads. What the business cares about.

Deal size is context and **never** the coaching number: it rests on a handful of
wins, so it swings on noise.

---

## Step 1 — the maturity window comes from your own data

Do not assume "last 90 days." Read it:

1. From your own won deals, find the age at which **9 in 10** had closed.
2. Round up to the next multiple of 5 days.
3. If you have fewer than 20 wins, fall back to 90 days and say so.

Judge only leads old enough for a deal to have had time to close. A deal that closed
after your export timestamp is still open — **open deals stay in every count.**

Exclude and report: leads that changed reps inside their first week, leads too new to
have had a first week, and leads in an export gap. Say how many you left out and why.

---

## Step 2 — test every candidate habit identically

For each habit (contacted twice, held a meeting, followed up on day three…), compute
the outcome rate on both sides:

- **habit present** → rate A
- **habit absent** → rate B

Then apply the lever test. A habit is a **lever** only when all three hold:

1. The gap `|A − B|` is bigger than **about twice the standard error** (the 95% test).
2. Each side has **at least 20 leads**.
3. The gap holds inside each control stratum before you pool.

If it fails any of these, it is **not a lever**. It may still be worth reporting as an
observation, but it cannot be presented as a lever, and it must not get a bar on a
chart.

**Never assume speed matters.** On a real team, speed to lead came back flat while
the *number of contact days* was strongly predictive. The habit you expect is often
not the habit that pays.

---

## Step 3 — use the right statistics for small counts

With counts in the tens, a naive confidence interval is wrong. Use **Wilson score
intervals** for every rate. Put the 95% range next to the number, always.

**The tie rule.** Two entities are tied when the gap between them is smaller than the
typical entity's standard error on that figure **times 1.4**.

**Never rank inside the tie band.** Publish the threshold and refuse to order tied
entities. If a rep has fewer than **15 wins**, do not rank them at all — flag them
instead. A ranking that separates two reps by less than the noise is worse than no
ranking, because it reads as a fact.

---

## Step 4 — one number per person, and the target must already be hit

Give each person **one** coaching number, not a list:

- the habit whose gap to the team's best is worth the most money over the leads counted
- summed across sources
- benchmarked against **a rate a peer on the same team already hits**

That last part is what makes the coaching actionable: the target is not a number from
a methodology, it is something the person two desks over already does.

Judge closing against what the rest of the team wins from leads with the same
follow-up, leaving that person's own leads out.

---

## Step 5 — the habit-vs-result falsification loop

After you start coaching the habit, watch two numbers weekly, inside one stratum:

1. the habit you asked to change
2. deals won per 100 leads

**If the habit rises and wins do not**, the habit was a proxy for lead quality, not a
cause. Go look at lead quality. Do not push the habit harder.

---

## Step 6 — the report must be able to fail itself

Publish the trip conditions and make the report fail when any of them trips:

- a section missing, renamed, or missing its "what we found" / "what to do" block
- a title or heading containing a number or a conclusion
- any sentence in a finding or action over 30 words
- the text contains: *eligible, denominator, numerator, cohort, censor, conditional
  median, provenance*
- a habit presented as a lever when its gap is inside the chance range
- a chart with (or without) bars for a habit that is not a lever
- any number in the text differing from the numbers file it was computed from
- the same metric showing two different values in the text and a chart
- two entities inside the tie gap ranked against each other

Then render every chart and **look at it**: overlapping labels, a "steady" label
beside a swing over 5 points, and any bar that could be read as advice to do less.

**A diagram can be wrong without any number being wrong.** "Any bar that could be read
as advice to do less" is a failure a numeric check cannot see.

---

## Step 7 — separate data QA from judgement

Reserve one panel for **record completeness** and never let it judge people. Draw
export gaps as hatched cells, never as zero — a missing week is missing data, not
performance. Say "contacted on 2 or more days", never "went back a second day".

---

## Vocabulary rules

- Say **"contacted on 2 or more days"**, not "went back a second day".
- Mark the coaching cell with a fill, never an outline.
- Never write a conclusion into a heading.
- If the output is too clean, check the input.

---

## Where this comes from

Reverse-engineered from a sales-coaching build that graded every rep visually, and
from a post that distilled twelve rules for going from zero to one. The method is
reproduced here in my own words with no numbers quoted from anyone else's run.
