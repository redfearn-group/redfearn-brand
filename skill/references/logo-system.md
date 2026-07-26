# Redfearn Group Logo System: Full Specification

The Redfearn Group identity is built from one canonical badge (the "RG"
monogram) and one wordmark ("REDFEARN GROUP"), combined into six layouts
(lockup, wide, stacked, wordmark-only, icon-only, icon-avatar-safe) and
produced in a growing set of color schemes (§4). Every letterform, in every
file, is a real vector glyph outline extracted from the actual font files.
Nothing is live `<text>` with a `font-family` reference. This matters because
standalone SVG files (favicons, logo files, email signatures) do not reliably
load webfonts, and a font-loading failure silently falls back to a system
font, breaking the brand. Extracting outlines once removes that failure mode
permanently.

**Icon-only is deprecated, use icon-avatar-safe instead.** Icon-only (the
bare 100x100 badge, letters flush to the edges) was the original square-icon
construction and is what the currently-live `rg-mark.svg` still uses. It has
a confirmed bug: rendered through an actual circular crop mask (the kind
almost every avatar/app-icon system applies), the R glyph's left stroke gets
clipped clean off. Icon-avatar-safe fixes this by insetting the same
unmodified badge inside a larger transparent-margin canvas (§3). Icon-only's
files are being retired, not maintained going forward; don't generate new
ones or point new placements at it.

## 1. The canonical badge

The "RG" monogram is a fixed piece of artwork: a `100 x 100` square, `rx="8"`
rounded corners, solid `--rg-red` (`#BF1E2E`) fill, with the letters R and G
rendered as cream (`#F7F4EF`) Space Grotesk Bold vector paths positioned by
these exact transforms:

```
R: translate(-1.4960,79.1455) scale(0.083273,-0.083273)
G: translate(45.8697,79.1455) scale(0.083273,-0.083273)
```

This exact badge (rect + these two transforms + these two path strings) is
reused verbatim, unmodified, in every layout below. Never redraw or
re-derive it. Never letter-space, skew, or resize the R and G independently
of each other. If a new size is needed, wrap the whole badge group in an
outer `<g transform="translate(x,y) scale(s)">` and scale it as a unit,
exactly as the lockup and stacked layouts do.

## 2. The wordmark

"REDFEARN" is Space Grotesk Bold at 0.98x natural glyph advance (slightly
tightened tracking). "GROUP" is JetBrains Mono Medium, natural monospace
advance plus 0.30em extra tracking (letters spread apart, matching a
tracked small-caps look). GROUP is always the visually secondary line,
smaller than REDFEARN in every scheme. In the light and dark schemes,
REDFEARN and GROUP share the same solid color at full opacity; the
hierarchy there comes from size and typeface contrast alone, not color
or opacity.

The two words are never set in the same typeface. This contrast (display
serif-adjacent bold vs. tracked mono) is intentional and load-bearing for
the mark; do not substitute a single-family wordmark.

## 3. The six layouts

| Layout | ViewBox | Badge | Wordmark | Use for |
|---|---|---|---|---|
| **Lockup** (`logo-lockup*.svg`) | `0 0 517 120` | Left, 96px | Right, stacked REDFEARN over GROUP | Site footer, letterhead, email signature, wide horizontal placements |
| **Wide** (`logo-wide*.svg`) | `0 0 733 120` | Left, 96px | Right, REDFEARN and GROUP on one baseline-aligned row | Nav bars, document headers, letterhead, banners, anywhere there's plenty of horizontal room and the wordmark should read at close to full badge height rather than tucked into two smaller stacked lines |
| **Stacked** (`logo-stacked*.svg`) | `0 0 334 224` | Top-center, 96px | Below, centered, REDFEARN over GROUP | Square/vertical contexts: social profile photos, app-style icons, narrow sidebars, business card backs |
| **Wordmark-only** (`wordmark-only*.svg`) | `0 0 374 115` | None | Centered, REDFEARN over GROUP | Contexts where the badge appears separately nearby (e.g. paired with a favicon in a browser tab), or where a text-only mark reads cleaner: document headers, slide footers |
| **Icon-only** (`icon-*.svg`) — **deprecated** | `0 0 100 100` | The badge alone, flush to the edges | None | Not for new placements. Clips on circular crops (verified). Kept only as a historical record of the bug; use icon-avatar-safe below instead. |
| **Icon-avatar-safe** (`icon-avatar-safe-*.svg`) | `0 0 190 190` | The same unmodified badge, inset with a 45px transparent margin on every side | None | Favicon, app icon, social avatar, PWA/maskable icon, watermark base, anywhere the badge might get cropped into a shape you don't control |

