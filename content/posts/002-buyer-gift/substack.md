# Post 002, Substack version

**Title:** 18 companies just raised $1.9B. Here is who each one is hiring.
**Subtitle:** I ran one playbook five times with five different buyer signatures. The
overlap is the interesting part.
**Slot:** Monday build log, deep version. Same facts as the LinkedIn post, told at length.
**Status:** drafted. Needs Asshvin's approval before publishing.

---

Most job applications are a monologue. You tell a company what you built. They tell you
nothing back. You wait, and you apply to the next one.

I have been doing this the wrong way for a while, so I built the other thing: a way to
arrive at a hiring manager with something useful already in hand.

Not a cover letter. A list.

## The idea

I wanted to walk into a conversation with Baseten and say: here are eleven companies that
raised money in the last month and are hiring machine learning engineers. You sell
inference. Those are your buyers.

That is only worth anything if the list is real, recent, and something they could not
easily have built themselves. Which meant the data had to be free, dated, and hard to
fake. I went looking for the public records that satisfy that.

There are exactly two I needed.

**SEC Form D.** When a private company raises money in the United States, it has to file a
short notice with the SEC. It is a legal requirement, it is free to read, and it contains
a date, a dollar amount, and the state. A company that files one has told the government
it just raised money. It cannot bluff that.

**Live job posts.** Every serious company posts roles on Greenhouse, Lever or Ashby, and
all three have free public APIs. No login, no scraping behind a wall, no sales tool.

Put the two together and you get something specific: **money says they can buy. A job
post says what they are trying to fix.** Both in the same window is a real buying
reason. Either one alone is just noise.

## What the run actually returned

I ran 30 days of Form D filings, from 2026-10-10 to 2026-11-08.

3,251 filings
→ 1,089 companies, after removing funds, SPVs and other pooled vehicles that file the same
form because they are legally required to
→ 297 technology companies, one row per company
→ 27 of those with a job board I could locate by company name or slug
→ 719 open roles
→ 12 companies that both raised and are hiring for a GTM role

That last number is the one that matters. 12 out of 1,089. The filter is doing the work.

Then I ran it five more times. Same filings, same job boards, but each run scored roles
against a different buyer signature, because each of the five companies I care about
sells something different:

| Company | What they sell | The signature I looked for | Matches |
|---|---|---|---|
| Baseten | Inference | ML, AI and inference engineers | 11 |
| Bluejay | Evals for voice and text agents | Voice, AI, NLP and agent engineers | 9 |
| Nectar | Community-led growth for consumer brands | Community, social, brand and growth roles | 9 |
| Wispr Flow | Dictation and meeting notes | Sales teams: AE, SDR, BDR, RevOps | 9 |
| FlowGen Labs | GTM engineering for mid-migration companies | SAP, ERP and systems roles | 6 |

44 matches. 231 live job posts behind them.

## The part that took the most work: deduplication

44 is not the number I would put in a post, and this is where I nearly got it wrong.

Five lists, 44 rows. But Legora appears in all five. Modal Labs appears in four. Factored
appears in four. Commure appears in all five.

One company is one buyer, no matter how many of my filters it happens to match. Dedupe by
name and 44 becomes **18 unique companies**.

And those 18 companies raised a combined **$1,908,732,450** in the window.

That number stopped me, because of how a company like Modal Labs looks. It raised
$601,892,375 on 2026-10-20 and is now hiring Forward Deployed Engineers for ML in New York
and London. One public filing shows up in four of my five lists because Modal Labs is
simultaneously a plausible buyer of inference, of agent evals, of growth and of migration
tooling. The overlap is not a bug in the filter. It is the signal.

## The honesty problem, which is the actual problem

Here is where I could have made this post look better than the work is.

Every company above matched a job board by one of two methods. Greenhouse boards let you
confirm the company name, so I could tell you this board really is Baseten's. Ashby and
Lever match by URL slug, which means I inferred the company from its slug.

6 of my 44 matches are name-verified. The rest are slug-matched.

Both are worth sending. A slug match is a lead. A name match is a fact. But a reader
deserves to know which one they are holding, so every sheet labels every row with the
match method. If I had not labelled them, the list would have looked twice as certain
than it is, and that is exactly the kind of overstatement that ends a working
reputation.

Two more limits worth stating plainly:

**27 out of 297.** Only a quarter of the tech companies had a job board I could find by
slug. The other 270 are not companies that did not raise and did not hire. They are
companies whose board I could not locate. I am not going to pretend the difference is
meaningful.

**I did not send any of this.** The lists exist. Nobody has received one. The first email
is still ahead of me, and until one lands I have not proven that a hiring manager wants
this.

## Why I built it this way

The whole thing runs on the Python standard library. No API keys, no paid data, no
account, no scraping anyone is hiding. The SEC asks for a contact in the user agent and
stays under ten requests a second, and the script does both.

It takes about six minutes to run, most of it waiting on the SEC.

The point was never the code. The point is that the code gives me something to hand over
that a candidate cannot fake, because the list is checkable by the person receiving it.
Every row links to the filing on sec.gov. Every row links to a live job post. If I am
wrong, they can see exactly where.

## What I would do differently

I would widen the window before I narrow the signature. I spent a long time tuning the
role regexes when I should have run 60 days and let the buyer signature do the filtering.

I would also keep the first list I built. When I started, the first version asked "who
raised and hired a GTM role", which is a list of my peers. It is a fine list. It is also
useless to a hiring manager, because they already know their peers. The moment I
inverted the question to "who raised and hired a role that this specific company sells
into", the list became something a person could actually use.

That inversion is the whole trick. Most outbound asks a seller "do you want to buy". This
one hands over the evidence that somebody else does.

---

**The play, the five sheets and the source code are on my site. Link in the comments.**

If you have ever sent a hiring manager a list instead of a pitch, I want to read it.
What did you send, and did they reply?
