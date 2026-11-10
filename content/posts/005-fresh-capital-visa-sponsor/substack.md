# Post 005, Substack version

**Title:** 8 companies just raised money, hired H-1B workers before, and are hiring now
**Subtitle:** I joined three free public sources and ran them over 30 days of SEC filings.
Here is what came back, and the part I did not expect.
**Slot:** Monday build log, deep version. Same facts as the LinkedIn post, told at length.
**Status:** drafted and gated. Needs Asshvin's approval before publishing.

---

Every job application is a monologue. You tell a company what you built. They tell you
nothing back. You wait, and you apply to the next one.

The thing I kept coming back to was a question I could not answer with the tools I had.
Not "who is hiring" or "who is growing". Something narrower:

**Which companies that just raised money have hired an H-1B worker in this kind of job
before, and are hiring for it right now?**

That is a specific situation, not a filter. And if it is answerable from public records,
then it should be answerable for free.

## The three signals

A situation this narrow needs three separate pieces of evidence, each from a source that
is forced to publish.

**SEC Form D.** When a private US company raises money it files a short notice with the
SEC. It is legally required, it is free to read, and it carries a filing date and a dollar
amount. A company that files one has told the government it just raised money. It cannot
bluff that.

**Department of Labor H-1B wage filings.** Before an employer can sponsor an H-1B worker,
it files a Labor Condition Application stating the job and the wage it intends to pay. The
Department of Labor publishes every one of these, quarterly, as a free spreadsheet. An
employer that appears in that file has done this before, in a specific job, at a specific
wage. This is the signal most people never open, because it arrives as a 250 MB Excel file
with a quarter's worth of rows.

**Live job posts.** Greenhouse, Lever and Ashby all publish their job boards through free
public APIs. No login, no scraping behind a wall, no sales tool.

Join the three and you get a company whose money is fresh, whose paperwork shows they
already know this process, and whose job board shows the role open today.

One important precision before I go further. A certified wage filing is a first step. It
shows the company was ready to sponsor. It is not a granted visa, and I do not claim it is.

## What the run actually returned

I ran it on 30 days of SEC filings, 2026-10-08 to 2026-11-06. The run happened on
2026-11-08.

3,673 Form D filings
→ 1,203 operating companies, after removing the funds, SPVs and pooled vehicles that file
the same form because they are legally required to
→ 328 technology companies, one row per company
→ 24 of those had filed H-1B wage paperwork before
→ 8 of the 24 had a job board I could find
→ 563 open roles on those boards
→ 55 of those roles look like the work the company had sponsored before

Every one of those numbers is read from the run files. I have not rounded any of them into
something more flattering.

Then I did the part that took the longest, which was checking things by hand.

I opened all 8 job boards. I checked the company name and the locations on the board
against the SEC filing behind the match. That last step mattered more than it sounds:
Play 01 matched all 8 boards by URL slug, not by a name the board itself confirmed, and a
slug match is a lead rather than a fact. So I confirmed all 8 by hand.

## The part I did not expect

A run is easy to get wrong in a way that flatters you. I went looking for that.

The 55 roles "similar to what they sponsored before" sounded like a good spread across a
market. It was not.

**42 of the 55 came from two companies.** Commure, with 24 roles, and Modal Labs, with 18.
That is 76.4% of the number from two employers out of 8. If I had posted "55 open roles at
companies that sponsor H-1B workers", the number would have been true and the picture would
have been a lie.

So I looked closer at Modal's 18. Thirteen of them matched on one single sponsored title:
"Member of Technical Staff". Roles like "Member of Technical Staff, Research, Inference"
and "Member of Technical Staff, Platform Engineering" and "Member of Technical Staff,
Storage, Stockholm". All 13 of those roles share two or more meaningful words with the
same generic sponsored title, and my similarity test treats that as a match.

That is a real weakness in the test, not a rounding error. A generic sponsored title will
match a whole company. I would rather tell you that than let the 55 stand.

There is a second, sharper version of the same point in the other direction. Legora had 318
of the 563 open roles on those boards and only 3 of them were flagged as similar to what it
had sponsored. The company with the most open roles is not the company whose roles look
like its own history. Volume of postings is not relevance.

## Two more things the run would have let me hide

I did not want to publish this without them.

**Half the list is thin.** 12 of the 24 sponsors have exactly one certified filing behind
them. One filing is a fact. It is not a track record. 8 of the 24 have four or more. I am
telling you the distribution because a list of 24 reads very differently when you know 12
of them are a single form.

**16 of the 24 had no job board I could find at all.** This one is worth pausing on, because
it is easy to misreport. Play 01 found a job board for only 30 of the 328 tech companies
in the window. So "no open roles found" for those 16 does not mean they are not hiring. It
means I could not find their board. A slug-based lookup against three ATS platforms misses
any company that posts elsewhere, which is most companies. I wrote a separate post about
that one, because it is the kind of limit that quietly turns into a false claim.

## Why I built it this way

The whole thing runs on the Python standard library. No API keys, no paid data, no
account. The two dependencies you would otherwise need, reading a quarter's Excel file and
fetching a lot of URLs, are handled by a calendar package and a thread pool.

The SEC asks for a contact in the user agent and asks you to stay under ten requests a
second. The script does both. The Department of Labor asks for a contact in the user agent
too, for the same reason: the file is 250 MB and they would rather you did not hammer
them.

The point was never the code. The point is that the output is something a recipient can
check without trusting me. Every sponsor in the CSV carries the tax ID the match was made
on, the number of certified filings behind it, the date of the last decision, and the
titles they sponsored for. If a row is wrong, you can see exactly which field is wrong.

## What I would do differently

I would measure the concentration of every match group before I publish the headline. I
did not, and I found out because I went looking. The rule I am keeping is simple: before
a filtered count goes in a post, check how many entities it is really spread across.

I would also make the similarity test stricter about generic titles. Right now "Member of
Technical Staff" will match anything with "technical" and "staff" in it. Requiring a
distinctive word, not just two words, would have flagged those 13 rows on their own.

And I would go looking for job boards beyond three ATS platforms sooner, because 16 of my
24 sponsors are invisible to me for a reason that has nothing to do with their hiring.

## What this does not prove

- **Nobody has received this list.** It exists. Nobody knows it exists.
- **A filing is not a visa.** The index stops at a decision date of 2026-06-30, so a company
  that filed H-1B paperwork after that date is not in this list at all.
- **The 55 roles are a similarity score, not a match.** Two overlapping words is a weak
  signal, and 13 of them are one generic title.
- **The 8 boards were all slug matches.** I checked them by hand. An automated rerun would
  not have that check.

---

**The play, the run files and the source code are on my site. Link in the comments.**

If you have applied to a company that sponsors H-1B workers, I would like to hear how it
went. Did the sponsorship actually happen, or did it stall somewhere?
