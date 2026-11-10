# Post 007, Substack version

**Title:** A join key is a claim about identity. Make the claim you can defend.
**Subtitle:** Two companies can share a name and a tax ID cannot. Here is how I found out
which one my pipeline was betting on.
**Slot:** Friday framework, deep version. Same facts as the LinkedIn post, told at length.
**Status:** drafted and gated. Needs Asshvin's approval before publishing.

---

There is a question you answer once, at the start of a pipeline, and then never think
about again.

When two datasets describe the same real-world thing, what makes two rows the same row?

If you build lists by joining on company name, you have answered it. If you join on a tax
ID, you have answered it differently. Most of the time nobody writes down which answer
they gave, and the pipeline carries that silent decision into every number it produces.

I want to name the rule that fell out of a real join for me, and give you the test that
produced it.

## The rule

**A join key is a claim about identity. Make the claim you can defend.**

Two companies can share a name. Two companies cannot share a tax ID. So a name makes a
weak claim about identity and a tax ID makes a strong one, and the difference is not
theoretical. It has a count, and the count is large.

## Where the claim came from

I built a play that finds companies for a job seeker. A company that just raised money,
has filed H-1B paperwork before, and is hiring now.

Two public files, joined:

**SEC Form D filings.** Companies that recently raised money. Free, dated, legally required.

**Department of Labor H-1B wage filings.** Every certified Labor Condition Application
names an employer, a job, a wage and a state. Quarterly, free, one 250 MB spreadsheet.

The join needs a key. The employer's name is in both files and is readable without a
second request. The employer's tax ID is in both files too: the SEC filing's SGML header
carries the filer's EIN, and the DOL disclosure row carries the employer's FEIN.

I used the tax ID. Every row in my output records which route produced it, so a reader can
tell which matches are exact and which are inferred.

On the run of 2026-11-08, 23 of the 24 sponsors matched by tax ID and 1 matched by name,
because that filing had no tax ID in its header.

That is a good result. And it taught me nothing, which is the problem with good results.

## The measurement that changed my mind

"I picked the better key" is not an argument. If I am going to claim that names are
worse, I should be able to say what a name-based version of my own pipeline would have
done.

So I built the index the way the pipeline builds it, and then measured the name key
against it.

The index holds 50,307 employers, built from 437,496 disclosure rows, of which 392,175
were certified H-1B applications.

Then I went through the name index and asked, for every name, how many different tax IDs
are stored under it.

**219 names are carried by two or more different tax IDs.**

Two different tax IDs are two different legal entities. So in this index, 219 names do
not identify a company. They identify two or more.

I did not stop at the count, because a count without a consequence is just trivia. A
name index holds one record per name, the way a dictionary holds one entry per word. So
when two tax IDs share a name, one of them is not stored under it.

227 tax IDs are hidden behind a shared name. And 223 of them have no other spelling in
the index that reaches them, so there is no second chance to find them.

The size of that last group is what makes it a real problem. It is not that names
sometimes collide. It is that for a meaningful number of employers, a name lookup returns
a different company and the pipeline has no way to notice.

## The test that produced the rule

Now the part I would actually keep.

I replayed a name-only join across all 24 sponsors from my own run. Not the ones it
caught. All 24.

→ 22 land on the same tax ID the tax ID route found
→ 1 finds nothing at all
→ 1 had no tax ID to compare, because the run matched it by name

Look at that result the wrong way and it is reassuring. 22 of 24, and one more that had no
tax ID to check. That is the number I would have quoted if I had only checked the rows
the fallback handled.

Looked at properly, it says something else entirely. The one name-only match my pipeline
made was correct. Every bit of information about the fallback was in the other 23 rows,
the ones the fallback never got to touch. A pipeline that reports only on what it matched
would never have learned that the fallback drops companies.

The company it dropped is Get Vocal, PBC. The SEC filing says "Get Vocal, PBC". The
Department of Labor says "Get Vocal PBC dba Vocal Media". The `dba` survives
normalization as extra characters, the keys do not match, and the company vanishes from a
name lookup that a tax ID join keeps without effort.

That is the whole rule in one row. The fallback was not wrong. It was silently
incomplete, and it was incomplete in a direction I would never have audited.

## Two things that belong next to it

**Test the fallback across the whole population, not the rows it caught.**

This is the cheapest habit in this whole post and the one I keep forgetting. Running the
alternative key over every row costs one script and one pass over the data. It found a
dropped company in a pipeline I had already called working. I did not find it by reading
the output, because the output looked correct.

**Publish the ceiling with the number.**

My index stops at a decision date of 2026-06-30. The filing window my run covers ends
2026-11-06. That is 129 days, about 4.2 months, where the sponsorship signal cannot see
anything. No employer in the index has a filing after the ceiling.

So "has sponsored before" really means "sponsored before 2026-06-30, observed on
2026-11-08". A company that filed its first H-1B paperwork in September 2026 is not in my
list, and my list cannot tell you it is missing.

This is the same discipline as the key, applied to time. A number without its coverage
window is not a measurement. It is a memory.

## What this means for the work you are doing now

If you build lists for a living, your join key is making a claim about identity on every
row you will ever ship. Sometimes that claim is strong.

A tax ID. A domain. A registration number. A government-issued identifier of any kind.
Those are facts about entities, and facts do not get reused.

Sometimes it is weak.

A company name. A person's name. A city. A job title. Those are labels, and labels get
reused, and when they do, the pipeline either returns the wrong row or drops one.

The test is the same either way, and it is cheap: run the alternative key across every
row of your population and count where it lands. If the alternative also scores well, you
learned nothing and you should say so. If it does not, you have found the number that
should be printed next to your headline.

And the second test, which costs even less: what is the date your data stops? Publish it
with the count, every time.

## What this does not prove

- **I did not ship a name-based version.** I measured what it would have done.
- **22 correct out of 24 is 22 out of 24.** One run, one window.
- **I did not resolve the 219 shared names to legal entities.** I measured the collision.
  Adjudicating who is who is a different job.
- **223 hidden tax IDs have no other name route inside this index.** Whether another
  source reaches them is untested.
- **Nobody has received any of this.** The lists exist and nobody knows.

---

**The audit script, the collision list and the run files are on my site. Link in the
comments.**

If you have a join key you are confident about, I would like to hear how you tested it.
What did you run against, and what did it cost?
