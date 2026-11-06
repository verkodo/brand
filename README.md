# verkodo – brand kit

The mark is **⊨ ∎**: the double turnstile of logic – *is true*, the *vero* in verkodo – and the tombstone that ends a
proof. The two bars of ⊨ cut into ∎ as notches: the truth is carried into the proof. Every falkOSS project has its own
name, logo, colours and look; falkOSS appears only as publisher.

| | |
|---|---|
| Grid | stem, bars and the gap between them one unit each; bars two units up to ∎; ∎ five units, cut one unit deep (16–48 px: ∎ four units on a coarser unit, so the notches stay open) |
| Colours | ground `#0D1117` (dark) or `#F7F4EC` (warm paper); face `#E6EDF3` on dark, `#14202B` on light; titanium `#8F959B` on dark, `#646A70` on light – the one colour beside the face |
| Type | [Crimson Pro](https://github.com/Fonthausen/CrimsonPro) (SIL OFL 1.1, `fonts/`): SemiBold for the name, Regular for text; all text in the artwork is converted to outlines |
| One colour | the notches are cut out, not painted, so the mark works in black or white alone (`mark-black`, `mark-white`) |

Everything here is generated: edit `generate.py` (the drawing) – `brandkit.py` (the export) stays as it is – then run
`python3 generate.py` (needs `rsvg-convert` from Homebrew `librsvg` and fontTools: `pip install fonttools`). It writes `svg/`, `png/` and `web/`.

| Use | File |
|---|---|
| GitHub organisation avatar | `png/social/github-avatar-500.png` |
| GitHub social preview, link previews | `png/social/verkodo-social-1280x640.png` |
| Website head (copy to the website) | `web/` – favicon.svg (follows light/dark), favicon.ico, apple-touch-icon.png, icon-192/512.png, social.png, site.webmanifest |
| Headers, documents, profile | `svg/verkodo-lockup-on-dark.svg`, `-on-light.svg` (PNG: `png/lockup/`) |
| Wordmark alone | `svg/verkodo-wordmark-on-dark.svg`, `-on-light.svg` |
| Mark alone (transparent) | `svg/verkodo-mark-on-dark.svg`, `-on-light.svg`; one colour: `-black.svg`, `-white.svg` |
| App-like icon | `png/icon/` (rounded), `png/icon-square/` (edge to edge), `png/icon-small/` (16–48 px) |

## Where it is used

This repository is the brand's one source; the others carry copies of what they show and are updated by copying,
never edited there:

| Repository | Copies |
|---|---|
| `verkodo/website` | `web/`, the lockup and mark on dark and on light (`assets/`) |
| `verkodo/.github` | the lockups in the organisation profile |
| `verkodo/verkodo` | `web/favicon.*` and the lockup on dark in `docs/assets/`; `web/favicon.svg` in the web app's `web/public/` (if there is one) |

## Rules for the design (as for all falkOSS projects)

- One accent colour, near-black or a clear light ground; straight edges where it fits; no glow, neon or gradients
  unless the project's idea needs them.
- A small variant for 16–48 px that still reads.
- A wordmark as outlines (no font needed where it is shown); fonts only under a free licence (e.g. SIL OFL), never
  loaded from a font service – fonts go to `fonts/` with their licence, and into `REUSE.toml`.
- The name is always lowercase.

## Licences and rights

| Files | Licence |
|---|---|
| `generate.py`, `brandkit.py`, this README | [MIT](LICENSES/MIT.txt) |
| the artwork: `svg/`, `png/`, `web/` | [CC BY-ND 4.0](LICENSES/CC-BY-ND-4.0.txt) |
| the fonts: `fonts/` (Crimson Pro, © 2018 The Crimson Pro Project Authors) | [SIL OFL 1.1](fonts/OFL.txt) |

The artwork may be copied and passed on – also in apps distributed through app stores and in other software – as it
is and naming falkOSS; changed versions may not be passed on. The licence covers the artwork's copyright, not the
name: verkodo's name and brand belong to falkOSS – Falcon Lake Open Source Software gUG (haftungsbeschränkt) i. G., the publisher of verkodo. They may be used to refer to verkodo,
not for other products or in a way that suggests endorsement. **OPEN**: trademark search and registration, and a
review of these terms by someone who knows the law.
