/* Copy the canonical brand.css into each sibling property on disk.
   Run from this repo: `node sync.mjs`
   Pass --check to report drift without writing anything. */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const CANONICAL = path.join(ROOT, "brand.css");

const CONSUMERS = [
  ["redfearn-group.github.io", "src/css/brand.css"],
  ["garage-log", "src/styles/brand.css"],
  ["home-log", "src/styles/brand.css"],
];

const checkOnly = process.argv.includes("--check");
const source = readFileSync(CANONICAL, "utf-8");
let drifted = 0;
let missing = 0;

for (const [repo, rel] of CONSUMERS) {
  const dir = path.resolve(ROOT, "..", repo);
  if (!existsSync(dir)) {
    console.log(`SKIP   ${repo} not found as a sibling folder`);
    missing++;
    continue;
  }
  const dest = path.join(dir, rel);
  const current = existsSync(dest) ? readFileSync(dest, "utf-8") : null;

  if (current === source) {
    console.log(`OK     ${repo}/${rel}`);
    continue;
  }

  drifted++;
  if (checkOnly) {
    console.log(`DRIFT  ${repo}/${rel} ${current === null ? "(missing)" : "(differs)"}`);
  } else {
    writeFileSync(dest, source);
    console.log(`WROTE  ${repo}/${rel} ${current === null ? "(created)" : "(updated)"}`);
  }
}

if (missing) console.log(`\n${missing} consumer(s) not on disk.`);
if (checkOnly && drifted) {
  console.error(`\n${drifted} copy/copies differ from canonical.`);
  process.exit(1);
}
if (!checkOnly && drifted) {
  console.log(`\n${drifted} copy/copies updated. Push this repo before pushing consumers.`);
}
