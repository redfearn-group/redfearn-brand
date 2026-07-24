#!/usr/bin/env python3
"""
Redfearn Group logo variant generator.

Regenerates any lockup/stacked/wordmark-only/icon-only SVG in any established
color scheme from the pre-extracted glyph data in
../assets/logo-glyph-paths.json. No font files or fontTools needed at
generation time; that extraction already happened once and is baked into
the JSON.

Usage:
    python generate_logo_variant.py <layout> <scheme> <output.svg>

    layout: lockup | wide | stacked | wordmark-only | icon-only
    scheme: light | dark | reverse | bw | red

    An outlined-letterform scheme (red-outline/white-outline) was built and
    evaluated, then deliberately removed after review: full-color blocking
    reads as a more confident, professional identity mark for this brand.
    Do not reintroduce outline mode without being asked for it again.

Examples:
    python generate_logo_variant.py lockup dark redfearn-group-lockup-dark.svg
    python generate_logo_variant.py wide light redfearn-group-wide-light.svg
    python generate_logo_variant.py stacked reverse redfearn-group-stacked-reverse.svg
    python generate_logo_variant.py icon-only bw redfearn-group-icon-bw.svg

To change proportions (cap heights, gaps, padding) edit the LAYOUTS dict
below rather than hand-editing generated SVG output; regenerate instead.
"""
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
GLYPH_DATA_PATH = SKILL_DIR / "assets" / "logo-glyph-paths.json"

RG_RED = "#BF1E2E"
RG_BLUE = "#0A1128"
RG_CREAM = "#F7F4EF"
RG_BLACK = "#000000"
RG_WHITE = "#FFFFFF"
RG_ASH = "#676E7C"

# Native badge artwork: 100x100 viewBox, rx=8 rounded rect + R/G glyph paths.
# This exact geometry is the canonical badge, reused verbatim in every variant.
BADGE_R_TRANSFORM = "translate(-1.4960,79.1455) scale(0.083273,-0.083273)"
BADGE_G_TRANSFORM = "translate(45.8697,79.1455) scale(0.083273,-0.083273)"

# Per-layout composition geometry, in final SVG px units. These are the exact
# values used to build the shipped variants; change here and regenerate
# rather than hand-editing output SVGs.
LAYOUTS = {
    "lockup": dict(
        badge_size=96, pad=12, gap=24, line_gap=13,
        rf_cap_px=56, gr_cap_px=25,
    ),
    "wide": dict(
        # Single row: badge, then REDFEARN and GROUP baseline-aligned on the
        # same line rather than stacked. rf_cap_px is deliberately close to
        # badge_size so the wordmark reads as tall as the badge itself.
        badge_size=96, pad=12, gap=24, word_gap=20,
        rf_cap_px=64, gr_cap_px=29,
    ),
    "stacked": dict(
        badge_size=96, pad=14, gap=22, line_gap=11,
        rf_cap_px=46, gr_cap_px=21,
    ),
    "wordmark-only": dict(
        pad=14, line_gap=12,
        rf_cap_px=52, gr_cap_px=23,
    ),
    "icon-only": dict(),
    # Same canonical 100x100 badge as icon-only, unchanged, inset inside a
    # larger canvas with a transparent margin, sized to clear Google's own
    # maskable-icon safe zone (web.dev/articles/maskable-icon): only the
    # central circle with radius = 40% of the canvas width is guaranteed
    # visible once Android/Chrome applies its own mask shape. The 100x100
    # badge's corner sits sqrt(2)/2*100 = ~70.7 units from center, a fixed
    # distance that doesn't shrink just by adding padding, so the canvas
    # has to be wide enough that 40% of ITS width clears that 70.7, not
    # the other way around: 70.7 / 0.4 = ~176.8 minimum. pad=45 (canvas
    # 190x190, badge at 52.6% of canvas width) clears that with a ~7%
    # margin, comfortably inside Android's own adaptive-icon foreground
    # ratio (66% of canvas) for reference. An earlier pad=20 (canvas 140)
    # only fixed a smaller, different bug (the flush icon-only badge's
    # own corners clipped by a circle inscribed in ITS OWN 100x100 square)
    # and was verified against that bug, not against Google's actual
    # maskable spec, where the safe-zone circle is relative to the whole
    # canvas: at canvas 140 the safe radius is only 56, well short of the
    # badge's fixed 70.7 corner distance, so the badge still visibly
    # clipped on both sides under the real maskable overlay. Confirmed by
    # rendering this construction with a maskable safe-zone overlay, not
    # just calculated.
    "icon-avatar-safe": dict(pad=45),
}

