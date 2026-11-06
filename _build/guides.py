# Brand.Life guides — original long-form content (Markdown). Edited by hand; build.py renders them.
GUIDES = []


def G(slug, title, desc, cat, minutes, body, tool=None):
    GUIDES.append({"slug": slug, "title": title, "desc": desc, "cat": cat, "min": minutes, "body": body.strip(), "tool": tool})


G("what-is-a-brand", "What Is a Brand? The Plain-English Guide to Branding",
  "A brand is the gut feeling people have about you. Learn the parts of a brand, how they work together, and where to start building one.",
  "Foundations", 9, """
Ask ten people what a brand is and you'll hear "a logo", "a reputation", "a promise" and "marketing". They're all describing one piece of the same thing. The working definition we use at Brand.Life is simple:

> **A brand is the set of expectations people carry about you — and the feeling those expectations create.**

Your logo, name, colors and ads are signals. The brand is what forms in someone's head after they've received those signals and, more importantly, after they've *experienced* you. That's why two coffee shops with equally nice logos can have wildly different brands: one remembers your order, the other loses it.

## The five layers of a brand

Think of a brand as five layers stacked from the inside out. Most small businesses start at layer four (the logo) and wonder why it doesn't work. Strong brands start at layer one.

1. **Purpose** — why you exist beyond making money. This doesn't have to be world-changing. "Make weeknight dinner less stressful" is a perfectly good purpose.
2. **Positioning** — who you serve, what you do for them, and why you instead of the alternatives. This is the strategic core.
3. **Personality** — how you sound and behave: your voice, values and archetype.
4. **Identity** — the visible system: name, logo, color, typography, imagery, packaging.
5. **Experience** — every touchpoint: the website, the checkout, the support email, the unboxing, the invoice.

Each layer should be a consequence of the one beneath it. If your positioning is "the calm, expert choice for first-time home buyers", a neon, all-caps identity contradicts it, and customers feel the mismatch even if they can't name it.

## Brand vs. branding vs. marketing

These three words get blended, so it helps to separate them:

| Term | What it is | Example |
|---|---|---|
| Brand | The perception in people's minds | "They're the reliable ones" |
| Branding | The deliberate work of shaping that perception | Choosing a name, writing a voice guide |
| Marketing | Activities that reach people and drive action | Ads, email, content, promotions |

Marketing gets attention. Branding makes the attention *add up* — so that every ad, post and conversation compounds instead of starting from zero.

## Why branding pays

Branding is sometimes treated as a cosmetic expense. The numbers say otherwise. Recognized brands can charge more for comparable products, convert better on search because people click names they know, and spend less to win back customers. In Interbrand's 2025 Best Global Brands ranking, the combined value of the top 100 brands reached roughly $3.6 trillion — brand value counted as a business asset, separate from factories or cash.

For a small business, the payoff is more concrete:

- **Higher conversion.** A visitor who recognizes you is more likely to buy on the first visit.
- **Pricing power.** Clear positioning lets you stop competing on price alone.
- **Lower acquisition cost.** Referrals and direct searches are cheaper than ads.
- **Easier hiring.** People want to work for brands they understand and respect.

## Where to start (in order)

1. **Write one sentence of positioning.** Use the template: *For [audience] who [need], [brand] is the [category] that [benefit]. Unlike [alternative], we [difference].* Our [Positioning Builder](../tools/positioning-statement.html) walks you through it.
2. **Pick three personality words** — and three words you are *not*. "Confident, warm, precise — not loud, not cute, not corporate."
3. **Check your name.** Can people spell it after hearing it once? Is the domain available? Run it through the [Name Tester](../tools/name-tester.html).
4. **Build a minimum identity.** One logo lockup, two to four colors, two typefaces. Generate a starting palette with the [Color Palette Generator](../tools/color-palette.html).
5. **Fix your top three touchpoints.** For most businesses that's the homepage, the Google Business Profile and the first email a customer receives.
6. **Write it down.** A one-page style guide stops your brand drifting the moment someone else starts making content. Use the [Style Guide Builder](../tools/style-guide-builder.html).

## Common mistakes

- **Designing before deciding.** A logo can't fix unclear positioning.
- **Trying to appeal to everyone.** A brand for everyone is memorable to no one.
- **Changing too often.** Consistency is how recognition forms. Most audiences notice your brand long after you're bored of it.
- **Copying the category leader.** Looking like the leader makes you the cheaper alternative by default.

## The bottom line

A brand isn't something you finish. It's alive: it's born, it grows, it matures and it sometimes needs renewal. That's the idea behind our [Brand Life Cycle](brand-life-cycle.html) framework — read it next to find out which stage your brand is in and what to focus on now.
""", tool=("brand-health-score", "Score your brand in 5 minutes"))