**Why icon-avatar-safe is 190x190, not just "padded a bit":** this isn't a
cosmetic margin, it's sized against Google's own maskable-icon spec
(web.dev/articles/maskable-icon): only the central circle with radius = 40%
of the *canvas* width is guaranteed visible once Android/Chrome (or any
avatar system) applies its own mask shape. The 100x100 badge's corner sits a
fixed `100 * sqrt(2)/2 ≈ 70.7` units from center, a distance padding alone
doesn't shrink, so the canvas has to be wide enough that 40% of *its* width
clears 70.7: `70.7 / 0.4 ≈ 176.8` minimum. 190 (pad=45 per side) clears that
with a ~7% margin, verified both by calculation and by rendering the actual
file with the safe-zone overlay and pixel-measuring the badge's corners
(189.5 units from center, against a 204.8-unit safe radius at 512px export
size). An earlier pad=20 (140x140 canvas) fixed a smaller, different bug
(the flush icon-only badge's own corners clipped by a circle inscribed in
its *own* 100x100 square) but was never checked against Google's actual
maskable-icon math, where the safe circle is relative to the whole canvas,
not the badge; at 140x140 the safe radius is only 56, well short of the
badge's fixed 70.7, so it still visibly clipped under a real maskable
overlay. If the badge ever needs to look larger on a specific platform that
you know for certain never applies a shape mask, that's a deliberate
zoom/crop decision to make at upload time on that platform, not a reason to
regenerate this file smaller.

**Wide vs. lockup:** both put the badge on the left, and both are the
layout to reach for on a horizontal placement. The difference is purely
proportion. Lockup keeps REDFEARN and GROUP stacked in two lines so the
whole mark stays compact (56px REDFEARN cap height against a 96px badge,
roughly the same visual weight the R/G lettering has inside its own
badge). Wide spreads REDFEARN and GROUP across one line instead, which
frees up the vertical room to size REDFEARN much closer to the badge's
full height (64px cap height against the same 96px badge) at the cost of
needing significantly more horizontal space, hence the name. Reach for
wide when the container is wide and short (a nav bar, a letterhead
strip); reach for lockup when the container is narrower or roughly square.

Do not invent a fifth layout (e.g. wordmark-left-badge-right, or a
horizontal single-line wordmark) without extending this spec first. Every
layout here has been checked for wordmark legibility against its target
placement, and an ad hoc layout skips that check.

## 4. The color schemes

`red` is the actual minimal source file for every layout: single red ink,
everything else genuinely transparent (a true knockout mask, not a baked-in
fill). `light` and `dark` are not separately-maintained files anymore in the
review gallery, they're `red`'s knockout demonstrated on a cream background
(pixel-identical to the old opaque `light` file) and a two-tone opaque
construction demonstrated on a dark background, respectively. The generator
script keeps `light`/`dark`/`light-group-blue` as internal scheme keys for
other two-tone uses even though the gallery presents them under different
names (Red / Red and Cream / Red with Group Blue); see the scheme table
below for the mapping.