# GROUP's cap height is set to ~0.45x REDFEARN's across every layout (was
# ~0.36x). GROUP is still clearly the secondary/smaller word, but the old
# ratio put GROUP below any legible on-screen size once a variant was
# displayed small (a nav bar, a footer lockup): see the "Minimum Text Size"
# rule in SKILL.md. Whenever a variant is placed somewhere new, check
# GROUP's actual rendered pixel height there, not just the ratio here.

RF_CAP_FONT_UNITS = 700  # Space Grotesk Bold capHeight
GR_CAP_FONT_UNITS = 730  # JetBrains Mono Medium capHeight
RF_TIGHTEN = 0.98        # slight tightened tracking on REDFEARN
GR_EXTRA_TRACKING_EM = 0.30  # extra tracking added to GROUP's monospace advance

SCHEMES = {
    # "red" is the actual minimal source asset: single red ink, everything
    # else (canvas, badge letterforms) is genuine SVG transparency via a
    # true mask cutout, not a baked-in white/cream fill (verified by
    # rendering over non-cream test backdrops and confirming the backdrop
    # shows through). "light" is not a separate maintained file, it is
    # this same "red" file, shown applied on a light/cream background,
    # since a transparent letter-hole over cream and an opaque cream fill
    # render pixel-identical. Both keys are kept below because the
    # generator still needs "light" for other things that reuse its
    # opaque badge/wordmark (e.g. two-tone comparison candidates like
    # "light-group-blue"), but the gallery presents "red" as the primary
    # asset and "light" purely as red's applied-on-cream demonstration,
    # not as an independent file to maintain.
    #
    # dark and reverse are each their own genuinely distinct file: dark's
    # badge is the opaque canonical one (self-contained, same red+cream
    # regardless of backdrop), reverse's badge is a separate single-ink
    # cream knockout. Neither is reducible to the other or to red.
    #
    # An outlined-letterform mode (naked R/G or REDFEARN/GROUP shapes with a
    # fill + contrasting stroke, no badge square) was built and evaluated as
    # "red-outline"/"white-outline", then deliberately removed: Brady
    # reviewed it side by side against full-color blocking and rejected it,
    # outlined letters read closer to a garment-print/decal treatment than a
    # professional identity mark. Don't reintroduce it without being asked.
    "light": {"mode": "two-tone", "redfearn": RG_RED, "group": RG_RED, "group_opacity": 1.0},
    "dark": {"mode": "two-tone", "redfearn": RG_CREAM, "group": RG_CREAM, "group_opacity": 1.0},
    "reverse": {"mode": "knockout", "ink": RG_CREAM},
    # Opaque two-tone, not a knockout: a black badge with genuine white
    # (not cream) letterforms, plus solid black wordmark. Brady reviewed
    # the knockout alternative (single black ink, letters knocked out as
    # transparent holes, only reading as "black and white" over an actual
    # white surface) and chose opaque instead: the RG mark must read as
    # black AND white on any backdrop, not black and whatever-color-is-
    # behind-it. Uses RG_WHITE, never RG_CREAM, so it isn't mistaken for
    # the warm off-white used elsewhere in the system.
    "bw": {"mode": "two-tone", "redfearn": RG_BLACK, "group": RG_BLACK, "group_opacity": 1.0, "badge_fill": RG_BLACK, "letter_fill": RG_WHITE},
    "red": {"mode": "knockout", "ink": RG_RED},
    # Candidate under review, not yet part of the canonical five schemes:
    # same light-scheme badge and REDFEARN treatment, GROUP recolored for
    # comparison against the all-red "light" scheme above. Still open.
    # Superseded as the maintained file by "red-group-blue" below (same
    # relationship as "light" -> "red": this two-tone version is kept only
    # because the generator still needs a reference two-tone GROUP-blue
    # comparison; the gallery shows the knockout version instead).
    "light-group-blue": {"mode": "two-tone", "redfearn": RG_RED, "group": RG_BLUE, "group_opacity": 1.0},
    # Same candidate, but as a genuine transparent single-badge-ink source
    # file: badge and REDFEARN are knocked out in red exactly like "red"
    # above (identical badge geometry, since the badge cutout never carries
    # GROUP's color), but GROUP's wordmark fill overrides to blue via
    # "group_ink". Transparent everywhere except the red badge/REDFEARN ink
    # and the blue GROUP ink, verified the same way "red" was: render over
    # a non-cream backdrop and confirm it shows through. Still open.
    "red-group-blue": {"mode": "knockout", "ink": RG_RED, "group_ink": RG_BLUE},
    # Low-opacity single-ink version for large decorative background use
    # (slide backgrounds, report covers), not a primary logo placement.
    # Reuses the knockout composition (badge letters as a transparent
    # cutout) so the RG shape stays visible as a ghost impression instead
    # of collapsing into a single flat blob at low opacity. Still open.
    "watermark": {"mode": "knockout", "ink": RG_BLUE, "opacity": 0.06},
    # Rejected candidates, tried and reviewed on purpose, don't rebuild
    # without being asked again:
    # - "light-group-grey" (REDFEARN red, GROUP RG_ASH, light bg)
    # - "light-blue" (REDFEARN and GROUP both RG_BLUE at full opacity, the
    #   monochrome-blue counterpart to "light")
    # - "dark-group-grey" (REDFEARN cream, GROUP RG_ASH, dark bg)
    # "dark-group-blue" was never built at all: GROUP in RG_BLUE on the
    # dark scheme's RG_BLUE background would be the exact same color as
    # the background and render invisible, so that one was rejected before
    # a single file was ever generated.
}