G("brand-life-cycle", "The Brand Life Cycle: 5 Stages Every Brand Goes Through",
  "Spark, Launch, Grow, Scale, Renew — a practical framework for knowing what your brand needs right now, with the metrics and mistakes for each stage.",
  "Strategy", 11, """
Products have life cycles; so do brands. The difference is that a brand can be renewed indefinitely — Lego, Old Spice and Apple each came back from decline by renewing their brands rather than replacing them. The Brand Life Cycle is the framework we use across Brand.Life to answer one question: **what should you be working on now?**

There are five stages. Most brands spend years in one or two of them. The mistake is doing the work of a different stage — polishing a logo when you have no customers, or running awareness ads when nobody understands what you sell.

## Stage 1 — Spark (idea to first sale)

**Goal:** prove that a specific group of people wants what you offer.

At this stage your brand is mostly a hypothesis. You need a working name, a clear one-sentence promise and something that looks credible — not a finished identity system.

- **Do:** write your positioning sentence, test two or three names, buy the domain, build a one-page site, talk to 20 potential customers.
- **Don't:** spend weeks on a logo, print merchandise, or register trademarks in ten countries.
- **Metric that matters:** conversations that end with "how do I buy this?"

## Stage 2 — Launch (first customers to repeatable sales)

**Goal:** make the brand recognizable and trustworthy enough that strangers buy.

Now the identity matters, because strangers judge you in seconds. You need consistency across your site, social profiles and packaging, plus proof: reviews, testimonials, case studies.

- **Do:** finalize the logo and palette, write a voice guide, collect your first ten reviews, set up a simple newsletter.
- **Don't:** chase every channel. Choose one or two where your audience already spends time.
- **Metric that matters:** conversion rate from first visit, and percentage of customers who arrive by referral.

## Stage 3 — Grow (repeatable sales to category presence)

**Goal:** become a name people search for, not just a business they stumble across.

This is where content, partnerships and community do the heavy lifting. Your brand should own a specific idea in the category — "the fastest", "the friendliest", "the one for beginners".

- **Do:** publish on a schedule, build a referral program, run contests and collaborations, track branded search volume.
- **Don't:** dilute the brand with off-strategy products because a few customers asked.
- **Metric that matters:** branded search growth and share of search (your branded searches divided by all branded searches in your category).

## Stage 4 — Scale (category presence to market leadership)

**Goal:** protect consistency while many more people — staff, agencies, partners — touch the brand.

Brands rarely fail at this stage from lack of attention; they fail from fragmentation. Ten teams interpret the brand ten ways.

- **Do:** create a full brand guidelines document and asset library, train new staff, introduce brand-architecture rules for sub-brands, register trademarks in key markets.
- **Don't:** let every new product invent its own look.
- **Metric that matters:** consistency audits and brand-tracking measures such as awareness, consideration and Net Promoter Score.

## Stage 5 — Renew (maturity to reinvention)

**Goal:** stay relevant without discarding the equity you've built.

Every brand eventually feels dated, or the market shifts under it. Renewal ranges from a light refresh (updated typography and photography) to full repositioning.

- **Do:** audit what customers still value, keep your most recognizable assets (a color, a shape, a sound), change what has gone stale, and communicate *why* you've changed.
- **Don't:** throw away distinctive assets just because the team is tired of them. Gap's 2010 logo change was reversed within about a week after customer backlash — a reminder that recognition belongs partly to customers.
- **Metric that matters:** retention of recognition after the change, and lift in consideration among younger or new audiences.

## How to tell which stage you're in

| If this is true… | You're probably in… |
|---|---|
| You have no paying customers yet | Spark |
| Customers mostly come from people you know | Launch |
| Strangers buy, but few search for you by name | Grow |
| Many people create content for the brand | Scale |
| Sales are flat and the brand feels old | Renew |

Brands can also be in two stages at once — for example, a mature company launching a new sub-brand is in Scale for the parent and Spark for the new product. Treat them separately.

## Use the framework

Take the [Brand Health Score](../tools/brand-health-score.html) to see which of the five brand dimensions is weakest, then use the stage table above to choose your next three actions. If you want a second opinion, request a [free brand audit](../audit.html) — we'll tell you which stage we think you're in and what we'd do in the next 90 days.
""", tool=("brand-health-score", "Find your weakest brand dimension"))