| Scheme (gallery name) | Generator key | Badge | REDFEARN | GROUP | Use on |
|---|---|---|---|---|---|
| **Red** | `red` | Transparent knockout, `--rg-red` ink | `--rg-red` `#BF1E2E` | `--rg-red` `#BF1E2E` | The primary file. Anywhere you control the backdrop, especially light/neutral surfaces. |
| **Red and Cream** | `dark` | Full color (opaque, self-contained) | `--rg-cream` `#F7F4EF` | `--rg-cream` `#F7F4EF` | Anywhere you *don't* control the backdrop (embeds, third parties); self-contained so it's safe on any surface. Currently the live favicon/nav/footer construction. |
| **Reverse Cream** | `reverse` | Transparent knockout, `--rg-cream` ink | `--rg-cream` `#F7F4EF` | `--rg-cream` `#F7F4EF` | Brand-red panels, photos, colored/dark backgrounds where the transparency lets the surface read as the mark's "white." |
| **Black & White** | `bw` | **Opaque two-tone**: solid black badge, genuine white (not cream) letterforms | `#000000` | `#000000` | Use *only* when no other color is available in the reproduction method itself: a newspaper ad, a single-color photocopy, a stamp or engraving. Not a stylistic choice, a fallback. |
| **Red with Group Blue** | `red-group-blue` | Transparent knockout, `--rg-red` ink | `--rg-red` `#BF1E2E` | `--rg-blue` `#0A1128` | Adopted for the site nav/header (`wide` layout) on light backgrounds. Brady's preferred header treatment. |
| **Watermark** *(candidate, not adopted)* | `watermark` | Transparent knockout, `--rg-blue` ink, 6% opacity | `--rg-blue` `#0A1128`, 6% opacity | `--rg-blue` `#0A1128`, 6% opacity | Low-opacity decorative use only (slide backgrounds, report covers). Never a primary mark, never at small/favicon sizes. |

**Black & White changed construction on purpose.** It used to be a
single-black-ink knockout (letters cut out as transparent holes), same
technique as Reverse, but that only actually reads as "black and white" over
a literal white surface, anywhere else it shows whatever backdrop is behind
it. It's now an opaque two-tone construction instead, a real black fill and
a real white fill, so it reads as black-and-white on any backdrop. This is
the one scheme that intentionally does *not* use the knockout technique
below, despite being single-ink in spirit.

**Rejected: outlined letterforms (tried on purpose, then removed on purpose).**
A "red outline" and "white outline" scheme were built and evaluated: naked
R/G or REDFEARN/GROUP letterforms with a solid fill and a contrasting
stroke traced around every letter, no badge square, meant for placement
over photos or textured backgrounds. Brady reviewed them side by side
against the full-color-blocked schemes above and rejected them outright,
full-color blocking (a solid badge, a solid wordmark) reads as a more
confident, professional identity mark; outlined letters read closer to a
garment-print or vinyl-decal treatment, wrong register for an executive
personal brand. This was a deliberate, reviewed decision, not an oversight.
Do not regenerate an outline scheme without Brady explicitly asking for it
again. `scripts/generate_logo_variant.py` no longer implements outline
mode at all, the code was removed along with the scheme.

**Rejected: three GROUP-color candidates (tried on purpose, then removed
on purpose).** While comparing GROUP-color treatments against the Light
and Dark defaults, three specific combinations were built, reviewed side
by side in a comparison gallery, and rejected. Do not rebuild any of
these without Brady explicitly asking for them again:
- **Light, GROUP grey** (REDFEARN red, GROUP `--rg-ash`, light background)
- **Light, monochrome blue** (REDFEARN and GROUP both `--rg-blue`, full
  opacity, the direct blue counterpart to the all-red Light default)
- **Dark, GROUP grey** (REDFEARN cream, GROUP `--rg-ash`, dark background)

**Dark, GROUP blue was never built at all**, and isn't a candidate to
revisit either: GROUP in `--rg-blue` on the Dark scheme's `--rg-blue`
background would be the exact same color as the background and render
invisible, so that combination was rejected before a single file was
generated.

