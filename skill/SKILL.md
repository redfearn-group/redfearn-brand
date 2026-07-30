---
name: redfearn-group-style
description: 'Apply the Redfearn Group design system and voice to any deliverable for Brady Redfearn / Redfearn Group: portfolio, redfearn.group, case studies, blog posts, reports, dashboards, slides, diagrams, GitHub project repos, and the working apps published from them (garage-log, home-log, and any future app). Use whenever Brady asks for one of these or is creating or restyling an app repo, even if he does not name the system explicitly, and whenever writing Brady-facing copy that should avoid em-dashes and AI-sounding phrasing. Canonical, standalone design system and voice guide, independent of any employer branding: defines the three layer scopes (Identity, Content, Product), typography, WCAG-verified color pairings, status/callout components, signature elements, voice rules, diagram conventions, and known implementation pitfalls. Colors live in brand.css in redfearn-group/redfearn-brand, which this skill points at rather than restating. Supersedes any earlier barn-swallow-design skill.'
---

# Redfearn Group Design System

The canonical, standalone design system for Brady Redfearn / Redfearn Group. Every visual artifact, portfolio pages, case studies, dashboards, reports, slides, should draw from these tokens. This system is intentionally independent of any employer's brand: it belongs to Brady, not to any organization he works with.

The palette draws from two sources: the barn swallow's natural coloring (deep blue-black, cream, cinnamon, tawny, gape yellow, plus a forest green) and Redfearn Group's own brand red. Typography is an open-source modern stack, no Microsoft/Aptos dependency, no institutional fonts.

---

## Source of Truth

**Values live in `brand.css`. This document holds the rules.**