G("brand-strategy-template", "How to Write a Brand Strategy (Free One-Page Template)",
  "A brand strategy fits on one page. Here are the nine questions it must answer, a fill-in template, and a worked example.",
  "Strategy", 10, """
A brand strategy is not a 60-slide deck. It's a short set of decisions that tells everyone — designers, writers, salespeople, you on a tired Tuesday — how the brand should show up. If it doesn't fit on one page, it's probably not decided yet.

## The nine questions

1. **Purpose — why do we exist?** One sentence, no buzzwords.
2. **Audience — who exactly do we serve best?** Name a segment specific enough to picture: "independent physiotherapy clinics with 2–10 staff", not "healthcare".
3. **Problem — what are they struggling with?** In their words, not yours.
4. **Promise — what do we reliably deliver?** The outcome they get, not the feature list.
5. **Proof — why should anyone believe us?** Numbers, credentials, customer results, guarantees.
6. **Difference — why us and not the alternative?** Include "do nothing" and "do it themselves" as alternatives.
7. **Personality — how do we behave?** Three words we are, three words we are not.
8. **Message — what do we say first?** A headline-level summary of the promise.
9. **Measures — how will we know it's working?** Two or three numbers you'll actually check.

## The one-page template

Copy this into a document and fill it in. Leave anything you can't answer blank — the blanks are your homework.

| Section | Your answer |
|---|---|
| Purpose | We exist to… |
| Audience | We serve… |
| Problem | They struggle with… |
| Promise | We help them… |
| Proof | We can prove it because… |
| Difference | Unlike…, we… |
| Personality | We are… / We are not… |
| Message | Our headline is… |
| Measures | We'll track… |

## A worked example

Here's how a fictional company — *Northbeam*, a bookkeeping service — might fill it in:

- **Purpose:** Give small-business owners their evenings back.
- **Audience:** Owner-operated trades businesses (plumbers, electricians, builders) with $250k–$2M revenue.
- **Problem:** "I'm great at the job but drowning in receipts, and my accountant only calls at tax time."
- **Promise:** Clean books every month, with a 15-minute call that tells you exactly where your money went.
- **Proof:** Fixed monthly price, 48-hour response guarantee, testimonials from 40 trades businesses.
- **Difference:** Unlike general accounting firms, we only serve trades, speak plainly and price monthly with no surprises.
- **Personality:** Straight-talking, organized, reassuring — not stuffy, not salesy, not cutesy.
- **Message:** "Books done. Evenings back."
- **Measures:** Lead-to-client conversion, referral share, monthly churn.

Notice what the example avoids: words like *innovative*, *quality* and *solutions*. Every line is something a competitor would have to work to copy.

## Testing your strategy

A strategy is a hypothesis until customers react to it. Three quick tests:

- **The swap test.** Replace your brand name with a competitor's. If the strategy still reads true, it isn't differentiated.
- **The bar test.** Explain your promise to a friend in under 15 seconds. If they ask "so what?", the promise is about you rather than them.
- **The customer test.** Show the message to five real customers. Ask what they'd expect to get. Compare their answer with your promise.

## Turning strategy into action

Once the page is filled in, three things should follow immediately:

1. Rewrite your homepage headline and subhead from the **Message** and **Promise** lines.
2. Brief any designer using the **Personality** line and your [style guide](../tools/style-guide-builder.html).
3. Set up the **Measures** in whatever tool you already use — even a spreadsheet works.

Need help pressure-testing yours? Our [free brand audit](../audit.html) reviews your strategy against your website and social presence and sends back the three biggest gaps.
""", tool=("positioning-statement", "Build your positioning statement"))

G("how-to-name-a-brand", "How to Name a Brand: A 7-Step Process That Actually Works",
  "Generate, filter, test and protect a brand name — including the radio test, domain strategy and basic trademark screening.",
  "Naming", 10, """
Naming is the branding task people dread most, mainly because it feels like waiting for inspiration. It isn't. Good names come from a process: generate a lot, cut ruthlessly, test with real people, and check the legal and digital basics before you fall in love.

## Step 1 — Write a naming brief

Before brainstorming, answer five questions:

- What should the name **suggest** (speed, calm, craft, scale)?
- What should it **avoid** (sounding cheap, sounding like a bank)?
- Where will it **live** (app icon, storefront sign, spoken on podcasts)?
- Which **markets and languages** matter?
- How much **room to grow** do you need? "Toronto Dog Walkers" boxes you in; "Leashly" doesn't.

## Step 2 — Know the name types

| Type | Example style | Strength | Trade-off |
|---|---|---|---|
| Descriptive | "Quick Plumbing" | Instantly clear | Hard to trademark, forgettable |
| Suggestive | evokes a benefit | Clear but ownable | Needs some explaining |
| Compound | two real words joined | Memorable, flexible | Domain often taken |
| Invented | new coinage | Highly ownable | Costs more to build meaning |
| Founder / place | a surname or city | Personal, heritage | Can limit scale or sale |
| Metaphor | an unrelated real word | Distinctive story | Requires consistent storytelling |

Suggestive and compound names are the sweet spot for most small businesses: understandable on day one, distinctive enough to protect.

## Step 3 — Generate at least 100 options

Volume beats genius. Mix methods:

- Word lists around your benefit, audience and feeling
- Blends and compounds ("Pin" + "Interest")
- Prefixes and suffixes (-ly, -ify, -io, go-, get-)
- Foreign-language and Latin roots (check meanings carefully)
- Metaphors from nature, craft, travel or science

Our [Brand Name Generator](../tools/name-generator.html) produces dozens of options per click from your keywords, and lets you save favorites on your device.

## Step 4 — Cut to ten with hard filters

Remove any name that fails one of these:

- **Radio test:** if you said it out loud, would people spell it correctly?
- **Length:** ideally 2–3 syllables, roughly 4–9 letters.
- **Meaning check:** no unfortunate meanings in your key languages or slang.
- **Category fit:** doesn't sound like a different industry.
- **Gut check:** you'd be proud to answer the phone with it.

Run your survivors through the [Name Tester](../tools/name-tester.html), which scores length, rhythm, spelling and flow.

## Step 5 — Check digital availability

- **Domain:** the .com is still the default trust signal in many markets. If it's taken, consider adding a short word ("get", "hq", "try") or choosing a relevant extension — but make sure the .com owner isn't a direct competitor.
- **Social handles:** check the platforms your audience actually uses.
- **Search results:** search the name. If page one is dominated by a big brand, you'll fight for visibility forever.

## Step 6 — Screen for trademarks

This step protects you from expensive rebrands later. A basic screen takes an hour:

1. Search the USPTO's trademark database and WIPO's Global Brand Database for identical and similar names.
2. Focus on the **same or related classes** of goods and services.
3. Look for names that *sound* alike, not just ones spelled alike.

A clear search is not legal clearance. Before you invest heavily, have a trademark attorney run a full search in each market you plan to enter.

## Step 7 — Test with real people

Show your top three names to 10–20 people in your target audience. Don't ask "which do you like?" — ask:

- "What do you think this company does?"
- "What would you expect it to cost?"
- "Can you spell it back to me?" (say it, don't show it)

Pick the name that creates the right expectations and survives the spelling test. Liking comes later; familiarity creates it.

## After you choose

Buy the domain and obvious typo domains, claim the handles, file your trademark application, and start using the name consistently. A name gets stronger with use — the best time to stop second-guessing it is the day you launch.
""", tool=("name-generator", "Generate brand names now"))