TITLES = {
    "lockup": "Redfearn Group: Badge and Stacked Wordmark Lockup",
    "wide": "Redfearn Group: Wide Single-Row Lockup",
    "stacked": "Redfearn Group: Stacked Vertical Lockup",
    "wordmark-only": "Redfearn Group: Wordmark Only",
    "icon-only": "Redfearn Group: Icon Only",
    "icon-avatar-safe": "Redfearn Group: Icon Only, Avatar-Safe Padding",
}

SCHEME_TITLE_SUFFIX = {
    "light": ", for light backgrounds",
    "dark": ", for dark backgrounds",
    "reverse": ", reverse single-color",
    "bw": ", opaque black and white",
    "red": ", solid single-ink Redfearn Group red, transparent elsewhere",
    "light-group-blue": ", for light backgrounds, GROUP in blue (comparison candidate)",
    "red-group-blue": ", solid single-ink Redfearn Group red with GROUP in blue, transparent elsewhere (comparison candidate)",
    "watermark": ", low-opacity watermark for slide and report backgrounds (comparison candidate)",
}


def load_glyph_data():
    with open(GLYPH_DATA_PATH) as f:
        return json.load(f)


def layout_word(glyphs, tighten=1.0, extra_tracking=0.0):
    x = 0.0
    placed = []
    for g in glyphs:
        placed.append((g, x))
        x += g["advance"] * tighten + extra_tracking
    min_x = min(g["bounds"][0] + off for g, off in placed)
    max_x = max(g["bounds"][2] + off for g, off in placed)
    min_y = min(g["bounds"][1] for g, _ in placed)
    max_y = max(g["bounds"][3] for g, _ in placed)
    return placed, (min_x, min_y, max_x, max_y)


def emit_glyphs(placed, bounds, scale, origin_x, baseline_y):
    lines = []
    for g, x_off in placed:
        tx = origin_x + (x_off - bounds[0]) * scale
        lines.append(
            f'    <g transform="translate({tx:.4f},{baseline_y:.4f}) '
            f'scale({scale:.6f},-{scale:.6f})"><path d="{g["path"]}"/></g>'
        )
    return "\n".join(lines)


def compute_words(glyph_data):
    redfearn = glyph_data["wordmark"]["REDFEARN"]["letters"]
    group = glyph_data["wordmark"]["GROUP"]["letters"]
    rf_placed, rf_bounds = layout_word(redfearn, tighten=RF_TIGHTEN)
    gr_placed, gr_bounds = layout_word(
        group, tighten=1.0, extra_tracking=600 * GR_EXTRA_TRACKING_EM
    )
    return rf_placed, rf_bounds, gr_placed, gr_bounds