**Red with Group Blue has been decided: adopted for the header.** Brady
reviewed it against the all-red default and preferred it for the site
nav/header on light backgrounds. It's now live there (`wide` layout,
generator key `red-group-blue`; REDFEARN and badge stay `--rg-red`
knockout, GROUP overrides to `--rg-blue`; genuine transparent knockout
file, same technique as Red, not the older opaque two-tone version this
was first tried as). It has not been extended to any other layout or
placement (footer, favicon, etc. still use Red or the avatar-safe
construction) — treat it as header-specific unless told otherwise.

**Never reuse light-mode colors on a dark surface.** `--rg-blue` text is
close to invisible on a `--rg-blue` background; this is why dark is a distinct
scheme; not just "light-mode file on a dark div."

**Reverse Cream, Black & White, and Red are not interchangeable.** Reverse
Cream is cream ink and is meant for a colored or photographic surface.
Black & White is opaque black-and-white and is meant for contexts with no
color available at all in the reproduction method itself (see §4's note on
why it's opaque, not knockout). Red is a single-ink knockout where the
brand color itself should carry. If unsure which one a new request needs,
ask what surface or reproduction method the logo is going onto, and whether
any color at all is available.

### The knockout technique (reverse and red only; not black & white)

Reverse (and Red) variants do not fill the R and G paths with a
color. Instead they use an SVG `<mask>`: a full-color rect is masked by a
white rect with the R/G paths painted black inside it, so the letterforms
become a true transparent hole through the badge shape rather than a
separately-colored fill. Black & White deliberately does not use this
technique anymore (§4); it's the one "single-ink-in-spirit" scheme built as
opaque two-tone instead:

```xml
<defs>
  <mask id="rgKnockoutExample" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100">
    <rect x="0" y="0" width="100" height="100" fill="#ffffff"/>
    <g fill="#000000">
      <g transform="translate(-1.4960,79.1455) scale(0.083273,-0.083273)"><path d="..."/></g>
      <g transform="translate(45.8697,79.1455) scale(0.083273,-0.083273)"><path d="..."/></g>
    </g>
  </mask>
</defs>
<rect x="0" y="0" width="100" height="100" rx="8" fill="INK_COLOR" mask="url(#rgKnockoutExample)"/>
```

This is the correct professional approach for a single-ink mark: it
survives conversion to true one-bit black and white, and it means the
letterforms show the background through them rather than covering it with
a second flat color. Do not build reverse/bw variants by simply changing
the badge fill to a solid color and the RG fill to a contrasting solid
color; that is a two-color mark, not a single-ink mark, and will not
reproduce correctly on a single-ink press.

Each SVG that uses this technique needs its own unique mask `id` if more
than one masked element might ever appear on the same page (e.g. an icon
and a lockup both embedded inline in one document): collisions between
same-ID masks in the same DOM will silently break one of them. The
generator script (`scripts/generate_logo_variant.py`) already assigns a
distinct id per layout (`rgKnockoutLockup`, `rgKnockoutStacked`,
`rgKnockoutIcon`, etc.); preserve that convention if hand-editing.

## 5. Minimum size and clear space

**The checkable rule (do this, not the rough width guesses below):**
GROUP's rendered on-screen height must be at least 12px, matching the
Minimum Text Size floor in SKILL.md. Compute it before shipping any new
placement:

```
GROUP on-screen height = gr_cap_px x (display_height / native_viewBox_height)
```

`gr_cap_px` and the native viewBox height come from `LAYOUTS` in
`generate_logo_variant.py` (currently 25-29px depending on layout, against
a native viewBox height of 120-224px depending on layout). If the result
is under 12px, don't ship it at that size: enlarge the placement until it
clears 12px, or use a layout without a shrinking secondary tier
(icon-avatar-safe has no wordmark to worry about).

Two worked examples from the live site, both clear the floor by a hair,
rounded up rather than down on purpose:
- **Nav** (`wide` layout, GROUP native 29px, viewBox height 120px): needed
  50px display height -> GROUP renders at 29 x (50/120) = 12.08px.
- **Footer** (`lockup` layout, GROUP native 25px, viewBox height 120px):
  needed 58px display height -> GROUP renders at 25 x (58/120) = 12.08px.

**Rough width floors, as a faster sanity check once you know a layout's
usual proportions:**
- **Icon-avatar-safe**: do not render below 16px square. Below that the R/G
  strokes begin to merge. 32px is the practical minimum for on-screen
  legibility; the favicon/app-icon exports ship dedicated PNGs at Google's
  own manifest sizes (192/384/512/1024/2048px, §9) specifically so nothing
  has to be upscaled from something small.
- **Lockup / wide**: do not render below roughly 145px wide (matches the
  46-53px display heights above). Always verify with the height formula
  before trusting a width guess at a new aspect ratio.
- **Stacked / wordmark-only**: do not render below roughly 105px wide, for
  the same reason.
- **Clear space**: leave at least the badge's own corner-radius (8% of the
  badge's rendered size) of empty space on all sides of any variant. None
  of the shipped files include outer margin in their viewBox beyond the
  small `pad` built into the composition; treat that `pad` as the *minimum*
  clear space, not decorative, when placing a logo file into a layout that
  adds its own container padding.

## 6. Do's and don'ts

**Do:**
- Use the SVG source files as the source of truth; the PNG exports exist
  only for contexts that cannot render SVG (email clients, favicon/app-icon
  and social-avatar upload pipelines, web app manifests).
- Pick the scheme by what's actually behind the logo, not by what's
  "close enough" (see §4).
- Regenerate variants from `scripts/generate_logo_variant.py` (§8) rather
  than hand-editing an existing SVG's transforms, whenever a new size or
  combination is needed.

**Don't:**
- Don't recolor the badge's red square. It is not a token to swap; a
  differently-colored badge is a different brand.
- Don't stretch any variant non-uniformly (different X and Y scale
  factors). Every transform in every shipped file uses matching absolute
  values for the X and Y scale (`scale(s,-s)`); breaking that distorts the
  letterforms.