G("brand-identity-design", "Brand Identity Design: Logo, Color and Type Without Wasting Money",
  "What a brand identity system includes, how to brief a designer, and which pieces you can build yourself for free.",
  "Identity", 10, """
A brand identity is the visible, repeatable system that makes you recognizable: logo, color, typography, imagery, iconography and layout patterns. The key word is *system*. A beautiful logo used inconsistently does less than an average logo used with discipline.

## The core kit

At minimum, a working identity has:

- **A primary logo** plus a compact version (icon or monogram) for small spaces like favicons and app icons.
- **A color palette** of one primary color, one or two secondary colors and a neutral set — with exact HEX, RGB and CMYK values.
- **Two typefaces** — one for headlines, one for body text — with rules for sizes and weights.
- **Image style** — the kind of photography or illustration you use and what you avoid.
- **A few layout patterns** — how a social post, a slide and an email header are put together.

## Logos: what actually matters

A logo's job is identification, not explanation. A bank logo doesn't need a coin in it. What matters:

- **Works small.** Test at 16 px (browser tab) and 24 px (social avatar).
- **Works in one color.** You will need it on a receipt, an embroidered shirt and a dark background.
- **Is distinctive in your category.** Collect competitors' logos on one page; yours should stand out on that page.
- **Ages well.** Trend-driven effects (gradients, glows, ultra-thin lines) date fast.

## Color: choose for distinction, then psychology

Color associations are real but overstated. Blue isn't "trust" in every context; it's just very common, which is the bigger point — in a category full of blue, a different color is a strategic advantage. Choose your primary color by asking:

1. What colors do competitors own? Avoid them.
2. Which colors fit your personality (see our [color psychology guide](brand-color-psychology.html))?
3. Does it pass accessibility? Text needs a contrast ratio of at least 4.5:1 against its background under WCAG AA.

Generate harmonious options and check contrast instantly with our [Color Palette Generator](../tools/color-palette.html).

## Typography: two fonts, many uses

Most brands need only two typefaces. A common, reliable approach is a characterful display face for headlines paired with a highly readable sans-serif for body text. Free, open-licensed families from Google Fonts are perfectly professional — preview pairings in our [Font Pairing Explorer](../tools/font-pairing.html).

Rules worth writing down: heading sizes, body size (16–18 px on screen), line length (60–80 characters) and which weights are allowed.

## DIY vs. hiring a designer

| Your stage | Sensible approach | Typical budget range |
|---|---|---|
| Spark | DIY with free tools, simple wordmark | $0–$100 |
| Launch | Freelancer or design contest for logo + palette | Hundreds to low thousands |
| Grow | Experienced freelancer or small studio, full identity | Low to mid thousands |
| Scale | Agency, full system and guidelines | Five figures and up |

Prices vary widely by region and experience; treat these as orientation, not quotes.

## How to brief a designer

Good briefs produce good work. Include:

- Your one-page [brand strategy](brand-strategy-template.html)
- Three personality words and three "not" words
- Competitor logos and what you want to differ from
- Where the logo will appear (sign, app, packaging, embroidery)
- Deliverables: file formats (SVG, PNG, PDF), color versions, a mini style guide
- Ownership: confirm in writing that you receive full rights to the final artwork

## Keep it consistent

The moment you have a logo, colors and fonts, document them. Our [Style Guide Builder](../tools/style-guide-builder.html) turns your choices into a printable one-page guide you can share with anyone who creates content for you.
""", tool=("color-palette", "Generate an accessible palette"))