def badge_paths(glyph_data):
    r = glyph_data["badge_monogram"]["R"]["path"]
    g = glyph_data["badge_monogram"]["G"]["path"]
    return r, g


def knockout_opacity_attr(scheme_cfg):
    """Optional fill-opacity for knockout schemes that also carry a low
    opacity value (currently just "watermark"). Normal knockout schemes
    (reverse/bw/red) have no "opacity" key and render at full strength."""
    opacity = scheme_cfg.get("opacity")
    return f' fill-opacity="{opacity}"' if opacity is not None else ""


def knockout_defs(mask_id, r_path, g_path):
    return (
        f'  <defs>\n'
        f'    <mask id="{mask_id}" maskUnits="userSpaceOnUse" x="0" y="0" width="100" height="100">\n'
        f'      <rect x="0" y="0" width="100" height="100" fill="#ffffff"/>\n'
        f'      <g fill="#000000">\n'
        f'        <g transform="{BADGE_R_TRANSFORM}"><path d="{r_path}"/></g>\n'
        f'        <g transform="{BADGE_G_TRANSFORM}"><path d="{g_path}"/></g>\n'
        f'      </g>\n'
        f'    </mask>\n'
        f'  </defs>'
    )


def two_tone_badge_markup(r_path, g_path, badge_fill=RG_RED, letter_fill=RG_CREAM):
    return (
        f'<rect x="0" y="0" width="100" height="100" rx="8" fill="{badge_fill}"/>\n'
        f'    <g fill="{letter_fill}">\n'
        f'      <g transform="{BADGE_R_TRANSFORM}"><path d="{r_path}"/></g>\n'
        f'      <g transform="{BADGE_G_TRANSFORM}"><path d="{g_path}"/></g>\n'
        f'    </g>'
    )


def build_title_desc(layout, scheme):
    title = TITLES[layout] + SCHEME_TITLE_SUFFIX[scheme]
    mode = SCHEMES[scheme]["mode"]
    if mode == "knockout":
        opacity = SCHEMES[scheme].get("opacity")
        if opacity is not None:
            desc = (
                f"Low-opacity ({opacity * 100:.0f}%) single-color watermark version, for "
                f"large decorative background use behind text on slide backgrounds and "
                f"report covers, not a primary logo placement. Reuses the knockout "
                f"composition (badge letters as a transparent cutout) so the RG shape "
                f"stays visible as a faint impression instead of collapsing into a flat "
                f"blob at low opacity. Real Space Grotesk Bold and JetBrains Mono Medium "
                f"vector outlines, no font dependency."
            )
        elif scheme == "red-group-blue":
            desc = (
                "Transparent knockout badge and REDFEARN in Redfearn Group red, GROUP "
                "overridden to blue. The badge is knocked out as transparent negative "
                "space exactly like the all-red 'red' scheme (the cutout never carries "
                "GROUP's color), only the GROUP wordmark's own fill differs. Real Space "
                "Grotesk Bold and JetBrains Mono Medium vector outlines, no font "
                "dependency."
            )
        else:
            color_names = {"reverse": "cream", "red": "Redfearn Group red"}
            color_name = color_names[scheme]
            desc = (
                f"Single-color {color_name} knockout version. The RG mark is knocked out "
                f"as transparent negative space rather than a separate fill color, so it "
                f"reproduces correctly in single-ink printing, embroidery, or on colored "
                f"and photo backgrounds. Real Space Grotesk Bold and JetBrains Mono Medium "
                f"vector outlines, no font dependency."
            )
    elif scheme == "bw":
        desc = (
            "Opaque black-and-white two-tone version: a solid black badge with genuine "
            "white (not cream) letterforms, and a solid black wordmark. Both colors are "
            "baked in as real fills, not a knockout cutout, so it reproduces correctly "
            "on any backdrop rather than only reading as black-and-white over a literal "
            "white surface. Real Space Grotesk Bold and JetBrains Mono Medium vector "
            "outlines, no font dependency."
        )
    else:
        desc = (
            "Real Space Grotesk Bold and JetBrains Mono Medium vector outlines, "
            "no font dependency."
        )
    return title, desc


