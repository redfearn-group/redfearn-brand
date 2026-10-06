/* Copy the canonical shared files out to where they are consumed.
   Run from this repo: `node sync.mjs`
   Pass --check to report drift without writing anything, exit 1 if any.

   Everything below is authored HERE and copied outward. Never edit a
   destination copy: the next sync silently overwrites it, and a CI job in
   each consumer fails the build first. */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = path.resolve(ROOT, "..");

/* Every .ts file in kit/ is shared. Enumerated from disk rather than listed
   by hand so adding a module is one file, not one file plus four edits. */
const KIT_FILES = readdirSync(path.join(ROOT, "kit"))
  .filter((f) => f.endsWith(".ts"))
  .sort();

/* Where each consumer wants the kit. Astro apps only: the modules import
   `import.meta.env` and js-yaml, so they are meaningless to the Eleventy
   site, which is why it appears below with brand.css and nothing else. */
const kitInto = (dir) =>
  KIT_FILES.map((f) => [`kit/${f}`, `${dir}/${f}`]);

/* Per consumer, so it is obvious at a glance what any one repo receives.
   Paths are relative to the workspace folder holding the sibling repos. */
const CONSUMERS = [
  {
    repo: "redfearn-group.github.io",
    note: "Eleventy. Brand tokens only, no kit.",
    files: [["brand.css", "src/css/brand.css"]],
  },
  {
    repo: "garage-log",
    files: [["brand.css", "src/styles/brand.css"], ...kitInto("src/lib/kit")],
  },
  {
    repo: "home-log",
    files: [["brand.css", "src/styles/brand.css"], ...kitInto("src/lib/kit")],
  },
  {
    repo: "canyon-breeze-manor-hoa",
    files: [["brand.css", "src/styles/brand.css"], ...kitInto("src/lib/kit")],
  },
  {
    repo: "civic-log",
    note: "Civic monitor for Spanish Fork and Utah County. Astro, deployed at /civic-log/.",
    files: [["brand.css", "src/styles/brand.css"], ...kitInto("src/lib/kit")],
  },
  {
    repo: "canyon-breeze-manor-hoa-private",
    note: "Private board tracker. Never deployed, but renders locally and runs the same drift check.",
    files: [["brand.css", "src/styles/brand.css"], ...kitInto("src/lib/kit")],
  },
  {
    // The workspace root itself, not a repo. Claude Code auto-loads
    // CLAUDE.md from there, but the root is not version controlled, so this
    // repo holds the copy that actually survives.
    repo: ".",
    files: [["workspace/CLAUDE.md", "CLAUDE.md"]],
  },
];

/* Private consumers live in consumers.local.json, which is gitignored. This
   repo is public, and naming a private repo here would publish that it
   exists. Same shape as above, except "kit" names the folder that receives
   the kit instead of spelling out each file:
   [{ "repo": "name", "note": "...", "css": "src/styles/brand.css", "kit": "src/lib/kit" }] */
const LOCAL = path.join(ROOT, "consumers.local.json");
if (existsSync(LOCAL)) {
  for (const c of JSON.parse(readFileSync(LOCAL, "utf-8"))) {
    CONSUMERS.push({
      repo: c.repo,
      note: c.note,
      files: [
        ...(c.css ? [["brand.css", c.css]] : []),
        ...(c.kit ? kitInto(c.kit) : []),
        ...(c.files || []),
      ],
    });
  }
}

const checkOnly = process.argv.includes("--check");
let drifted = 0;
let missing = 0;

/* Compare on content, not bytes. A Windows checkout rewrites these files
   with CRLF, which would otherwise report as drift on every line even
   though nothing changed. .gitattributes pins them to LF, and this is the
   backstop for a copy that predates that or was written by hand. */
const normalize = (s) => s.replace(/\r\n/g, "\n");

for (const consumer of CONSUMERS) {
  const repoDir = path.join(WORKSPACE, consumer.repo);

  // A repo that is not cloned here is skipped rather than created, so
  // syncing never scatters files into empty folders.
  if (!existsSync(repoDir)) {
    console.log(`SKIP   ${consumer.repo} (not on disk)`);
    missing += consumer.files.length;
    continue;
  }

  for (const [srcRel, destRel] of consumer.files) {
    const source = readFileSync(path.join(ROOT, srcRel), "utf-8");
    const dest = path.join(repoDir, destRel);
    const label = `${consumer.repo}/${destRel}`;

    // Unlike the repo itself, a missing subdirectory IS created: kit/ is a
    // new folder in every consumer and requiring a manual mkdir first would
    // make the first sync fail for no useful reason.
    const destDir = path.dirname(dest);
    if (!existsSync(destDir)) {
      if (checkOnly) {
        console.log(`DRIFT  ${label} (directory missing)`);
        drifted++;
        continue;
      }
      mkdirSync(destDir, { recursive: true });
    }

    const current = existsSync(dest) ? readFileSync(dest, "utf-8") : null;
    if (current !== null && normalize(current) === normalize(source)) {
      console.log(`OK     ${label}`);
      continue;
    }

    drifted++;
    const why = current === null ? "(missing)" : "(differs)";
    if (checkOnly) {
      console.log(`DRIFT  ${label} ${why}`);
    } else {
      writeFileSync(dest, source);
      console.log(`WROTE  ${label} ${current === null ? "(created)" : "(updated)"}`);
    }
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