G("brand-voice-guide", "Brand Voice: How to Define How Your Brand Sounds",
  "Turn three personality words into a usable voice guide with do's and don'ts, tone shifts and real before-and-after examples.",
  "Messaging", 8, """
Your brand voice is your personality expressed in words. It's why one airline's safety announcement makes you smile and another's makes you check your phone. Voice is one of the cheapest brand assets to build and one of the most neglected.

## Voice vs. tone

- **Voice** is constant. It's who you are.
- **Tone** shifts with the situation. You're the same person at a celebration and at a funeral, but you don't speak the same way.

A brand that's "playful" in voice should still lower the playfulness in a payment-failure email or an apology.

## Build your voice in four steps

### 1. Choose three voice traits

Start with words that follow from your [brand strategy](brand-strategy-template.html) and [archetype](brand-archetypes.html). Good traits are specific: *candid* beats *honest*, *nerdy* beats *smart*.

### 2. Define each trait with "this, not that"

| Trait | This | Not that |
|---|---|---|
| Confident | Clear claims, backed by proof | Arrogant, dismissive |
| Warm | Friendly, human, uses "you" | Gushing, over-familiar |
| Precise | Specific numbers, plain words | Jargon, padding |

The "not that" column is where the value is — it stops writers from overcorrecting.

### 3. Write before-and-after examples

Rules are abstract; examples teach. Take three real pieces of your copy and rewrite them in your voice.

**Before:** "We offer innovative solutions to optimize your business workflows."
**After:** "We cut the busywork out of your week — most clients save five hours by Friday."

**Before:** "Your request has been received and will be processed in due course."
**After:** "Got it. You'll hear from a real person within one business day."

### 4. Map tone to situations

| Situation | Dial up | Dial down |
|---|---|---|
| Launch announcement | Energy, confidence | Caveats |
| Customer complaint | Empathy, clarity | Jokes |
| Error message | Helpfulness | Personality flourishes |
| Social media | Personality | Formality |

## Word lists

Keep two short lists: words you love and words you avoid. Many brands ban empty words like *leverage*, *synergy*, *world-class* and *solutions* because they say nothing a competitor couldn't.

## Grammar and style choices

Decide once and write it down: sentence case or title case headlines, contractions or not, emoji or not, the serial comma, how you write numbers and dates. These small choices create a surprisingly strong sense of consistency.

## Put it to work

Add your voice traits to your [one-page style guide](../tools/style-guide-builder.html), then rewrite your homepage, your "About" page and your three most-sent emails. Those six pieces of text shape more customer impressions than almost anything else you'll write this year.
""", tool=("tagline-generator", "Generate taglines in your tone"))

G("personal-branding-guide", "Personal Branding: Build a Reputation That Opens Doors",
  "A practical system for professionals, freelancers and creators to define, publish and grow a personal brand — without feeling fake.",
  "Personal brand", 11, """
Everyone with an online presence already has a personal brand. The only question is whether it's deliberate. A personal brand is simply what people say about you when you're not in the room — and what they find when they search your name.

## Why it matters now

Hiring managers, clients and partners search before they reply. A clear personal brand shortens trust: people arrive already knowing what you're good at. For freelancers and consultants, it's often the difference between competing on price and being asked for by name.

## Step 1 — Find your intersection

Strong personal brands sit at the overlap of three circles:

1. **What you're good at** — skills others ask you for
2. **What you care about** — topics you'd talk about unpaid
3. **What people pay for** — problems with a budget attached

Write a list for each, then look for a combination that's specific: "brand strategist" is crowded; "brand strategist for climate-tech startups" is ownable.

## Step 2 — Write your positioning line

Use: *I help [who] [achieve what] by [how].*

- "I help first-time founders name and launch their brand in 30 days."
- "I help nurses move into health-tech product roles."

Try our [Personal Bio Generator](../tools/bio-generator.html) to turn this line into social, short, medium and speaker bios.

## Step 3 — Fix your search results

Search your full name in a private window. Then:

- Claim a simple personal domain (your name, or name + profession).
- Make your LinkedIn headline your positioning line, not just a job title.
- Use the same professional photo and bio across profiles.
- Publish one cornerstone piece — a guide, case study or talk — that you want to be found for.

## Step 4 — Choose content pillars

Pick three to five topics you'll talk about repeatedly. Repetition is how people associate you with an idea. For example, a freelance brand designer might choose: naming, small-business identity, behind-the-scenes process, and client results.

A sustainable cadence beats a heroic one. Two thoughtful posts a week for a year will outperform two posts a day for a month.

## Step 5 — Show proof, not adjectives

"Passionate, results-driven professional" is wallpaper. Replace adjectives with evidence:

- Before-and-after work samples
- Specific numbers ("cut onboarding time from 3 weeks to 6 days")
- Short testimonials with names and roles
- Lessons from mistakes — these build more trust than wins

## Step 6 — Build relationships, not just reach

The highest-value part of a personal brand is often private: the inbox, the referrals, the introductions. Comment generously on others' work, credit collaborators, and say yes to small podcasts and panels — they compound.

## Personal brand red flags

- Faking expertise or inflating numbers — it's discoverable
- Posting only self-promotion
- Copying another creator's format so closely you look like a tribute act
- Sharing employer or client confidential information

## Measure what matters

Ignore follower counts at first. Track inbound messages, introductions, invitations, and how often people mention your topic when they describe you. If those rise, your personal brand is working.
""", tool=("bio-generator", "Write your bio in 30 seconds"))