def generate_lockup(glyph_data, scheme):
    cfg = LAYOUTS["lockup"]
    rf_placed, rf_bounds, gr_placed, gr_bounds = compute_words(glyph_data)
    r_path, g_path = badge_paths(glyph_data)

    badge_size, pad, gap, line_gap = cfg["badge_size"], cfg["pad"], cfg["gap"], cfg["line_gap"]
    rf_cap_px, gr_cap_px = cfg["rf_cap_px"], cfg["gr_cap_px"]

    rf_scale = rf_cap_px / RF_CAP_FONT_UNITS
    gr_scale = gr_cap_px / GR_CAP_FONT_UNITS
    rf_width_px = (rf_bounds[2] - rf_bounds[0]) * rf_scale
    gr_width_px = (gr_bounds[2] - gr_bounds[0]) * gr_scale
    wordmark_block_width = max(rf_width_px, gr_width_px)

    total_width = pad + badge_size + gap + wordmark_block_width + pad
    total_height = pad + badge_size + pad

    text_block_height = rf_cap_px + line_gap + gr_cap_px
    text_block_top = pad + (badge_size - text_block_height) / 2
    rf_baseline_y = text_block_top + rf_cap_px
    gr_baseline_y = rf_baseline_y + line_gap + gr_cap_px
    wordmark_x = pad + badge_size + gap

    rf_svg = emit_glyphs(rf_placed, rf_bounds, rf_scale, wordmark_x, rf_baseline_y)
    gr_svg = emit_glyphs(gr_placed, gr_bounds, gr_scale, wordmark_x, gr_baseline_y)

    scheme_cfg = SCHEMES[scheme]
    badge_transform = f"translate({pad},{pad}) scale({badge_size / 100:.6f})"

    if scheme_cfg["mode"] == "two-tone":
        badge_markup = two_tone_badge_markup(
            r_path, g_path,
            badge_fill=scheme_cfg.get("badge_fill", RG_RED),
            letter_fill=scheme_cfg.get("letter_fill", RG_CREAM),
        )
        defs = ""
        rf_color, gr_color, gr_opacity = scheme_cfg["redfearn"], scheme_cfg["group"], scheme_cfg["group_opacity"]
        body = (
            f'  <g transform="{badge_transform}">\n    {badge_markup}\n  </g>\n'
            f'  <g fill="{rf_color}">\n{rf_svg}\n  </g>\n'
            f'  <g fill="{gr_color}" fill-opacity="{gr_opacity}">\n{gr_svg}\n  </g>'
        )
    else:  # knockout
        ink = scheme_cfg["ink"]
        opacity_attr = knockout_opacity_attr(scheme_cfg)
        mask_id = "rgKnockoutLockup"
        defs = knockout_defs(mask_id, r_path, g_path)
        group_ink = scheme_cfg.get("group_ink", ink)
        body = (
            f'  <g transform="{badge_transform}">\n'
            f'    <rect x="0" y="0" width="100" height="100" rx="8" fill="{ink}"{opacity_attr} mask="url(#{mask_id})"/>\n'
            f'  </g>\n'
            f'  <g fill="{ink}"{opacity_attr}>\n{rf_svg}\n  </g>\n'
            f'  <g fill="{group_ink}"{opacity_attr}>\n{gr_svg}\n  </g>'
        )

    title, desc = build_title_desc("lockup", scheme)
    return assemble_svg(total_width, total_height, title, desc, defs, body)