- Don't set REDFEARN and GROUP in the same weight or the same typeface.
- Don't add a tagline, year, "™", or any other element into a logo file.
  If a placement needs a tagline, set it separately in body copy near the
  logo, not baked into the SVG.
- Don't use `filter`, `drop-shadow`, gradients, or outlines on any logo
  variant. The mark is flat color by design.

## 7. The data behind every variant

`assets/logo-glyph-paths.json` (bundled with this skill) contains the
complete pre-extracted vector data: every glyph's SVG path, advance width,
and bounding box, for both the badge letters (R, G in Space Grotesk Bold)
and every letter used in the wordmark (REDFEARN in Space Grotesk Bold,
GROUP in JetBrains Mono Medium). It was generated once via `fontTools`
(`instantiateVariableFont` to pin the exact weight, then `SVGPathPen` and
`BoundsPen` to extract outlines and metrics) from the real Google Fonts
variable font files. Coordinates are in font units (1000 units/em), Y-up,
origin at baseline; flip Y when placing into an SVG, which is Y-down.

This file means no future variant needs a font file, `fontTools`, or a
Python font-processing environment. It's pure geometry data plus a Python
script that lays it out; regenerating a variant is a data-and-math
problem, not a font-extraction problem.

## 8. Generating a new variant

`scripts/generate_logo_variant.py` (bundled with this skill) reads
`assets/logo-glyph-paths.json` and can produce any of the six layouts in
any of the canonical or candidate schemes:

```
python scripts/generate_logo_variant.py <layout> <scheme> <output.svg>

layout: lockup | wide | stacked | wordmark-only | icon-only | icon-avatar-safe
scheme: red | dark | reverse | bw | light | light-group-blue | red-group-blue | watermark
```

`icon-only` still generates (kept so the historical/buggy construction can
be regenerated for reference), but don't use its output for anything new;
see §3. `light` and `light-group-blue` are the internal two-tone keys the
gallery no longer surfaces as their own columns (§4) — reach for `dark` or
`red-group-blue` instead unless you specifically need the old opaque
construction.

Examples:

