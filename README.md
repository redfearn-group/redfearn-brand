# Redfearn Group Brand

Canonical design tokens and shared CSS primitives for every Redfearn Group property.

Two things are canonical here and vendored outward by `sync.mjs`: **`brand.css`**, the design tokens, and **`kit/*.ts`**, a small set of shared TypeScript helpers. Each consuming repo's CI fails the build if its copy has drifted from this one.

## Why vendored instead of a package

Builds stay hermetic with no network dependency and no registry, which keeps every property free to build and deploy. The tradeoff is that copies could silently diverge, so the drift check exists specifically to make that loud. That failure mode is not hypothetical: garage-log and home-log had already diverged from the site and from each other before this file existed.

## Consumers

| Property | Vendored path | Layer |
| :--- | :--- | :--- |
| [redfearn-group.github.io](https://github.com/redfearn-group/redfearn-group.github.io) | `src/css/brand.css` | Identity, plus Content on case studies |
| [garage-log](https://github.com/redfearn-group/garage-log) | `src/styles/brand.css` | Product |
| [home-log](https://github.com/redfearn-group/home-log) | `src/styles/brand.css` | Product |
| [canyon-breeze-manor-hoa](https://github.com/redfearn-group/canyon-breeze-manor-hoa) | `src/styles/brand.css` | Product |
| canyon-breeze-manor-hoa-private | `src/styles/brand.css` | Product |

The four Astro apps also receive `kit/*.ts` at `src/lib/kit/`. The Eleventy site does not: the modules use `import.meta.env` and js-yaml and mean nothing in an Eleventy build.

`workspace/CLAUDE.md` is also synced out, to `C:\Claude Code\CLAUDE.md`. Claude Code loads that path automatically, but the workspace folder is not a git repo, so this is the only place the file survives. Edit it here, not there.

Shared files are pinned to LF via `.gitattributes` in every repo. Without that, a Windows checkout rewrites them with CRLF and the drift check reports every line as changed. `sync.mjs` also compares on normalized content as a backstop.

## The kit

Shared, app-agnostic helpers. Deliberately small, around 230 lines. Anything that needs to know what a vehicle or a meeting is belongs in the app, not here.

| Module | Exports |
| :--- | :--- |
| `kit/base.ts` | `withBase(p)`, prefixing an internal link with the Pages base path |
| `kit/date.ts` | `formatDate`, `formatMonth`, `parseDate`, `addMonths`, `daysBetween`, `today` |
| `kit/yaml.ts` | `DATA_DIR`, `readYaml(path, fallback)`, `readData(relPath, fallback)` |
| `kit/due.ts` | `dateDue({lastDone, intervalMonths, today, dueSoonDays})`, the date half of a due-status calculation |

Two rules the kit exists to enforce:

**Dates never travel through `new Date(isoString)`.** That parses a bare `YYYY-MM-DD` as UTC midnight and renders it in local time, printing the previous day west of Greenwich. Everything here parses by regex.

**Never derive today from `new Date().toISOString().slice(0, 10)`.** That is UTC, so it returns tomorrow after 18:00 Mountain, and these sites build in GitHub Actions on UTC. Use `today()`.

`npm test` runs 25 assertions over the kit. The kit ships bare relative imports because that is what Astro and Vite expect, so the runner copies `kit/` to a temp directory and rewrites the imports rather than changing what ships.

The `.mjs` scripts in the consuming apps are run directly by node, outside the Astro build, so they **cannot** import this TypeScript. Each carries its own small `today()`. That duplication is a known limitation, not an oversight.

## The three layers

Each layer sets the accent role. Never mix two layers in the same accent role on one page.

- **Identity** (`:root`, no class needed). Brand red. Site chrome, nav, marketing surfaces, CTAs.
- **Content** (`.content-layer`). Ember to gape. Case studies and reports, so they carry warmth without competing with the brand red.
- **Product** (`.app-layer`). Dark surfaces, lightened red accent. Real working applications.

The Product layer is dark unconditionally rather than through `prefers-color-scheme`. The dark treatment is the product identity for these tools, not an echo of an OS setting.

## Contrast

Every Product layer value is measured against the card surface `#0F1830`, which is the binding constraint because it is lighter than the page background.

| Token | Ratio on card | Level |
| :--- | ---: | :--- |
| cream body text / links | 16.04:1 | AAA |
| muted text | 6.77:1 | AA |
| status overdue | 6.40:1 | AA |
| status due-soon | 8.69:1 | AAA |
| status ok | 6.42:1 | AA |
| gape yellow (ambient log only) | 11.64:1 | AAA |

Raw `--rg-red` is 2.88:1 on that surface and raw `--rg-ember` is 3.98:1, both failing body text on dark. Rather than invent a lightened red, the Product layer keeps text and links cream and moves red onto decoration instead: link underlines, borders, tints, the gradient bar. Those are not contrast-bound. The palette stays the closed set Brady already reviewed in `logo-variant-review`, no off-system color introduced without his sign-off.

## Changing a value

1. Edit `brand.css` here.
2. Run `node sync.mjs` to push it into the sibling repos on disk.
3. Commit and push this repo **first**, then each consumer. The drift check pulls from `main` here, so consumers will fail until this repo is updated.

## The skill

`skill/` holds the `redfearn-group-style` skill: layer semantics, voice rules, the logo system, WCAG pairings, and implementation pitfalls. It points at `brand.css` rather than restating values, so the rules and the values version together in one repo.

It is kept here because the copy Claude loads at runtime lives in a session-scoped plugin cache that does not survive. This is the durable source. To update the active copy, replace the contents of the plugin's `skills/redfearn-group-style/` directory with `skill/`, or drop it into `~/.claude/skills/`.

### Exporting it

```sh
node package-skill.mjs            # dated ZIP written to the parent folder
node package-skill.mjs 2026-07-24 # rebuild a specific dated release
```

The archive nests everything under `redfearn-group-style/`, so unzipping gives a folder ready to drop into a skills location. Attach it to a [GitHub release](https://github.com/redfearn-group/redfearn-brand/releases) rather than committing it, so the repo does not accumulate binaries duplicating what `skill/` already tracks. ZIPs are gitignored for that reason.

## Adding a new property

1. Vendor `brand.css` into it, and add the path to `CONSUMERS` in `sync.mjs`.
2. Copy `.github/workflows/vendor-drift.yml` from an existing consumer and fix the paths.
3. Load `brand.css` before the property's own stylesheet.
4. Pick a layer. Applications set `class="app-layer"` on `<html>`.
5. Use `rg-mark.svg` as the favicon and in the header. Never a framework default.