def generate_wide(glyph_data, scheme):
    cfg = LAYOUTS["wide"]
    rf_placed, rf_bounds, gr_placed, gr_bounds = compute_words(glyph_data)
    r_path, g_path = badge_paths(glyph_data)

    badge_size, pad, gap, word_gap = cfg["badge_size"], cfg["pad"], cfg["gap"], cfg["word_gap"]
    rf_cap_px, gr_cap_px = cfg["rf_cap_px"], cfg["gr_cap_px"]

    rf_scale = rf_cap_px / RF_CAP_FONT_UNITS
    gr_scale = gr_cap_px / GR_CAP_FONT_UNITS
    rf_width_px = (rf_bounds[2] - rf_bounds[0]) * rf_scale
    gr_width_px = (gr_bounds[2] - gr_bounds[0]) * gr_scale

    total_width = pad + badge_size + gap + rf_width_px + word_gap + gr_width_px + pad
    total_height = pad + badge_size + pad

    # Single row: REDFEARN and GROUP share one baseline, vertically centered
    # against the badge, rather than REDFEARN stacked over a smaller GROUP line.
    text_top = pad + (badge_size - rf_cap_px) / 2
    baseline_y = text_top + rf_cap_px

    rf_origin_x = pad + badge_size + gap
    gr_origin_x = rf_origin_x + rf_width_px + word_gap

    rf_svg = emit_glyphs(rf_placed, rf_bounds, rf_scale, rf_origin_x, baseline_y)
    gr_svg = emit_glyphs(gr_placed, gr_bounds, gr_scale, gr_origin_x, baseline_y)

    scheme_cfg = SCHEMES[scheme]
    badge_transform = f"translate({pad},{pad}) scale({badge_size / 100:.6f})"

    if scheme_cfg["mode"] == "two-tone":
        badge_markup = two_tone_badge_markup(
            r_path, g_path,
            badge_fill=scheme_cfg.get("badge_fill", RG_RED),
            letter_fill=scheme_cfg.get("letter_fill", RG_CREAM),
        )
        defs = ""
        rf_color, gr_color, gr_opacity = scheme_cfg["redfearn"], scheme_cfg["group"], scheme_cfg["group_opacity"]
        body = (
            f'  <g transform="{badge_transform}">\n    {badge_markup}\n  </g>\n'
            f'  <g fill="{rf_color}">\n{rf_svg}\n  </g>\n'
            f'  <g fill="{gr_color}" fill-opacity="{gr_opacity}">\n{gr_svg}\n  </g>'
        )
    else:  # knockout
        ink = scheme_cfg["ink"]
        opacity_attr = knockout_opacity_attr(scheme_cfg)
        mask_id = "rgKnockoutWide"
        defs = knockout_defs(mask_id, r_path, g_path)
        group_ink = scheme_cfg.get("group_ink", ink)
        body = (
            f'  <g transform="{badge_transform}">\n'
            f'    <rect x="0" y="0" width="100" height="100" rx="8" fill="{ink}"{opacity_attr} mask="url(#{mask_id})"/>\n'
            f'  </g>\n'
            f'  <g fill="{ink}"{opacity_attr}>\n{rf_svg}\n  </g>\n'
            f'  <g fill="{group_ink}"{opacity_attr}>\n{gr_svg}\n  </g>'
        )

    title, desc = build_title_desc("wide", scheme)
    return assemble_svg(total_width, total_height, title, desc, defs, body)