Canonical file: [`redfearn-group/redfearn-brand`](https://github.com/redfearn-group/redfearn-brand) → `brand.css`. It is vendored into every property, and a CI job in each consuming repo fails the build when a copy drifts.

| Property | Vendored path | Layer |
| :--- | :--- | :--- |
| redfearn-group.github.io | `src/css/brand.css` | Identity, plus Content on case studies |
| garage-log | `src/styles/brand.css` | Product |
| home-log | `src/styles/brand.css` | Product |

When building anything for Brady:

1. **Never hand-copy tokens out of this document into a new stylesheet.** Import or vendor `brand.css`. The hex values below are reference for reasoning about contrast and pairing, not a source to copy from.
2. **Never edit a vendored copy.** Edit the canonical file, run `node sync.mjs` in the brand repo, push the brand repo first, then the consumers.
3. If a property needs a value that is not in `brand.css`, that is a signal the token belongs in `brand.css`, not that the property should invent its own.

This split exists because the previous arrangement, where this document restated every hex code in prose, produced four independent copies of the design system (this skill, the site's CSS, and two app stylesheets) that silently diverged. Prose guidance makes drift diagnosable after the fact. A shared artifact plus a drift check prevents it.

---

## Voice & Copy

The visual system and the writing follow the same standard: confident, specific, and never AI-generated-sounding. Apply these rules to every piece of Redfearn Group copy, site pages, case studies, blog posts, slide text, alike.

- **No em-dashes.** Not a style preference, a hard rule. Restructure with a period, a comma, or a colon instead.
- **No AI-tropes.** Avoid phrases like "in today's fast-paced landscape," "leverage," "unlock the potential," "delve into," "it's important to note," "navigate the complexities," "game-changer," "cutting-edge," "seamless," "robust solution." If a sentence could appear in a generic corporate AI-written blog post, rewrite it.
- **Short, direct sentences.** Cut hedging ("might potentially," "it could be argued"). State the position.
- **Numbers over adjectives.** "75x adoption growth" beats "significant adoption growth" every time. If a claim can be backed by a real number, use the number, and only numbers that are actually verified true, never invented ones that sound plausible.
- **Confident, not hedgy.** This is an executive's brand, not a cover letter. Say what's true plainly.

---

## Color Tokens

These are the only colors to use. Do not introduce grays outside the defined neutral scale, or any other off-system colors, without explicit instruction.

```
--rg-red:       #BF1E2E   /* Redfearn Group brand red, identity layer anchor */
--rg-blue:   #0A1128   /* Deep steel blue-black, primary text, dark surfaces (renamed from --rg-ink) */
--rg-cream:  #F7F4EF   /* Cream/off-white, main light background */
--rg-green:  #1A6635   /* Forest green, positive/on-track status signal */
--rg-gape:   #FFCC00   /* Gape yellow, AI log hero element, warning bars (dark bg only) */
--rg-tawny:  #D97443   /* Tawny, warm secondary, metric panels, "at risk" status */
--rg-ember:  #C2592A   /* Cinnamon/ember, large headings, UI, "caution" status */
```

### Editorial Neutral Scale

Secondary palette for text hierarchy, borders, and surfaces, keeps muted tones consistent instead of inventing opacity values per page.

```
--rg-graphite: #2B2F36   /* secondary headings, dark-mode elevated text */
--rg-slate:    #4B5563   /* secondary body text, "Note" callout */
--rg-ash:      #676E7C   /* tertiary text, captions, labels */
--rg-mist:     #D1D5DB   /* borders, dividers, "Definition" tint */
--rg-paper:    #F8F9FA   /* off-white surface, "Bottom Line" tint */
--rg-bone:     #F7F5EF   /* warm off-white, alternate to cream for layering */
```

These neutrals are for secondary/tertiary text, captions, borders, and surface layering, not verified for primary body copy at small sizes. For body text, use `--rg-blue` on `--rg-cream` (or the reverse), which is independently AAA-verified. If you use Slate or Ash for body-length text, check contrast before shipping.

---

### WCAG Compliance Reference

Pre-verified pairs. Choose from this list for text. Don't eyeball new combinations.

| Usage | Text | Background | Ratio | Level |
|---|---|---|---|---|
| Body text (light mode) | `#0A1128` | `#F7F4EF` | ~18:1 | **AAA** |
| Reverse (dark mode body) | `#F7F4EF` | `#0A1128` | ~18:1 | **AAA** |
| Gape yellow on dark | `#FFCC00` | `#0A1128` | ~9.5:1 | **AAA** |
| Green status text | `#1A6635` | `#F7F4EF` | ~7.2:1 | **AAA** |
| RG Red on cream (body) | `#BF1E2E` | `#F7F4EF` | ~6.1:1 | **AA** ✓ body text |
| Cream on RG Red (buttons) | `#F7F4EF` | `#BF1E2E` | ~6.1:1 | **AA** ✓ button text |
| Body on tawny panel | `#0A1128` | `#D97443` | ~5.2:1 | **AA** — tawny as a background with dark text on it |
| Tawny on cream (as text) | `#D97443` | `#F7F4EF` | ~2.9–3.2:1 | Fails even large text. Never use tawny as literal text color anywhere, not just tags/labels, a heading or word-cloud item styled with it directly fails the same way (see `.tag-tawny` below for the accent-edge pattern that keeps the hue visible without putting it in the text color) |
| Cinnamon/ember on cream | `#C2592A` | `#F7F4EF` | ~3.8:1 | UI / Large only, never as tag/label text (see `.tag-ember` below) |
| RG Red on dark navy blue | `#BF1E2E` | `#0A1128` | ~3.3:1 | UI / Large only |
| Ash (muted label) on cream | `#676E7C` | `#F7F4EF` | ~4.67:1 | **AA** |

**Critical rules:**
- `--rg-red` on `--rg-blue` is only ~3.3:1. On dark backgrounds, use red for borders, gradient bars, badges, and button fills, not for dark-mode body text. Use `--rg-cream` for dark-mode body text instead.
- `--rg-gape` (yellow) must never appear on any light background. It fails contrast against cream every time.
- `--rg-ember` (cinnamon) is for headings ≥18pt, bold ≥14pt, or UI components only. Never body paragraphs.

---

## Color Role Architecture

Three layers govern how colors are applied. Keep them distinct. Each is a CSS class scope in `brand.css` that sets `--accent`, `--accent-tint`, `--accent-border`, and the gradient stops.

**Identity Layer** (`:root`, no class needed. Anchor: `--rg-red`): the brand anchor. Use as primary accent on Brady-branded surfaces: the main portfolio (redfearnb.github.io), redfearn.group, nav/logo accents, CTA buttons, live badges, card hover borders, gradient bars, section dots. This is what visitors associate with the Redfearn Group brand.

**Content Layer** (`.content-layer`. Anchor: `--rg-ember` to `--rg-gape`): used within portfolio pieces, case studies, reports, and project-specific work. Carries warmth and craft without competing with the brand red. Gape yellow is reserved for the dark-mode hero log element specifically.

**Product Layer** (`.app-layer`, dark surfaces): real working applications published as GitHub projects, such as garage-log and home-log. These are portfolio evidence that Brady ships working software, so they carry the brand mark and brand red, but on dark surfaces to read as tools rather than marketing pages. Set the class on `<html>`.

Never mix layers within the same accent role on the same page. A card on the main portfolio uses `--rg-red` for hover borders; the same card pattern inside a case study uses `--rg-ember`; inside an application, text and links use `--rg-cream` and red moves to the underline, border, or fill. The component does not change, the layer scope does.

**Why Product still reads as red, without a red accent token:** raw `--rg-red` is 2.88:1 on the dark card and fails contrast for text, so text and links on `.app-layer` use cream, same as body copy, and red carries the brand instead through underlines, borders, tints, and the gradient bar, which are decorative and not contrast-bound. Do not invent a lightened red to force red text onto dark. The palette is the closed set defined here and in `logo-system.md`'s five schemes; off-system colors are not introduced without Brady's explicit sign-off, confirmed 2026-07-24 after an earlier pass added one without asking.

---

## Status & Callout System

A complete semantic vocabulary for reports, dashboards, and case studies. Full HTML/CSS for every variant lives in `references/callout-system.md`. Load it when building any report, dashboard, or status-driven artifact.

### Status Signals
| Status | Token | Notes |
|---|---|---|
| ON TRACK | `--rg-green` | 7.2:1 AAA, safe for text |
| AT RISK | `--rg-tawny` | bold/UI weight |
| BLOCKED | `--rg-ember` | ~3.8:1, UI/large text only |
| CRITICAL | `--rg-red` | 6.1:1 AA, safe for text on cream |

### KPI Deltas
- ▲ Up → `--rg-green`
- ▼ Down (moderate) → `--rg-ember`
- ▼ Down (severe) → `--rg-red`

### Callout Variants (8)
| Variant | Bar / Accent | Text | Use |
|---|---|---|---|
| KEY INSIGHT | `--rg-blue` | `--rg-blue` on cream tint | Primary finding, strongest non-semantic signal |
| NOTE | `--rg-slate` | `--rg-slate` | Informational, non-urgent context |
| BOTTOM LINE | `--rg-blue` | `--rg-blue` on `--rg-paper` | TL;DR / recommendation |
| DEFINITION | `--rg-graphite` | `--rg-graphite` on `--rg-mist` tint | Term introduction, code blocks |
| QUOTE | `--rg-tawny` | `--rg-blue` | Attributed excerpts |
| WARNING | `--rg-gape` bar, `--rg-ember` label | `--rg-ember` | Risks/caveats, yellow bar, ember label (yellow fails as text) |
| CAUTION | `--rg-ember` | `--rg-ember` | Do-not-proceed, one level below Alert |
| ALERT | `--rg-red` | `--rg-red` | Most severe, already failing |

Implementation pattern: 4px left accent bar + ~8% tint background. See `references/callout-system.md` for exact CSS and tint hex values.

---

## Typography

Open-source, modern, no institutional dependency.

| Role | Typeface | Weight(s) | Use |
|---|---|---|---|
| Display | **Space Grotesk** | 700, 600, 500 | Page titles, hero headings, metric values, card titles |
| Body | **IBM Plex Sans** | 400, 300, italic 300 | Paragraphs, descriptions, captions, nav links |
| Mono | **JetBrains Mono** | 500, 400 | Section labels, badges, data, code, eyebrows, timestamps |

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
```

### Type Scale

| Level | Family | Size | Weight | Letter-spacing |
|---|---|---|---|---|
| Hero H1 | Space Grotesk | clamp(2.5rem, 5vw, 4.5rem) | 700 | -0.025em |
| Page H1 | Space Grotesk | clamp(2rem, 4vw, 3rem) | 700 | -0.02em |
| H2 | Space Grotesk | 1.5–1.75rem | 600 | -0.015em |
| H3 | Space Grotesk | 1.1–1.2rem | 600 | -0.01em |
| Body | IBM Plex Sans | 1rem | 400 | 0 |
| Small body | IBM Plex Sans | 0.875rem | 300 | 0 |
| Section label | JetBrains Mono | 0.75rem | 500 | 0.14–0.18em |
| Metric value | Space Grotesk | 1.5–2.5rem | 700 | -0.02em |
| Badge/tag | JetBrains Mono | 0.75rem | 500 | 0.06em |

### Minimum Text Size

No text on the site, in a document, or baked into a graphic asset (a logo
file, a diagram, an OG card) renders smaller than **12px (0.75rem)**,
full stop. No exceptions for compact UI chrome (tags, pills, badges, the
footer legal line): an earlier version of this rule allowed those down to
11px, and 11px is exactly what shipped in the live-badge before Brady
flagged it as barely readable. The gap between 11px and 12px looks small
on paper and is not small on screen, especially in tracked uppercase
mono. Treat 12px as the one number, not a range.

- **The floor: 12px (0.75rem), everywhere.** Eyebrows, section labels,
  metric/timeline labels, nav links, tags, pills, badges, footer legal
  text, post meta, logo-baked text. If a design genuinely can't fit 12px
  text, the design is wrong for that space, not the text.
- **Weight floor: 500 (Medium) minimum for anything under 14px.** Light
  (300) and Regular (400) lose stroke contrast fast at small sizes,
  especially in tracked uppercase mono, where letter-spacing pulls the
  already-thin strokes further apart. This is why every eyebrow, tag,
  badge, and label in Component Patterns below carries `font-weight: 500`
  or heavier even though the base body font is Regular.
- **Exemption: the Ambient AI Operations Log.** It's intentionally
  near-invisible background texture at 5–7% opacity, not reading content,
  see Signature Design Element 5. The floor doesn't apply to things that
  aren't meant to be read.
- **Logo-system corollary:** a multi-tier wordmark (a prominent word plus
  a smaller secondary word, like REDFEARN plus GROUP) must be checked at
  its *actual on-screen render size* wherever it's placed, not just at
  its native SVG size. A secondary tier that's perfectly legible at
  native/poster size can shrink below the 12px floor once the whole
  composition is displayed small (a nav bar, a footer lockup). If it
  does, don't just scale the whole composition down further: either
  enlarge the placement, or use a variant whose proportions were tuned
  for that scale. See `references/logo-system.md` for the full ratio
  history and the nav/footer sizing this produced.

---

## Mode Selection

### Light Mode (default for reports, case studies, documents, redfearn.group)
- Background: `--rg-cream`
- Body text: `--rg-blue`
- Primary accent: `--rg-red` (identity layer) or `--rg-ember` (content layer)
- Secondary accent: `--rg-tawny`
- CTA: blue-fill or red-fill button with cream text

### Dark Mode (portfolio hero, interactive dashboards, all Product-layer apps)
- Background: `--rg-blue`
- Surface (cards): `#0F1830` (blue tinted slightly warm)
- Body text: `--rg-cream`
- Text and links: `--rg-cream`, same as body copy. Do not color links red on dark, raw `--rg-red` is 2.88:1 on the card and fails contrast.
- Red carries the brand through decoration instead: link underlines, card borders on hover, the gradient bar, tint fills, dots. All decorative uses are not contrast-bound, so raw `--rg-red` is fine there.
- Hero log element: `--rg-gape` exclusively
- Muted text: `#9AA1AE`, or `rgba(247,244,239,0.55)` cream at reduced opacity
- Borders: `rgba(191,30,46,0.12–0.35)` red ghost, or `rgba(247,244,239,0.12)` cream ghost

**Verified against the card surface `#0F1830`**, which is the binding constraint because it is lighter than the page background. Measured 2026-07-24, superseding the earlier "good-faith, not independently verified" note:

| Token | Ratio on card | Level |
| :--- | ---: | :--- |
| cream body text / links | 16.04:1 | AAA |
| muted text `#9AA1AE` | 6.77:1 | AA |
| status overdue `#FF6B7A` | 6.40:1 | AA |
| status due-soon `#F0A57A` | 8.69:1 | AAA |
| status ok `#4CAF6E` | 6.42:1 | AA |
| `--rg-gape` (log only) | 11.64:1 | AAA |
| raw `--rg-red` (decorative only) | 2.88:1 | fails as text, fine as a border/underline/fill |
| raw `--rg-ember` (decorative only) | 3.98:1 | fails as text, fine as a border/underline/fill |

**Product-layer apps are dark unconditionally, not through `prefers-color-scheme`.** The dark treatment is the product identity for these tools, not an echo of an OS setting. Do not add a light-mode branch to an app.

---

## Signature Design Elements

### 1. Eyebrow Label
```css
.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 0.65rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--rg-ash);          /* muted label text */
}
.eyebrow::before {
  content: '';
  display: block;
  width: 26px;
  height: 1px;
  background: var(--rg-red);     /* identity layer rule */
  /* content layer: background: var(--rg-ember); */
}
```

### 2. Live / Active Badge
This component is calibrated for dark backgrounds (the hero). Text is
`--rg-cream`, not `--rg-red`: the WCAG table above already flags
`--rg-red` on `--rg-blue` at ~3.3:1, well under the 4.5:1 floor for text
this size, and this badge is exactly the kind of small tracked-caps label
that fails hardest at low contrast. Red stays on the border, tint
background, and dot, since those are decorative, not text. If this
component is ever placed on a light/cream background instead, swap the
text color to `--rg-red` there (6.1:1 AA per the table) rather than
reusing this dark-mode version as-is.
```css
.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.22rem 0.65rem;
  background: rgba(191,30,46,0.08);
  border: 1px solid rgba(191,30,46,0.22);
  border-radius: 99px;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--rg-cream);
}
.live-dot { width: 5px; height: 5px; border-radius: 50%; background: var(--rg-red); animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.25} }
```

### 3. Gradient Accent Bar
```css
/* Identity layer */
.featured-card-identity::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, #BF1E2E 0%, #D97443 100%);  /* red → tawny */
}
/* Content layer */
.featured-card-content::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, #C2592A 0%, #FFCC00 100%);  /* ember → gape */
}
```

### 4. Section Label with Rule
```css
.section-label {
  display: flex; align-items: center; gap: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  font-weight: 500;
  font-size: 0.75rem; letter-spacing: 0.18em; text-transform: uppercase;
  color: var(--rg-ash);
}
.section-label::after { content: ''; flex: 0 0 80px; height: 1px; background: var(--rg-mist); }
```

### 5. Ambient AI Operations Log (dark hero only)
The scrolling log is the signature hero element on dark-mode pages. Reference the *type* of work Brady does (LLM agents, AI governance, multi-agent systems, systems engineering) rather than placeholder text. This is content, not a branding choice, so it should feel real and specific.

**Confidentiality check first, every time:** Brady's current role is under an active NDA. Before any log line ships, ask whether it names his current employer, cites a headcount/enrollment figure, or is specific enough that someone could reverse-search it back to one identifiable institution. If yes, generalize it (describe scale qualitatively, e.g. "enterprise scale," instead of a number that's really just his current employer's well-known headcount in disguise). Past employers he's already named publicly on his own site and LinkedIn (Blackboard, IBM, Amazon, Sonos, BluePath Labs) are fine to reference directly since that's already public information. The caution is specifically about the *current* job. Opacity 0.05–0.07, gape yellow only, never increase beyond 0.10. Line library in `references/log-lines.md`.

### 6. Logo System
The Redfearn Group mark is finalized: one canonical "RG" badge (cream Space Grotesk Bold letterforms on a `--rg-red` rounded square) plus a "REDFEARN GROUP" wordmark (Space Grotesk Bold + tracked JetBrains Mono Medium), combined into six layouts (lockup, wide, stacked, wordmark-only, icon-only, icon-avatar-safe) and a growing set of color schemes: Red (transparent, the primary file), Red and Cream (opaque, self-contained on any backdrop), Reverse Cream (transparent cream-ink knockout), Black & White (opaque two-tone, single-color-reproduction fallback only), Red with Group Blue (adopted for the site nav/header on light backgrounds, `wide` layout only), plus one open comparison candidate, Watermark. Every letterform in every variant is a real vector glyph outline, never live `<text>` with a font-family reference, since standalone SVG files don't reliably load webfonts. GROUP's cap height is fixed at roughly 0.45x REDFEARN's across every layout, the minimum that keeps GROUP legible once a variant is displayed small (see Minimum Text Size above); don't shrink that ratio further chasing a more dramatic size contrast. An outlined-letterform treatment (solid fill, contrasting stroke) was built and evaluated, then deliberately rejected: full-color blocking (a solid badge, solid wordmark) reads as a more confident, professional identity mark, outlined letters read closer to a garment/decal treatment. Do not reintroduce an outline scheme without Brady explicitly asking for it again.

**Icon-only is deprecated** (confirmed to clip on circular crops) in favor of **icon-avatar-safe**, the same badge inset in a 190x190 canvas sized specifically to clear Google's maskable-icon 40%-radius safe zone. Don't generate new icon-only files or point new placements at it.

Full specification, the do's and don'ts, minimum sizes, the current scheme table, and the knockout technique (now reverse/red only, not black-and-white): `references/logo-system.md`. To generate a new size or combination, use `scripts/generate_logo_variant.py` against the pre-extracted glyph data in `assets/logo-glyph-paths.json`, don't hand-edit an existing SVG's transforms or re-derive glyph paths from font files again.

---

## Component Patterns

### Card (Light Mode)
```css
.card {
  background: #FFFFFF;
  border: 1px solid rgba(10,17,40,0.10);
  border-radius: 4px;
  padding: 2rem;
  transition: border-color 0.2s, transform 0.18s;
}
.card:hover { border-color: rgba(191,30,46,0.30); transform: translateY(-2px); }  /* identity layer hover */
```

### Card (Dark Mode)
```css
.card-dark {
  background: #0F1830;
  border: 1px solid rgba(191,30,46,0.10);
  border-radius: 4px;
  padding: 2rem;
  transition: border-color 0.2s, transform 0.18s;
}
.card-dark:hover { border-color: rgba(191,30,46,0.28); transform: translateY(-2px); }
```

### Primary Button
```css
/* Light background */
.btn-primary-light { background: var(--rg-red); color: var(--rg-cream); font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 0.875rem; padding: 0.75rem 1.7rem; border-radius: 2px; border: none; }
/* Dark background */
.btn-primary-dark { background: var(--rg-red); color: var(--rg-cream); font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 0.875rem; padding: 0.75rem 1.7rem; border-radius: 2px; border: none; }
```

### Tag / Chip
```css
/* Provided by brand.css. Reproduced here for reasoning only, do not copy.
   Status tags read from the --status-*-fg/-bg tokens rather than the raw
   palette, so they pick up the corrected dark values inside .app-layer
   automatically. Font size is 0.75rem, not 0.6rem: an earlier version of
   this snippet said 0.6rem, which is 9.6px and violates the 12px floor in
   Minimum Text Size above. The floor wins. */
.tag { padding: 0.22rem 0.55rem; border-radius: 2px; font-family: 'JetBrains Mono', monospace; font-weight: 500; font-size: 0.75rem; letter-spacing: 0.06em; text-transform: uppercase; }
.tag-red    { color: var(--status-overdue-fg);  background: var(--status-overdue-bg); }
.tag-green  { color: var(--status-ok-fg);       background: var(--status-ok-bg); }
.tag-neutral{ color: var(--status-never-fg);    background: var(--status-never-bg); }
/* tag-tawny's default (light) value of --status-due-soon-fg is --rg-tawny,
   which measures ~2.9-3.2:1 as text, worse than ember's ~3.8:1 and
   confirmed 2026-07-27, same root cause: copy-pasted across red/green/
   tawny/ember without checking each hue's own contrast as text. The
   .app-layer override already corrects to #F0A57A (8.69:1 AAA) for real
   due-soon status badges in garage-log/home-log, untouched here. The
   default gets the same accent-edge move as tag-ember, and now matches
   co-quote, which has used exactly this pattern since day one. */
.tag-tawny {
  position: relative;
  padding-left: 0.95rem;
  color: var(--rg-blue);
  background: var(--status-due-soon-bg);
}
.tag-tawny::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--rg-tawny); border-radius: 2px 0 0 2px; }
.app-layer .tag-tawny { padding-left: 0.55rem; color: var(--status-due-soon-fg); background: var(--status-due-soon-bg); }
.app-layer .tag-tawny::before { content: none; }
/* tag-ember does NOT set ember as the text color. Ember-as-text measures
   ~3.8:1 on cream and ~3.98:1 on the app-layer card, both below the 4.5:1
   floor at this size, confirmed as a live failure on the frameworks/
   case-study tags 2026-07-26. Ember instead renders as a 3px decorative
   left edge, and the label text uses the surface's safe neutral
   (--rg-blue light, --rg-cream dark), the same brand-on-decoration move
   used for dark-mode links elsewhere in this system. Brady reviewed this
   against plain ember text and picked the accent-edge version as more
   consistent with an executive-level site; don't revert to ember text
   without asking again. */
.tag-ember {
  position: relative;
  padding-left: 0.95rem;
  color: var(--rg-blue);
  background: rgba(194,89,42,0.08);
}
.tag-ember::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; background: var(--rg-ember); border-radius: 2px 0 0 2px; }
.app-layer .tag-ember { color: var(--rg-cream); background: rgba(217,116,67,0.12); }
.app-layer .tag-ember::before { background: var(--rg-tawny); }
```

---

## Diagrams & Data Visualization

Custom SVG diagrams, architecture diagrams, pictograms, Gantt-style timelines, are a proven way to make technical and career depth visible instead of just claimed in prose. Use the same layer logic as everything else:

- **Identity layer pages** (home, about, contact): `--rg-red` as the primary diagram accent, blue for structural boxes and text.
- **Content layer pages** (case studies): `--rg-ember` to `--rg-gape` gradient accents, matching the content-layer gradient bar.
- Structural boxes: white or cream fill, `rgba(10,17,40,0.15)` blue-tinted border, `rx="4"` to `rx="6"` corner radius, consistent with the Card component.
- Connecting lines: 1.5px stroke weight, accent color. Arrowheads are usually unnecessary for simple hierarchy diagrams, the visual flow already reads clearly without them.
- Emphasis elements (a "current/now" marker, an outlier data point): fill with `--rg-blue` or a tint background plus accent border, not just a color swap, so it reads clearly at a glance.
- Wrap every diagram in a `<figure>` with a `<figcaption>` stating the takeaway in one sentence, someone skimming should get the point from the caption alone. Set `role="img"` with a full `aria-label` on the `<svg>` describing what it shows, since screen readers can't parse SVG shape data.
- Pick a real, verifiable metric to visualize (team scale, timeline overlaps, architecture structure) rather than an invented "impact score" or an axis nobody could define precisely. If you can't say exactly what a chart's axis or size difference represents, don't ship it. Red-team it first.
- Build and preview every diagram before calling it done. Markup that looks correct doesn't always render correctly (see the blank-line pitfall above), so verify in a real browser, not just by reading the source.

---

## Deliverable-Specific Notes

**redfearnb.github.io portfolio (dark mode, identity layer)**
Primary accent `--rg-red` throughout: borders, CTAs, live badges, gradient bars (red→tawny). Gape yellow reserved for the hero log only. Cream for all body text.

**redfearn.group (light mode, identity layer)**
Cream background, blue body text, `--rg-red` for CTAs, eyebrows, contact section background. Tawny as warm secondary. No gape yellow on light backgrounds.

Validated hybrid pattern (shipped and tested): a dark blue hero band (matching the dark-mode portfolio hero, including the ambient log) at the top of the homepage, transitioning into the light cream body for every section below. This gives the page a strong opening moment without abandoning the light-mode identity that the rest of the site, and every other deliverable type, is built on. Use this specifically for redfearn.group's homepage hero; interior pages (About, Work, Contact, case studies) stay fully light mode throughout.

**Case studies, reports, dashboards (light mode, content layer)**
Use the status/callout system as the primary structural device. Cinnamon/ember for section labels and featured metrics, tawny for metric panels, green for positive KPIs, red reserved for genuinely critical/alert states only. Don't dilute it by overusing the identity-layer red here.

**GitHub project repos and real working applications (dark mode, Product layer)**
These are portfolio evidence that Brady ships working software, so they are held to the same brand standard as the site, not treated as throwaway utilities. Requirements, confirmed live on garage-log and home-log as of 2026-07-25:
- Vendor `brand.css`, add the drift-check workflow, set `class="app-layer"` on `<html>`.
- Favicon is `rg-mark.svg` (the icon-avatar-safe construction). Never ship a framework default favicon.
- **Header carries the full wide lockup, not the bare mark.** Use `logo-wide-dark.svg` (Red and Cream scheme, self-contained on any surface), the same file the site's footer already uses, at the `305x50` display size the minimum-size formula in `logo-system.md` calls for. The app name sits beside it as a small tracked mono label (`.site-brand__app`: 0.75rem, JetBrains Mono, `--text-muted`) after a vertical divider, not as the page's actual heading. An earlier version of this rule said the bare `rg-mark.svg` belonged in the header too; that was superseded once the full lockup shipped, since a bare 26px mark plus plain text read as a different, unbranded product next to the site and the other app.
- **The header brand link is `<h1>`, so every page's own title is `<h2>`.** In-page card or section headers follow at `<h3>`, and anything nested deeper (a governance page's phased policy sub-sections, for instance) at `<h4>`. This falls directly out of the previous bullet (the header carries a real heading, not a styled `<div>`) plus the never-skip-a-level rule below, but the two are easy to leave unconnected: a new property built without stating this outright gave every page its own `<h1>` and left the header with no heading at all, the inverse of garage-log/home-log's pattern, and it wasn't caught until an explicit cross-repo audit (2026-07-29).
- **Footer carries the lockup and a bottom bar**, matching the site: `logo-lockup-dark.svg` linking to redfearn.group, then a bottom bar (`.site-footer__bottom`) with `REDFEARN GROUP · EST. 2014 · SPANISH FORK, UT` on one side and the copyright line on the other, in JetBrains Mono at the 0.75rem floor.
- **Content container matches the site's width**, `1180px`, not an app-specific value. Garage-log and home-log both used `1000px` before this was caught; there was no reason for the divergence, so treat 1180px as the shared convention going forward rather than something each property picks independently.
- **Use the `eyebrow` kicker above primary page headings** (dashboard, archive/list views, detail-page titles), the same small mono label-plus-rule component the site uses before its headings. Label it with the page's role (`Dashboard`, `Archive`, `Vehicle`/`Item`), not the app name, since the header already carries the app name.
- Dark unconditionally. No `prefers-color-scheme` branch.
- App-specific components live in the property's own stylesheet and use their own class names. Do not redefine `--rg-*` or `--status-*` there.
- Real actions (a print/export trigger, not a navigational link) use `.btn-ghost-dark`, brand.css's existing dark-surface secondary button, rather than an unstyled native `<button>`.
- The README is public-facing brand copy. Apply the voice rules to it, including the em-dash rule.
- Repo description and topics are brand surfaces too, and they show up in search and on the profile.

**React artifacts / dashboards**
Set tokens as CSS custom properties on `:root`. Default to dark mode for portfolio-adjacent tools, light mode for reports/analysis tools.

**Slides**
Dark mode preferred. Red for branded title/dividers (identity layer). Gape yellow for data callouts. Green/tawny/ember for status-driven content slides.

---

## Implementation Pitfalls

Hard-won lessons from actually shipping full sites with this system. Read before building any interactive web artifact, not just a static mockup.

- **Shared class names collide across layers.** `brand.css` and a property's own stylesheet can both define `.card`, `.tag`, or `.section-label`, and the later sheet only overrides the properties it actually sets. Pseudo-elements are the trap: `.section-label::after` in `brand.css` draws an 80px rule, and an app that reused the class for a compact card label inherited a stray grey line it never asked for, because its own rule set no `::after`. If a component in an app is not the same component as the one on the site, give it a different class (`.card-label`, not `.section-label`). Reserve the shared names for genuinely shared components.
- **Copying a stylesheet from a sibling repo is how drift starts.** home-log was built by copying garage-log's CSS, which had itself drifted from the site. Neither matched, and both shipped Astro's default favicon for weeks, a 1000px content container instead of the site's 1180px, and a bare `rg-mark.svg` in the header instead of the full lockup. Vendor `brand.css` and add the drift-check workflow instead. Every new property gets `rg-mark.svg` as its favicon, `logo-wide-dark.svg` in its header, and the site's `1180px` container width, never framework defaults or an app-specific guess.
- **Raw palette tokens do not adapt across layers.** `var(--rg-red)`, `var(--rg-mist)`, `var(--rg-green)` are fixed light-mode values. Inside `.app-layer` they render as muddy or glaring. Use the semantic tokens (`--status-*-fg`, `--border`, `--text-muted`, `--accent`) anywhere a value must change with the layer, and reserve raw palette references for genuinely fixed decorative uses like the skip-link fill. Lowering a raw value's opacity does not fix this, and can make it worse: `rgba(10,17,40,0.35)` (`--rg-blue` at 35%) used directly as an icon color reads fine on a light card and goes nearly invisible on `.app-layer`'s dark surface, since dropping an already-dark color's opacity against an already-dark background pushes it toward nothing rather than toward muddy. This exact mistake showed up independently in garage-log's and home-log's vehicle/item-type icons (confirmed 2026-07-29 by measuring contrast in a running dev server, not just reading the CSS), which is a sign it's an easy trap rather than a one-off. `--text-muted` already carries the right icon color for each layer; reach for it before hand-picking an opacity on a raw hex.
- **`backdrop-filter` breaks `position: fixed` children.** Any element with `backdrop-filter`, `filter`, `transform`, or `will-change` set becomes a new containing block for descendants that are `position: fixed`, per the CSS spec. A frosted sticky nav (`backdrop-filter: blur()`) containing a fixed-position mobile menu will silently collapse that menu's height, since it's now sized relative to the ~64px nav bar instead of the viewport. Fix: give the fixed child an explicit `height: 100vh` (or `calc(100vh - navHeight)`) instead of relying on `top`/`bottom` to compute height automatically.
- **Blank lines corrupt SVG embedded in Markdown.** If you write raw `<svg>...</svg>` directly inside a Markdown file (for a diagram, chart, or icon), don't put blank lines anywhere inside the block. Markdown parsers (including markdown-it) split an HTML block at the first blank line and wrap what follows in a stray `<p>` tag, which causes browsers to exit SVG parsing mode partway through and silently drop the rest of the diagram. Keep the entire SVG as one continuous block with zero internal blank lines, but make sure there is a blank line immediately before and after the whole block so surrounding Markdown (like a following heading) still parses correctly.
- **Respect `prefers-reduced-motion`.** Anything using the pulse or ambient-log-scroll animations needs a `@media (prefers-reduced-motion: reduce)` override that disables the animation.
- **Heading hierarchy: never skip a level.** h1 straight to h3 with no h2 in between is a common mistake whenever a visual "kicker" label (eyebrow, section-label) sits above a heading, since the kicker itself isn't a heading tag. If a section has no other heading, promote its kicker to a real heading (`<h2 class="section-label">`) instead of leaving it a `<div>`. If a section needs a heading purely for screen-reader structure but nothing worth showing visually, use a visually-hidden heading rather than skipping a level.
- **Add a skip-to-content link** on any full page build: one small CSS rule (visually hidden until focused) plus an anchor at the top of `<body>` pointing to `id="main"` on the `<main>` element.

---

## What to Avoid

- Aptos, or any Microsoft/M365-associated font: use the Space Grotesk / IBM Plex Sans / JetBrains Mono stack exclusively.
- Mixing identity-layer red with content-layer ember/cinnamon as if interchangeable: they're deliberately distinct.
- Using `--rg-ember` for body text fails WCAG at small sizes.
- Using `--rg-tawny` directly as text color anywhere, headings and word-cloud items included, not just tags: it fails WCAG at every size (~2.9-3.2:1). Use it as a background, border, or decorative accent instead, with the actual text in a safe token like `--rg-blue` or `--rg-cream` (see `.tag-tawny`'s accent-edge pattern).
- Using `--rg-gape` on light backgrounds fails contrast every time.
- More than one animated element per page.
- Pure `#000000` black or pure `#FFFFFF` white as primary tones: use `--rg-blue` and `--rg-cream`.