G("rebranding-guide", "Rebranding: When to Do It, When Not To, and How to Get It Right",
  "Refresh or full rebrand? A decision framework, a step-by-step plan and the launch checklist that protects the equity you've built.",
  "Renewal", 10, """
Rebrands are risky because they spend accumulated recognition. Done well, they reignite growth; done badly, they confuse customers and get reversed. The difference is usually not design quality — it's whether there was a real reason to change.

## Good reasons to rebrand

- **Your strategy changed.** You serve a different audience, sell different things or moved upmarket.
- **Your name is a problem.** It's confusing, misspelled, legally contested or limiting.
- **A merger or acquisition** needs one coherent brand.
- **Your identity fails practically** — illegible on mobile, impossible to embroider, inaccessible.
- **Reputation damage** that operational fixes alone can't repair.

## Weak reasons

- The team is bored of the logo
- A new executive wants to make a mark
- A competitor rebranded
- "It feels dated" with no customer evidence

If your reasons are on the second list, consider a **refresh** instead.

## Refresh vs. rebrand

| | Refresh | Rebrand |
|---|---|---|
| What changes | Typography, color tweaks, photography, layouts | Name and/or positioning, full identity |
| Risk | Low | High |
| Cost | Lower | Significantly higher |
| Customers notice | "Looks sharper" | "Who is this?" |
| When | Every 5–10 years, or as needed | Only with a strategic reason |

## The rebrand process

1. **Audit equity.** What do customers recognize and value? Survey them: what color, shape, word or sound do they associate with you? These are your distinctive assets. Keep them unless they're actively harmful.
2. **Redefine strategy first.** Update your [one-page strategy](brand-strategy-template.html) before any design work starts.
3. **Explore, then narrow.** Look at a few design directions, from evolutionary to revolutionary. Test the finalists with real customers.
4. **Build the full system** — not just a logo. Templates, guidelines, signage, packaging, email, app icons.
5. **Plan the rollout.** Decide between a big-bang launch and a phased transition. Make an inventory of every touchpoint.
6. **Explain the change.** Tell customers why you've changed and what stays the same. People accept change they understand.

## Launch checklist

- Website, favicon and social profile images updated on the same day
- Redirects from any old domain, preserving search rankings
- Email signatures, invoices, contracts and templates
- Google Business Profile, directory listings and app store listings
- Physical items: signage, vehicles, uniforms, packaging (often phased)
- Trademark filings for the new name or mark
- Internal briefing so every staff member can explain the change

## Learn from reversals

High-profile reversals — such as Gap's short-lived 2010 logo and Tropicana's 2009 packaging redesign, which the company reverted after a reported sales drop — share a pattern: distinctive assets customers relied on were removed without a strategic reason customers could see. Protect what people use to find you.

## Measure success

Track recognition before and after (simple surveys work), branded search volume, website conversion and customer sentiment for at least six months. If recognition dips briefly and then recovers above the old baseline, the rebrand worked.
""", tool=("brand-health-score", "Check whether you need a rebrand"))

G("brand-archetypes", "The 12 Brand Archetypes Explained (With How to Use Them)",
  "What each of the 12 brand archetypes stands for, how it sounds and looks, and how to combine a primary and secondary archetype.",
  "Personality", 9, """
Brand archetypes are 12 recurring character patterns drawn from Carl Jung's work on archetypes and popularized for marketing by Margaret Mark and Carol Pearson in their book *The Hero and the Outlaw*. They're a shortcut to a coherent personality: once you know your archetype, decisions about tone, imagery and story become easier and more consistent.

Archetypes are a creative tool, not a science. Use them to align a team, not to put your brand in a box.

## The four motivations

The 12 archetypes are often grouped by the core human desire they serve:

| Desire | Archetypes |
|---|---|
| Stability and control | Caregiver, Creator, Ruler |
| Belonging and connection | Everyperson, Jester, Lover |
| Risk and mastery | Hero, Magician, Outlaw |
| Independence and fulfilment | Innocent, Explorer, Sage |

## The 12 archetypes

**The Innocent** — optimism and simplicity. Voice: positive, honest, reassuring. Risk: coming across as naive.

**The Sage** — truth and understanding. Voice: knowledgeable, measured, evidence-led. Risk: lecturing.

**The Explorer** — freedom and discovery. Voice: adventurous, candid. Risk: feeling aloof or unreliable.

**The Outlaw** — disruption and liberation. Voice: provocative, rebellious. Risk: alienating mainstream buyers.

**The Magician** — transformation. Voice: visionary, inspiring. Risk: overpromising.

**The Hero** — courage and achievement. Voice: bold, motivating. Risk: arrogance.

**The Lover** — intimacy and indulgence. Voice: sensual, warm. Risk: superficiality.

**The Jester** — joy and play. Voice: witty, irreverent. Risk: not being taken seriously.

**The Everyperson** — belonging and fairness. Voice: friendly, down-to-earth. Risk: blandness.

**The Caregiver** — service and protection. Voice: gentle, supportive. Risk: martyrdom or paternalism.

**The Ruler** — leadership and order. Voice: authoritative, polished. Risk: coldness.

**The Creator** — craft and self-expression. Voice: imaginative, detailed. Risk: perfectionism.

## Primary plus secondary

Most strong brands combine one dominant archetype with one supporting archetype. A Sage–Jester brand teaches with humor; a Hero–Caregiver brand pushes you while having your back. The secondary archetype adds texture and keeps the brand from becoming a cliché.

## How to choose yours

1. Start with your audience's deepest desire — what do they want to *feel*?
2. Look at competitors. If everyone in your category is a Sage, a Jester or Explorer brand stands out.
3. Check authenticity. Can your team and product genuinely live the archetype every day?
4. Take our free [Brand Archetype Quiz](../tools/brand-archetype-quiz.html) for a primary and secondary match.

## Turning an archetype into decisions

- **Voice:** use the archetype's voice to draft your [voice guide](brand-voice-guide.html).
- **Visuals:** let it guide color, photography and type — a Ruler brand rarely uses bubbly rounded type.
- **Story:** every archetype has a story shape. Heroes overcome, Explorers discover, Caregivers protect.
- **Behavior:** archetypes should change how you act, not just how you look. A Caregiver brand with a hostile returns policy is a contradiction customers will notice.
""", tool=("brand-archetype-quiz", "Take the archetype quiz"))