def generate_stacked(glyph_data, scheme):
    cfg = LAYOUTS["stacked"]
    rf_placed, rf_bounds, gr_placed, gr_bounds = compute_words(glyph_data)
    r_path, g_path = badge_paths(glyph_data)

    badge_size, pad, gap, line_gap = cfg["badge_size"], cfg["pad"], cfg["gap"], cfg["line_gap"]
    rf_cap_px, gr_cap_px = cfg["rf_cap_px"], cfg["gr_cap_px"]

    rf_scale = rf_cap_px / RF_CAP_FONT_UNITS
    gr_scale = gr_cap_px / GR_CAP_FONT_UNITS
    rf_width_px = (rf_bounds[2] - rf_bounds[0]) * rf_scale
    gr_width_px = (gr_bounds[2] - gr_bounds[0]) * gr_scale

    content_width = max(badge_size, rf_width_px, gr_width_px)
    total_width = content_width + 2 * pad
    center_x = total_width / 2

    text_block_height = rf_cap_px + line_gap + gr_cap_px
    total_height = pad + badge_size + gap + text_block_height + pad

    badge_x = center_x - badge_size / 2
    badge_y = pad

    rf_top = pad + badge_size + gap
    rf_baseline_y = rf_top + rf_cap_px
    gr_baseline_y = rf_baseline_y + line_gap + gr_cap_px

    rf_origin_x = center_x - rf_width_px / 2
    gr_origin_x = center_x - gr_width_px / 2

    rf_svg = emit_glyphs(rf_placed, rf_bounds, rf_scale, rf_origin_x, rf_baseline_y)
    gr_svg = emit_glyphs(gr_placed, gr_bounds, gr_scale, gr_origin_x, gr_baseline_y)

    scheme_cfg = SCHEMES[scheme]
    badge_transform = f"translate({badge_x:.4f},{badge_y:.4f}) scale({badge_size / 100:.6f})"

    if scheme_cfg["mode"] == "two-tone":
        badge_markup = two_tone_badge_markup(
            r_path, g_path,
            badge_fill=scheme_cfg.get("badge_fill", RG_RED),
            letter_fill=scheme_cfg.get("letter_fill", RG_CREAM),
        )
        defs = ""
        rf_color, gr_color, gr_opacity = scheme_cfg["redfearn"], scheme_cfg["group"], scheme_cfg["group_opacity"]
        body = (
            f'  <g transform="{badge_transform}">\n    {badge_markup}\n  </g>\n\n'
            f'  <g fill="{rf_color}">\n{rf_svg}\n  </g>\n\n'
            f'  <g fill="{gr_color}" fill-opacity="{gr_opacity}">\n{gr_svg}\n  </g>'
        )
    else:  # knockout
        ink = scheme_cfg["ink"]
        opacity_attr = knockout_opacity_attr(scheme_cfg)
        mask_id = "rgKnockoutStacked"
        defs = knockout_defs(mask_id, r_path, g_path)
        group_ink = scheme_cfg.get("group_ink", ink)
        body = (
            f'  <g transform="{badge_transform}">\n'
            f'    <rect x="0" y="0" width="100" height="100" rx="8" fill="{ink}"{opacity_attr} mask="url(#{mask_id})"/>\n'
            f'  </g>\n\n'
            f'  <g fill="{ink}"{opacity_attr}>\n{rf_svg}\n  </g>\n\n'
            f'  <g fill="{group_ink}"{opacity_attr}>\n{gr_svg}\n  </g>'
        )

    title, desc = build_title_desc("stacked", scheme)
    return assemble_svg(total_width, total_height, title, desc, defs, body)


def generate_wordmark_only(glyph_data, scheme):
    cfg = LAYOUTS["wordmark-only"]
    rf_placed, rf_bounds, gr_placed, gr_bounds = compute_words(glyph_data)

    pad, line_gap = cfg["pad"], cfg["line_gap"]
    rf_cap_px, gr_cap_px = cfg["rf_cap_px"], cfg["gr_cap_px"]

    rf_scale = rf_cap_px / RF_CAP_FONT_UNITS
    gr_scale = gr_cap_px / GR_CAP_FONT_UNITS
    rf_width_px = (rf_bounds[2] - rf_bounds[0]) * rf_scale
    gr_width_px = (gr_bounds[2] - gr_bounds[0]) * gr_scale
    content_width = max(rf_width_px, gr_width_px)

    total_width = content_width + 2 * pad
    center_x = total_width / 2
    text_block_height = rf_cap_px + line_gap + gr_cap_px
    total_height = text_block_height + 2 * pad

    rf_baseline_y = pad + rf_cap_px
    gr_baseline_y = rf_baseline_y + line_gap + gr_cap_px
    rf_origin_x = center_x - rf_width_px / 2
    gr_origin_x = center_x - gr_width_px / 2

    rf_svg = emit_glyphs(rf_placed, rf_bounds, rf_scale, rf_origin_x, rf_baseline_y)
    gr_svg = emit_glyphs(gr_placed, gr_bounds, gr_scale, gr_origin_x, gr_baseline_y)

    scheme_cfg = SCHEMES[scheme]
    defs = ""
    if scheme_cfg["mode"] == "two-tone":
        rf_color, gr_color, gr_opacity = scheme_cfg["redfearn"], scheme_cfg["group"], scheme_cfg["group_opacity"]
        body = (
            f'  <g fill="{rf_color}">\n{rf_svg}\n  </g>\n\n'
            f'  <g fill="{gr_color}" fill-opacity="{gr_opacity}">\n{gr_svg}\n  </g>'
        )
    else:  # knockout
        ink = scheme_cfg["ink"]
        opacity_attr = knockout_opacity_attr(scheme_cfg)
        group_ink = scheme_cfg.get("group_ink", ink)
        body = (
            f'  <g fill="{ink}"{opacity_attr}>\n{rf_svg}\n  </g>\n\n'
            f'  <g fill="{group_ink}"{opacity_attr}>\n{gr_svg}\n  </g>'
        )

    title, desc = build_title_desc("wordmark-only", scheme)
    return assemble_svg(total_width, total_height, title, desc, defs, body)


