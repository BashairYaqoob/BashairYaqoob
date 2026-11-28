# Profile card generator

The SVGs in `assets/` are generated. Change the words in `karachi/content.py` and the look in `karachi/cards/`, then render:

```bash
pip install -r scripts/requirements.txt
python scripts/fetch_contributions.py   # needs GITHUB_TOKEN; skips quietly without one
python scripts/render.py
```

| Path | What it is |
|---|---|
| `karachi/content.py` | All copy: details, arsenal, projects, links, section titles |
| `karachi/svg.py` | Palette, font subsetting (fonts are embedded as woff2 subsets), SVG wrapper |
| `karachi/iso.py` | The isometric projection shared by the city and its landmarks |
| `karachi/data.py` | Folds `data/contributions.json` into GitHub-style weeks |
| `karachi/cards/*.py` | One module per card: hero, city (isometric), arsenal, project, section, links, footer |
| `karachi/art_*.txt` | The ASCII name, pre-rendered with figlet's `georgia11` font |
| `fetch_contributions.py` | GraphQL fetch of the last 365 days into `data/contributions.json` |

**Motion.** Animated cards are written twice: `assets/<card>.svg` and a final-frame twin in `assets/static/`. The README serves the twin through `<picture><source media="(prefers-reduced-motion: reduce)">`. Browsers don't pass the reduced-motion preference into SVGs loaded via `<img>`, so the SVG's own media query isn't enough on its own. `STATIC=1 python scripts/render.py` renders everything still, which helps for screenshots.

**Refresh.** `.github/workflows/render-profile.yml` runs daily, on manual dispatch, and when the generator changes. It fetches contributions, re-renders, and commits only when something changed. It uses the built-in token with `contents: write` and nothing else. To include private contributions, add a fine-grained personal access token with no repository permissions as the `CONTRIBUTIONS_TOKEN` secret.

**City mapping.** An isometric 53 × 7 grid laid out like the contribution graph: weeks run left to right, with Sunday at the back and Saturday on the seafront. Each building is one day. Its height follows that day's count on a square-root scale, and its windows glow by GitHub's 1–4 level. Quiet days are low, dark houses. The landmarks, drawn in the same projection in `karachi/cards/landmarks.py` (Mazar-e-Quaid, Frere Hall, Empress Market, Bahria Icon Tower, Teen Talwar, a Sea View camel), are scenery, not data.

Fonts: JetBrains Mono and Instrument Serif, both under the SIL Open Font License (see `assets/fonts/`).