```
python scripts/generate_logo_variant.py lockup dark redfearn-group-lockup-dark.svg
python scripts/generate_logo_variant.py wide red-group-blue redfearn-group-wide-red-group-blue.svg
python scripts/generate_logo_variant.py stacked reverse redfearn-group-stacked-reverse.svg
python scripts/generate_logo_variant.py icon-avatar-safe bw redfearn-group-icon-avatar-safe-bw.svg
```

An outline-mode scheme existed at one point and was fully removed from the
script after being rejected (§4-adjacent decision, see the rejected
outlined-letterforms note above); don't reintroduce it without being asked.

This reproduces the exact geometry of every shipped variant. To change
proportions, badge size, cap heights, gaps, or padding, edit the `LAYOUTS`
dict near the top of the script, not the generated SVG output, and
regenerate.

**If a genuinely new layout is needed** (not one of the six above), the
math to write is: (1) load `redfearn`/`group` letter arrays from the JSON,
(2) lay each word out left-to-right by summing `advance * tighten +
extra_tracking` per letter to get x-offsets and combined bounds, (3) pick a
target cap-height in px and derive `scale = target_px / cap_height_font_units`
(700 for Space Grotesk, 730 for JetBrains Mono), (4) place each glyph with
`translate(origin_x + (x_offset - bounds.minX) * scale, baseline_y)
scale(scale, -scale)`. This is exactly what `generate_stacked` and
`generate_wordmark_only` in the script do; read those two functions as the
reference implementation before writing a new one.

**If the underlying fonts ever change** (e.g. the design system moves off
Space Grotesk or JetBrains Mono), `assets/logo-glyph-paths.json` must be
regenerated from the new font files first; the generator script consumes
whatever is in that JSON, so it will silently keep producing outlines in
the old typeface until the JSON is rebuilt. There is no automated
extraction script bundled for this (it depends on which fonts are
downloaded and their exact file layout at the time), but the working
method is documented in this file's own history: download the variable
font file, use `fontTools.varLib.instancer.instantiateVariableFont` to pin
the exact weight, then `fontTools.pens.svgPathPen.SVGPathPen` and
`fontTools.pens.boundsPen.BoundsPen` per glyph to get `path`/`advance`/
`bounds`, matching the shape already in the JSON.

## 9. File inventory

A red-outline/white-outline scheme was built and shipped at one point, then
deliberately removed after review, see §4; if you find old
`*-red-outline.svg` / `*-white-outline.svg` files anywhere outside version
control history, they're stale and should be deleted, not treated as
current. Same for any flush `icon-*`/`favicon-*` (non-avatar-safe) PNG or
SVG file you find outside version control history: icon-only is deprecated
(§3), those files were deliberately deleted from Downloads and site assets
once icon-avatar-safe replaced them, don't treat any copy of them you find
elsewhere as current.

**Master exports — canonical source: `https://github.com/redfearn-group/logo-variant-review`
(private repo).** This is the durable reference for every rendered file;
treat it as the source of truth for "does this exact export already exist,"
not any local folder. It's organized into six subfolders by layout:
`icon-avatar-safe/`, `lockup/`, `wide/`, `stacked/`, `wordmark-only/`, and
`favicon-app-icon/` (a duplicate copy of `icon-avatar-safe/`'s files, kept
as its own folder purely so the repo's folder structure mirrors the review
gallery's six visual rows one-for-one — it's not a distinct construction).
Within each folder, files keep the `redfearn-group-<layout>-<scheme>-final`
naming convention (e.g. `redfearn-group-lockup-dark-final.svg`,
`redfearn-group-icon-avatar-safe-red-final.svg`), SVG plus PNG at every
needed resolution. Icon/favicon-type layouts (icon-avatar-safe) export PNGs
at Google's own web-app-manifest recommended sizes: 192, 384, 512, 1024px,
plus a 2048px "giant master" for headroom, per Google's own guidance ("if
you need to pick only one icon size, it should be 512x512; providing more
sizes is recommended including 192, 384, and 1024"). Wordmark-bearing
layouts (lockup/wide/stacked/wordmark-only) export the same five-size set,
width-scaled with native aspect ratio preserved, plus their original
2x-native "master" PNG kept for backward compatibility with existing
placements. It intentionally excludes the deprecated icon-only files.
`redfearn-group-favicon-final.ico` (in both `icon-avatar-safe/` and
`favicon-app-icon/`) packs 16/32/48/64px PNG frames of the Red and Cream
avatar-safe construction into one legacy `.ico` container, for browsers and
OS bookmark bars that request `/favicon.ico` directly. The repo's own
`README.md` has the folder-mapping table if this doc and the repo ever
drift.