def generate_icon_only(glyph_data, scheme):
    r_path, g_path = badge_paths(glyph_data)
    scheme_cfg = SCHEMES[scheme]

    if scheme_cfg["mode"] == "two-tone":
        badge_markup = two_tone_badge_markup(
            r_path, g_path,
            badge_fill=scheme_cfg.get("badge_fill", RG_RED),
            letter_fill=scheme_cfg.get("letter_fill", RG_CREAM),
        )
        defs = ""
        body = f'  {badge_markup}'
    else:  # knockout
        ink = scheme_cfg["ink"]
        opacity_attr = knockout_opacity_attr(scheme_cfg)
        mask_id = "rgKnockoutIcon"
        defs = knockout_defs(mask_id, r_path, g_path)
        body = f'  <rect x="0" y="0" width="100" height="100" rx="8" fill="{ink}"{opacity_attr} mask="url(#{mask_id})"/>'

    title, desc = build_title_desc("icon-only", scheme)
    return assemble_svg(100, 100, title, desc, defs, body)


def generate_icon_avatar_safe(glyph_data, scheme):
    """Same canonical 100x100 badge as icon-only, unmodified, inset inside
    a larger canvas so the badge sits entirely within the largest circle a
    square-to-circle avatar crop would keep. See the LAYOUTS comment for
    the geometry reasoning."""
    cfg = LAYOUTS["icon-avatar-safe"]
    pad = cfg["pad"]
    size = 100 + 2 * pad
    r_path, g_path = badge_paths(glyph_data)
    scheme_cfg = SCHEMES[scheme]
    badge_transform = f"translate({pad},{pad})"

    if scheme_cfg["mode"] == "two-tone":
        badge_markup = two_tone_badge_markup(
            r_path, g_path,
            badge_fill=scheme_cfg.get("badge_fill", RG_RED),
            letter_fill=scheme_cfg.get("letter_fill", RG_CREAM),
        )
        defs = ""
        body = f'  <g transform="{badge_transform}">\n    {badge_markup}\n  </g>'
    else:  # knockout
        ink = scheme_cfg["ink"]
        opacity_attr = knockout_opacity_attr(scheme_cfg)
        mask_id = "rgKnockoutAvatarSafe"
        defs = knockout_defs(mask_id, r_path, g_path)
        body = (
            f'  <g transform="{badge_transform}">\n'
            f'    <rect x="0" y="0" width="100" height="100" rx="8" fill="{ink}"{opacity_attr} mask="url(#{mask_id})"/>\n'
            f'  </g>'
        )

    title, desc = build_title_desc("icon-avatar-safe", scheme)
    return assemble_svg(size, size, title, desc, defs, body)


def assemble_svg(width, height, title, desc, defs, body):
    parts = [
        f'<svg viewBox="0 0 {width:.0f} {height:.0f}" xmlns="http://www.w3.org/2000/svg" role="img">',
        f'  <title>{title}</title>',
        f'  <desc>{desc}</desc>',
    ]
    if defs:
        parts.append(defs)
    parts.append(body)
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


GENERATORS = {
    "lockup": generate_lockup,
    "wide": generate_wide,
    "stacked": generate_stacked,
    "wordmark-only": generate_wordmark_only,
    "icon-only": generate_icon_only,
    "icon-avatar-safe": generate_icon_avatar_safe,
}


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    layout, scheme, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    if layout not in GENERATORS:
        print(f"Unknown layout '{layout}'. Choose from: {', '.join(GENERATORS)}")
        sys.exit(1)
    if scheme not in SCHEMES:
        print(f"Unknown scheme '{scheme}'. Choose from: {', '.join(SCHEMES)}")
        sys.exit(1)
    glyph_data = load_glyph_data()
    svg = GENERATORS[layout](glyph_data, scheme)
    Path(out_path).write_text(svg, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
