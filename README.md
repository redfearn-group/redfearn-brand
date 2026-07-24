# Redfearn Group Brand

Canonical design tokens and shared CSS primitives for every Redfearn Group property.

`brand.css` is the single source of truth. It is vendored into each consuming repo, and each repo's CI fails the build if its copy has drifted from this one.

## Why vendored instead of a package

Builds stay hermetic with no network dependency and no registry, which keeps every property free to build and deploy. The tradeoff is that copies could silently diverge, so the drift check exists specifically to make that loud. That failure mode is not hypothetical: garage-log and home-log had already diverged from the site and from each other before this file existed.

## Consumers

| Property | Vendored path | Layer |
| :--- | :--- | :--- |
| [redfearn-group.github.io](https://github.com/redfearn-group/redfearn-group.github.io) | `src/css/brand.css` | Identity, plus Content on case studies |
| [garage-log](https://github.com/redfearn-group/garage-log) | `src/styles/brand.css` | Product |
| [home-log](https://github.com/redfearn-group/home-log) | `src/styles/brand.css` | Product |

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
| cream body text | 16.04:1 | AAA |
| muted text | 6.77:1 | AA |
| accent link (`--rg-red-light`) | 6.40:1 | AA |
| status overdue | 6.40:1 | AA |
| status due-soon | 8.69:1 | AAA |
| status ok | 6.42:1 | AA |
| gape yellow (ambient log only) | 11.64:1 | AAA |

Raw `--rg-red` is 2.88:1 on that surface and raw `--rg-ember` is 3.98:1. Both fail body text on dark, which is why `--rg-red-light` exists. It also sits dE 13.8 from `--status-overdue-fg`, far enough that an accent link never reads as an overdue badge.

## Changing a value

1. Edit `brand.css` here.
2. Run `node sync.mjs` to push it into the sibling repos on disk.
3. Commit and push this repo **first**, then each consumer. The drift check pulls from `main` here, so consumers will fail until this repo is updated.

## Related

Application rules, voice, logo system, and implementation pitfalls live in the `redfearn-group-style` skill, which points at this file rather than restating values.