A local Downloads-folder copy of these same six subfolders may also exist
on Brady's machine as a working/scratch copy, but it is not authoritative:
it's local, gets reorganized or cleaned up independent of this skill, and
should never be treated as the reference for "does this file exist" or
"what's the latest version" — always resolve against the GitHub repo above
instead. When adding a new scheme or layout's export, commit and push it
into the matching subfolder of that repo; a local-only copy isn't
considered saved.

**Site copies — canonical source: `https://github.com/redfearn-group/redfearn-group.github.io`
(the live site's own repo, deployed to redfearn.group on every push to
`main`).** These live under `src/assets/`, under shorter names
(`icon-red.svg`, `logo-lockup-red.svg`, etc), distinct from the master
exports above because the site only needs one file per layout/scheme
combination actually in use, not the full export matrix. `rg-mark.svg`,
`favicon-32.png`, and `apple-touch-icon.png` point at the icon-avatar-safe
construction (not the deprecated flush icon-only), and `icon-192.png`/
`icon-512.png` were added alongside a `site.webmanifest` for PWA/maskable-icon
support, linked from `base.njk`. `favicon.ico` (16/32/48/64px packed into one
container, same avatar-safe construction) is also linked from `base.njk` as
a legacy fallback, for browsers/OS bookmark bars that request `/favicon.ico`
directly instead of reading `<link rel="icon">` tags. The nav/header
(`logo-wide-red-group-blue.svg`) uses the Red with Group Blue scheme (§4);
the footer (`logo-lockup-dark.svg`) uses the opaque Red and Cream scheme
(generator key `dark`), appropriate there since the footer sits on a dark
`--rg-blue` background and Red and Cream is the self-contained,
any-backdrop-safe construction. Resolve against this repo (not
a local clone's working tree, which can have uncommitted or stale changes)
before assuming this doc describes what's actually live — this doc is
updated as changes land, not generated from the repo automatically.

**App copies — canonical source: same master exports repo as above, `wide/`
and `lockup/` folders, `dark` scheme.** garage-log and home-log
(`redfearn-group/garage-log`, `redfearn-group/home-log`) each vendor two
files straight from the master exports into their own `public/`:
`redfearn-group-wide-dark-final.svg` (renamed `logo-wide-dark.svg` on disk)
in the header at `305x50` display size, and
`redfearn-group-lockup-dark-final.svg` (renamed `logo-lockup-dark.svg`) in
the footer at `250x58`, both worked examples in §5's minimum-size table.
Both apps use the opaque Red and Cream scheme for the same reason the
site's footer does: it is self-contained on any backdrop, appropriate on
the unconditionally-dark Product-layer surface these apps render on.
`rg-mark.svg` (icon-avatar-safe, Red and Cream) remains the favicon in both
apps; it is not also the header mark. This was a live correction, both
apps originally shipped a bare `rg-mark.svg` plus plain text in the header
with no footer lockup at all, caught and fixed 2026-07-25 (see the
workspace-level `redfearn-group-style` skill's Deliverable-Specific Notes
for the full requirement list this produced). Treat this pairing, wide
lockup in the header, lockup in the footer, both `dark` scheme, both
sized per §5, as the standard for any future GitHub project repo, not
something to re-derive per property.

When exporting a new PNG from any SVG here, render at the target resolution
directly from the vector source (or at minimum 4x the target display size
and downscale), never upscale a small raster, to avoid visible aliasing on
the thin strokes in GROUP's mono letterforms.
