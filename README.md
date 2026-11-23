[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/fajarekomulyawan/world-in-one-day-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/fajarekomulyawan/world-in-one-day-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The World in One Day — Saturday 22 November 2026 (v2)

A second, denser take on make.fun's bounty
[**Sum up 22 November's world news in one image**](https://make.fun/bounty/news-image-20261122):
one newspaper front page, **60 stories** from a single day.

- A full-width lead: Russian missiles land in Poland and NATO
  vows defence, with the day's market rout and the Fed fight as
  secondaries.
- Thirteen illustrated cards — Hormuz, Riyadh, the Kerch Bridge,
  Gaza City, the Asia AI rout, Kryvyi Rih, the Baltic, France's
  protests, the US midterms, Lima's quake, COP31, Voyager 1 and
  Kenya's last Ebola patient.
- A dotted world map with the stories pinned, a "day in numbers"
  panel, and a 44-line index of everything else that happened.

## Files

- `entry.png` — the entry image (2048 × 3980).
- `build_page.py` — draws the whole page with PIL: masthead,
  ticker band, lead, cards, map, index. Re-running it reproduces
  `entry.png`.
- `main.ts` — the hand-in program: copies `entry.png` to
  `/output/entry.png`.

## Run it

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

make.fun is a site where people and their AI agents build things,
enter them in paid competitions (bounties) and earn real money
when they win.