G("brand-color-psychology", "Brand Color Psychology: What Colors Really Communicate",
  "What common brand colors suggest, why category context matters more than color charts, and how to choose an accessible palette.",
  "Identity", 8, """
Color is often the first thing people remember about a brand — sometimes before the name. But most "color psychology" charts oversimplify. Red doesn't make everyone hungry and blue doesn't make everyone trust you. What color communicates depends on culture, category and what competitors already use.

## Common associations (in many Western markets)

| Color | Often associated with | Watch out for |
|---|---|---|
| Red | Energy, urgency, passion, appetite | Can feel aggressive or signal danger |
| Orange | Friendliness, enthusiasm, value | Can feel cheap if overused |
| Yellow | Optimism, attention, warmth | Poor legibility as text on white |
| Green | Growth, health, nature, money | Very crowded in wellness and finance |
| Blue | Reliability, calm, technology | Extremely common — hard to stand out |
| Purple | Creativity, luxury, imagination | Can feel niche or juvenile in bright tints |
| Pink | Playfulness, care, modernity | Strong gender coding in some markets |
| Black | Sophistication, power, premium | Can feel cold or heavy |
| White / neutrals | Simplicity, cleanliness, calm | Easy to be forgettable |

Associations differ across cultures. White is linked with mourning in parts of East Asia; red signals luck and celebration in China. If you operate internationally, test with people in each market.

## Context beats charts

The most useful color question isn't "what does green mean?" but "what does green mean *here*?" In a category full of blue banks, a bank in warm coral is instantly distinctive. Distinctiveness drives recognition, and recognition drives choice.

Practical steps:

1. Collect logos and websites from your top ten competitors.
2. Note which hues dominate.
3. Shortlist colors that fit your personality *and* are rare in that set.

## Building a palette

A practical brand palette has:

- **One primary color** — your signature; used for key moments, not everywhere
- **One or two secondary colors** — support and variety
- **A neutral range** — backgrounds and text (off-white, greys, near-black)
- **Functional colors** — success, warning and error states for digital products

The 60-30-10 rule is a helpful starting point: about 60% neutral, 30% secondary, 10% primary accent.

## Accessibility is non-negotiable

Roughly 1 in 12 men and 1 in 200 women have some form of color vision deficiency. Never rely on color alone to convey meaning, and make sure text contrast meets WCAG guidelines: **4.5:1** for normal text and **3:1** for large text under the AA level. Our [Color Palette Generator](../tools/color-palette.html) shows contrast ratios for every color against white and black so you can see which shades are safe for body text.

## Document exact values

Record each color in HEX (web), RGB (screens), CMYK (print) and, if you print a lot, a Pantone reference. Inconsistent reds across a website, a sign and a box are one of the most common signs of an unmanaged brand. Put your values into your [style guide](../tools/style-guide-builder.html).
""", tool=("color-palette", "Build your palette"))

