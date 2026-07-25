/* Package skill/ into a dated ZIP for backup and re-import.
   Run from this repo: `node package-skill.mjs`

   The archive nests everything under a `redfearn-group-style/` folder so
   unzipping produces a directory ready to drop into a skills location.

   skill/ in this repo stays the source of truth. The ZIP is a snapshot.
   Attach it to a GitHub release rather than committing it, so the repo
   does not accumulate binaries that duplicate what is already tracked. */

import { execFileSync } from "node:child_process";
import { existsSync, rmSync, mkdirSync, cpSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(ROOT, "skill");
const NAME = "redfearn-group-style";

if (!existsSync(SRC)) {
  console.error(`No skill/ directory at ${SRC}`);
  process.exit(1);
}

// Date is passed in rather than read from the clock so a rebuild of an
// older release reproduces its filename exactly.
const stamp = process.argv[2] ?? new Date().toISOString().slice(0, 10);
if (!/^\d{4}-\d{2}-\d{2}$/.test(stamp)) {
  console.error(`Expected a YYYY-MM-DD date, got "${stamp}"`);
  process.exit(1);
}

const stage = path.join(ROOT, ".package-tmp");
const out = path.join(ROOT, "..", `${NAME}-${stamp}.zip`);

rmSync(stage, { recursive: true, force: true });
mkdirSync(path.join(stage, NAME), { recursive: true });
cpSync(SRC, path.join(stage, NAME), { recursive: true });
rmSync(out, { force: true });

// Compress-Archive is built into Windows PowerShell, so this needs no
// dependency and no zip binary on PATH.
execFileSync("powershell", [
  "-NoProfile",
  "-Command",
  `Compress-Archive -Path '${path.join(stage, NAME)}' -DestinationPath '${out}' -CompressionLevel Optimal`,
]);

rmSync(stage, { recursive: true, force: true });
console.log(`Wrote ${out}`);
console.log(`Publish it with:\n  gh release create skill-${stamp} "${out}" --title "..." --notes "..."`);
