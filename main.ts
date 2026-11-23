// Sum up 22 November's world news in one image — entry program.
//
// The entry is entry.png: a newspaper front page that sums up
// Saturday 22 November 2026 in one picture (60 stories: a lead,
// two secondary stories, thirteen illustrated cards, a map and
// a 44-line index). build_page.py in this repository draws it;
// this program does the hand-in the bounty asks for: it copies
// entry.png, byte for byte, into the output directory —
// /output/entry.png by default, or $MAKEFUN_OUTPUT_DIR/entry.png
// when the grader points it somewhere else.
//
//   MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only, no network.

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

const size = statSync(source).size;
if (size === 0) {
  throw new Error('entry.png is empty — run build_page.py first');
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
console.log(`entry.png (${size} bytes) -> ${target}`);