G("small-business-branding", "Small Business Branding on a Budget: A 30-Day Plan",
  "A day-by-day plan to build a credible brand with free and low-cost tools — positioning, identity, website, reviews and local search.",
  "Small business", 10, """
You don't need an agency to have a strong brand. You need clear decisions, consistency and a month of focused effort. This plan assumes about an hour a day and almost no budget.

## Week 1 — Decide

- **Day 1:** Write your [positioning statement](../tools/positioning-statement.html). Who do you serve, and why you?
- **Day 2:** List your top five competitors. Note their colors, taglines and prices. Find the gap.
- **Day 3:** Choose three personality words and three "not" words.
- **Day 4:** Take the [Brand Archetype Quiz](../tools/brand-archetype-quiz.html) and compare the result with your words.
- **Day 5:** Pressure-test your name with the [Name Tester](../tools/name-tester.html). If you're renaming, use the [Name Generator](../tools/name-generator.html).
- **Days 6–7:** Talk to five customers. Ask why they chose you and what nearly stopped them. Their words become your copy.

## Week 2 — Design the basics

- **Day 8:** Generate a palette with the [Color Palette Generator](../tools/color-palette.html). Check contrast.
- **Day 9:** Pick a font pairing with the [Font Pairing Explorer](../tools/font-pairing.html).
- **Day 10:** Create a simple wordmark (your name in your headline font, perhaps with one distinctive detail). Simple and consistent beats complex and inconsistent.
- **Day 11:** Make a compact icon version for social avatars and favicons.
- **Day 12:** Write three taglines with the [Tagline Generator](../tools/tagline-generator.html); pick one.
- **Days 13–14:** Build your one-page [style guide](../tools/style-guide-builder.html).

## Week 3 — Apply it everywhere

- **Day 15:** Update your website homepage: headline from your positioning, a clear call to action, real photos.
- **Day 16:** Claim or update your Google Business Profile: categories, hours, photos, description.
- **Day 17:** Make social profiles match: same avatar, bio, link and cover style.
- **Day 18:** Redesign your email signature, invoice and quote templates.
- **Day 19:** Create three reusable social post templates.
- **Days 20–21:** Audit physical touchpoints: sign, cards, packaging, uniforms. List what to update as stock runs out.

## Week 4 — Build trust and visibility

- **Day 22:** Ask your ten happiest customers for reviews, with a direct link.
- **Day 23:** Write one genuinely useful guide answering your customers' most common question.
- **Day 24:** List your business in two or three relevant directories with identical name, address and phone.
- **Day 25:** Set up a simple newsletter or customer email list.
- **Day 26:** Plan one partnership with a complementary local business.
- **Day 27:** Plan a small contest or giveaway that rewards referrals.
- **Days 28–30:** Take the [Brand Health Score](../tools/brand-health-score.html) again and compare with Day 1.

## Where to spend money first

If you have a small budget, spend it in this order:

1. Your domain and professional email
2. A designer to refine your DIY logo into clean vector files
3. Good photography of your real product, space or team
4. Printed items you use every day

## Consistency is the multiplier

The plan works because it makes every touchpoint say the same thing. Customers rarely remember any single ad; they remember the pattern. Repeat your colors, your tagline and your promise until you're tired of them — that's usually when customers start to notice.
""", tool=("brand-health-score", "Take your Day 1 score"))

G("measuring-brand-health", "How to Measure Brand Health: 10 Metrics That Matter",
  "Awareness, consideration, share of search, NPS and more — how to track brand health with free tools and simple surveys.",
  "Measurement", 9, """
"Brand" can feel unmeasurable, which is why it's often the first budget cut. It isn't. You can track brand health with a handful of metrics, most of them free. The goal isn't a perfect number; it's a trend line you can act on.

## The brand funnel

Brand metrics map onto a simple funnel:

1. **Awareness** — do people know you exist?
2. **Familiarity** — do they know what you do?
3. **Consideration** — would they consider you?
4. **Preference** — would they choose you over alternatives?
5. **Loyalty and advocacy** — do they come back and recommend you?

## Ten metrics worth tracking

### Awareness and visibility

1. **Branded search volume.** How many people search your name? Google Search Console shows queries containing your brand for free. Growth here is one of the best leading indicators of brand strength.
2. **Share of search.** Your branded search volume divided by the total for you and your main competitors. Marketing effectiveness researchers, notably Les Binet, have argued it tracks closely with market share over time.
3. **Direct traffic.** Visitors who type your URL or use a bookmark — a proxy for memory.
4. **Aided and unaided awareness.** Ask a sample of your target audience: "Which brands of X can you name?" (unaided), then "Which of these have you heard of?" (aided).

### Perception

5. **Brand association.** Ask: "Which words describe [brand]?" Compare answers with your intended personality words.
6. **Sentiment.** Track the tone of reviews and mentions. Even a monthly manual read of reviews is valuable.

### Behavior and loyalty

7. **Net Promoter Score (NPS).** "How likely are you to recommend us to a friend?" on a 0–10 scale. NPS = % promoters (9–10) minus % detractors (0–6).
8. **Repeat purchase rate.** The share of customers who buy again within a set period.
9. **Referral share.** The percentage of new customers who came via word of mouth.
10. **Price premium.** Can you charge more than average competitors without losing conversion? Pricing power is the financial signature of a strong brand.

## A simple brand dashboard

| Metric | Source | Frequency |
|---|---|---|
| Branded search | Google Search Console | Monthly |
| Direct traffic | Website analytics | Monthly |
| NPS | Two-question email survey | Quarterly |
| Reviews and rating | Google, marketplaces | Monthly |
| Referral share | "How did you hear about us?" field | Monthly |
| Awareness | Short survey of target audience | Twice a year |

## Running a low-cost brand survey

You don't need a research agency. A ten-question survey sent to your email list and shared in relevant communities will reveal patterns. Keep questions neutral, randomize brand order in lists, and survey at the same time each year for comparability.

## Start with a self-assessment

Before you build dashboards, get a baseline. The [Brand Health Score](../tools/brand-health-score.html) rates your brand across clarity, identity, consistency, visibility and loyalty in about five minutes, and tells you which area to fix first. Retake it every quarter and watch the trend.
""", tool=("brand-health-score", "Get your baseline score"))
