---
name: non-us-data-map
description: Build the public-data stack for a non-US market using the same compelled-disclosure method as the US shelf — registries, licences, filings and tenders — then publish coverage, freshness and cost per usable row. Use when a target market is outside the US, when a list does not exist for a country, or to build the defensible version of an international play.
---

# Non-US Data Map

The US shelf works because someone was legally forced to publish. That force is
jurisdiction-specific, but the force exists almost everywhere. This skill is the
method for finding it outside the US — and for turning a list of sources into a
published, auditable pipeline rather than a folder of links.

**Why this is worth doing:** the US registries (NPI, OSHA, Form D, FAA, 5500) are
the most crowded lane in public-data GTM. The map of a country that nobody has
mapped is a category of one that cannot be copied by adding a filter.

---

## The method, in the same shape as the US shelf

### 1. Ask who was compelled to publish

The question does not change by country. It changes its *answers*.

| Trigger | What gets published | Who publishes it |
|---|---|---|
| Incorporation | company master data, directors, filings | Registrar of Companies |
| Selling to government | tender awards, bidder lists | Public procurement portal |
| Selling to regulated buyers | licence and registration lists | Sector regulator |
| Hiring | vacancies, headcount signal | Job boards + company sites |
| Importing / exporting | shipment and licence data | Customs authority |
| Paying tax | tax registration, filings | Tax authority |
| Receiving government money | subsidy and scheme beneficiaries | Scheme portals |

### 2. Rank by the same ladder

Same rungs as the US shelf — a government registry with a unique ID is the top,
a scraped aggregator is a lead and never a source of truth. The join key quality
is what separates them, and it is the thing most worth checking first: **does the
registry give you a stable ID, or only a name?**

### 3. Publish the four numbers nobody publishes

This is the actual deliverable. Any country has sources; almost nobody publishes:

1. **Coverage ceiling** — how much of the market your pipeline can see at all.
2. **Freshness distribution** — the age of each record, not a single "last updated".
3. **Cost per usable row** — total spend ÷ rows that survive your filters.
4. **The deletions** — how many rows were dropped and why.

A pipeline that prints only what worked has told you nothing about its own reach.

---

## India: the worked example

This is the lane with the most headroom and the most accessible data. Everything
below is free, public, and legally published.

### The stack

| Source | What it is | Join key | Notes |
|---|---|---|---|
| **MCA Company Master Data** (RoC-wise) via data.gov.in | Every company registered with the Registrar of Companies | **CIN** (15 chars) | ~3.74M companies. Government Open Data License – India (GODL): reuse and republish allowed with attribution. Free API key on data.gov.in. Paginated pull. |
| **FoSCoS** (FSSAI) | Every licensed and registered food business | 14-digit licence number | Licensing is mandatory under Section 31 of the FSS Act 2006, so this is a compelled list. Three tiers — Central, State, Registration — each with a different turnover threshold and fee, so the tier itself is a size signal. |
| **Udyam** (MSME) | Every registered MSME | Udyam Registration Number | Free official registration. Marks a business as an MSME, which is a firmographic you can query rather than guess. |
| **GeM** (Government e-Marketplace) | Every government buyer and their tender awards | GeM supplier ID + tender ID | The buyer side of every government purchase, with the bid documents. |
| **State RERA** | Every real-estate project registered with a state authority | state + project ID | State-by-state, so the join key is a composite. |
| **CDSCO / Medical Device** | Every licensed medical device and importer | licence number | Import and licensing data. |
| **SEBI / BSE-NSE** | Every listed company and its filings | ISIN / scrip code | The public-market subset — useful as a signal, not as coverage. |
| **GSTN** | Tax registration | GSTIN (15 chars) | Validate a GSTIN offline by checksum — no keyless public search API exists, so state the fields you cannot confirm rather than guessing them. |
| **DGFT IEC** | Every import-export code holder | IEC number | |

### The shape of the pipeline

```
registry pull (free, paginated, checkpointed)
  → deterministic extraction (code, no model)
  → identity audit (name collisions, ID joins)
  → coverage + freshness + cost published
  → only then: the list
```

The **identity audit** is not optional. Companies with similar names collide, and a
list that treats two companies as one is worse than a smaller honest list. Publish
the collision table.

