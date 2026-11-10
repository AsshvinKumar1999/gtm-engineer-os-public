# Post 006, Substack version

**Title:** Two companies can share a name. A tax ID cannot.
**Subtitle:** I joined SEC filings to Department of Labor H-1B filings, matched on tax ID,
and then went looking for the companies the name route would have lost.
**Slot:** Wednesday teardown, deep version. Same facts as the LinkedIn post, told at length.
**Status:** drafted and gated. Needs Asshvin's approval before publishing.

---

Every join has a key, and the key is where the whole thing quietly goes wrong.

Mine joins two public files. On one side, SEC Form D filings: companies that recently
raised money. On the other, Department of Labor H-1B wage filings: employers that have
sponsored a worker before, for a named job, at a named wage.

Put them together and you get a specific situation. A company that just raised money, has
done this paperwork before, and is hiring now.

To join them I needed something that identifies a company in both files. There were two
candidates, and one of them is obviously better. I want to show you why I picked it, and
what it would have cost me to pick the other one.

## The key I chose

The tax ID.

The SEC filing's SGML header carries the filer's EIN. The Labor Department disclosure row
carries the employer's FEIN. Both are the same nine-digit tax ID for the same legal
entity. Joining on it is exact, not inferred.

The alternative is the employer's name. It is right there in both files, it is readable, and
it does not need a second request. It is also wrong in a way that does not announce itself.

So I matched on the tax ID. Every row in my output records which route produced it, in a
column called `match`: `EIN` or `name-only`. On the run of 2026-11-08, 23 of the 24
sponsors matched by tax ID and 1 matched by name only, because that filing had no tax ID
in its header.

That is a good result and it taught me nothing on its own. The interesting question is what
the name route would have done, which is a question I had never asked.

## So I asked it

The Department of Labor publishes a quarter of H-1B wage filings at a time. The one I used
covers FY2026 Q3.

I built an index out of it: 437,496 rows read, 392,175 of them certified H-1B
applications, collapsing down to 50,307 employers. Keyed by tax ID, 50,307 entries. Keyed
by normalized employer name, 51,137 entries.

That gap of 830 is the first hint. 830 more name keys than employers means many employers
appear under more than one spelling, which is normal and harmless. 881 employers are
reachable through more than one name.

The number that stopped me was this one:

**219 of the names in the index are carried by two or more different tax IDs.**

Different tax IDs are different legal entities. Two different legal entities, in this
data, carry the same employer name.

## What a shared name does to a lookup

The name index holds one record per name. When two tax IDs share a name, the first one
written wins and the second is not stored under that name at all.

I went back through the index and counted the damage precisely, rather than assuming it.

227 tax IDs are hidden behind a shared name. Of those, 223 have no other name spelling
that reaches them. So for 223 employers in this index, asking the name index for their
company returns a different company, and there is no second spelling to fall back to.

Some of these are ordinary. "Magna Electronics, LLC" and "Magna Electronics, Inc." are two
tax IDs, one with 6 certified filings and one with 33. A name lookup for "Magna
Electronics" gives you the one with 33 filings and the other one is invisible.

Others are more confusing. "AArete, LLC" and "AArete, Inc." carry 3 filings and 1 filing.
"AEVEX Aerospace, LLC" appears under two tax IDs with 1 filing each, and they are not the
same entity, they just have the same name and the same filing count.

The point is not that the data is wrong. The data is the Labor Department's, and it is
accurate. The point is that a name is a label, and labels are not unique.

## Now the part that was about my run

I did not want to argue about the index in the abstract, because a reader has no way to
check a claim about 219 names without the file.

So I replayed a name-only join over all 24 sponsors from my run. Not over the one the
name route happened to catch. All 24.

→ 22 land on the same tax ID the tax ID route found
→ 1 finds nothing at all
→ 1 had no tax ID in its filing to compare against, because the run itself matched it by name

Zero land on a different tax ID. I want to be precise about that, because it is the part
that makes this less dramatic than it sounds. On this particular run of 24 companies, the
name route would not have handed me a wrong company. It would have quietly dropped one.

That one is Get Vocal, PBC.

The SEC filing says "Get Vocal, PBC". The Labor Department employer name is "Get Vocal
PBC dba Vocal Media". The DBA suffix means the normalized keys do not match, so a name
lookup finds nothing. The tax ID in the filing header finds the company perfectly well.

So the honest summary of the name route is not "it produces wrong answers". It is "it
produces wrong answers at a rate you cannot observe, and it drops companies at a rate you
can." Twenty-three of 24 is a good hit rate on 24 rows and it hid a defect entirely.

There is also this, which I found while checking the 10 sponsors whose DOL employer name
differs from their SEC company name. Ten of my 24 sponsors are filed under a different
name at the two agencies. The tax ID says they are the same entity. The names do not, and
they cannot be made to.

## The ceiling I have to publish with the number

One more thing, and it is the reason the audit exists at all.

The index covers a quarter of filings. The newest decision date anywhere inside it is
2026-06-30. The filing window my run covers ends 2026-11-06.

That is 129 days, about 4.2 months, where the sponsorship signal cannot see anything. No
employer in the index has a filing after that date.

So "has sponsored before" means "sponsored before 2026-06-30, as of a run on 2026-11-08".
A company that filed its first H-1B paperwork in September 2026 is not in my list, and my
list will never say so.

I would rather a reader knew that up front. A number without its ceiling is a memory, and
I have no interest in publishing memories.

## What I learned

**A name is a label. A tax ID is a fact.** 219 labels are shared across those 50,307
employers. Not one tax ID is shared.

**A fallback that returns a plausible wrong answer is the dangerous kind.** Mine returned
the right company 23 times out of 24 and dropped one. I would not have found that by
looking at my output, because the output looked right.

**Test the fallback over the whole population, not the rows it caught.** The one name-only
match in my run was correct. The other 23 are where the information was. I replayed the
name join across all 24 sponsors and that is the only reason I know anything about it.

**Publish the ceiling with the number.** 129 days of blind spot is a fact about my
pipeline, not a footnote.

## What this does not prove

- **I did not ship a name-based version.** I measured what it would have done. I did not
  build one and compare results.
- **Zero wrong answers on 24 rows is not zero wrong answers.** It is 24 rows.
- **The 91 raw-name collisions and the 219 normalized-name collisions are different
  counts.** One is before normalization, one after. I have not mapped which legal entities
  sit behind each shared name.
- **I did not verify the 10 differently-named sponsors by hand.** The tax ID carries the
  match; the names do not support it.
- **This audit measures the index on disk.** A fresher quarter would change the ceiling.

---

**The audit script, the collision list and the run files are on my site. Link in the
comments.**

If you have hit a name collision in a join and found a way around it, I would like to read
it. What did you key on instead?
