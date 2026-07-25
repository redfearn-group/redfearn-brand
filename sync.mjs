/* Copy the canonical shared files out to where they are consumed.
   Run from this repo: `node sync.mjs`
   Pass --check to report drift without writing anything, exit 1 if any.

   Everything below is authored HERE and copied outward. Never edit a
   destination copy: the next sync silently overwrites it, and for
   brand.css a CI job in each consumer fails the build first. */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.resolve(ROOT, "..");

/* source, relative to this repo → destination, relative to the workspace
   folder that holds all the sibling repos. */
const FILES = [
  ["brand.css", "redfearn-group.github.io/src/css/brand.css"],
  ["brand.css", "garage-log/src/styles/brand.css"],
  ["brand.css", "home-log/src/styles/brand.css"],
  // Auto-loaded by Claude Code from the workspace root, which is not a git
  // repo, so this repo is where it actually survives.
  ["workspace/CLAUDE.md", "CLAUDE.md"],
];

const checkOnly = process.argv.includes("--check");
let drifted = 0;
let missing = 0;

/* Compare on content, not bytes. A Windows checkout rewrites these files
   with CRLF, which would otherwise report as drift on every line even
   though nothing changed. .gitattributes pins them to LF, and this is the
   backstop for a copy that predates that or was written by hand. */
const normalize = (s) => s.replace(/\r\n/g, "\n");

for (const [srcRel, destRel] of FILES) {
  const source = readFileSync(path.join(ROOT, srcRel), "utf-8");
  const dest = path.join(WORKSPACE, destRel);

  // A destination inside a repo that is not cloned here is skipped rather
  // than created, so syncing never scatters files into empty folders.
  const destDir = path.dirname(dest);
  if (!existsSync(destDir)) {
    console.log(`SKIP   ${destRel} (${path.relative(WORKSPACE, destDir)} not on disk)`);
    missing++;
    continue;
  }

  const current = existsSync(dest) ? readFileSync(dest, "utf-8") : null;
  if (current !== null && normalize(current) === normalize(source)) {
    console.log(`OK     ${destRel}`);
    continue;
  }

  drifted++;
  const why = current === null ? "(missing)" : "(differs)";
  if (checkOnly) {
    console.log(`DRIFT  ${destRel} ${why}`);
  } else {
    writeFileSync(dest, source);
    console.log(`WROTE  ${destRel} ${current === null ? "(created)" : "(updated)"}`);
  }
}

if (missing) console.log(`\n${missing} destination(s) not on disk.`);
if (checkOnly && drifted) {
  console.error(`\n${drifted} copy/copies differ from canonical.`);
  process.exit(1);
}
if (!checkOnly && drifted) {
  console.log(`\n${drifted} copy/copies updated. Push this repo before pushing consumers.`);
}