### What is already out there (so you do not rebuild it)

- `india-company-diligence` — an MCP server with a full local MCA mirror (~3.74M
  companies), offline CIN decoding and GSTIN validation, provenance per field.
  **Verification framing, not list building.** Its mirror is the fastest way to get
  the data; build the *GTM list layer* on top.
- `indian-bizverify-mcp` — KYB verification over CIN/GST/PAN/Udyam via free
  government APIs.
- `getregdata` — skills per jurisdiction; the UK front door is free, others paid.
- `OpenRegister` — Germany, positioned for lead generation.
- Kaggle mirrors of the MCA dataset — cleaned samples, not the full file.

**The gap is the list layer:** a registry pull turned into a *prospect list* with a
published coverage ceiling, a freshness distribution, and cost per usable row.
Everyone has built the mirror. Nobody has published the outbound artifact.

### Where the joins break

- **CIN carries the state and the year.** A CIN is not opaque — the state code and
  the incorporation year are embedded in it. That makes it a filter, not just a key.
- **Legal status lives in the master data, not the name.** A company named "Acme
  Private Limited" may be struck off. Filter on status, not on the word "Private".
- **GSTIN validation is offline-only by design.** There is no keyless public GST
  API. If a field cannot be confirmed, mark it missing rather than inferring it.
- **Tier is a size signal.** FoSCoS Central vs State vs Registration maps to
  turnover bands (Rs. 30 Cr / Rs. 12 L). That is a firmographic for free.

---

## UK and EU

| Source | What it is | Join key | Notes |
|---|---|---|---|
| **Companies House PSC** (UK) | Every company and its persons with significant control | Company number | Free, public, machine-readable. The PSC register is the ownership layer — the answer to "who actually controls this company". |
| **Companies House filing history** | Every filing, dated | Company number | Gives you a dated event stream per company: accounts, officers, charges, insolvency. The UK equivalent of a filing-driven signal. |
| **MaStR** (Germany) | The German business register | register number | National, machine-readable. |
| **Handelsregister** (DE) | Company register | register number | |
| **European EBR / Business Registers** | Cross-border company data | LEI + national ID | |

The **PSC** point is the transferable one: in the UK, ownership is a compulsory
disclosure with a machine-readable identifier. That is a "who actually controls this
company" answer you can get for free and at scale — and it is the same *shape* as
the US beneficial-ownership layer.

---

## Rules that keep this honest

1. **License check first, per source.** GODL allows commercial republication with
   attribution; some registries do not allow it at all. Note the license next to
   the source before you build on it. Non-commercial = banned for client work.
2. **`as_of` is a date the record states.** Never inferred. In India the MCA
   dataset carries its own update date; stamp it, do not guess it.
3. **Never let an auth error look like empty data.** A missing API key sent as an
   empty string returns an error on every call, and inside a try/except that reads
   as "no results found" for the entire run. Assert auth once, fail loud.
4. **A mirror is a mirror.** Label `provenance_type` for every row:
   `original` | `official_mirror` | `scrape_snapshot` | `derived` | `unknown`.
   Only the first two may be asserted as fact.
5. **Measure the filter before you spend.** Print the survivor count after each
   filter. If a free prefilter leaves more than 100k rows, the filter is broken.
6. **Do not guess a join key.** A name join across a country registry will collide.
   Where the registry gives an ID, use the ID. Where it does not, say the list is
   name-matched and publish the collision rate.

---

## The deliverable

Not a folder of links. A **published map**:

| Source | Rung | Join key | Coverage | Access | Cadence | Cost | Gotchas | Dead end? |
|---|---|---|---|---|---|---|---|---|

plus, for the pipeline you actually run:

- the coverage ceiling
- the freshness distribution
- the cost per usable row
- the count of rows deleted and why

That is the artifact nobody in the market publishes, and it is the thing that makes
the map defensible when someone copies your list.

---

## Where this came from

Most public-data projects outside the US are built for *verification*: checking one company at a time. Few are built for *list building*, with published coverage, freshness and cost per usable row. This skill fills that gap. It extends `skills/data-source-hunter/` and `METHOD.md`.
