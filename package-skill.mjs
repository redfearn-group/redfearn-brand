/* Package skill/ into a dated ZIP for backup and re-import.
   Run from this repo: `node package-skill.mjs`

   The archive nests everything under a `redfearn-group-style/` folder so
   unzipping produces a directory ready to drop into a skills location.

   skill/ in this repo stays the source of truth. The ZIP is a snapshot.
   Attach it to a GitHub release rather than committing it, so the repo
   does not accumulate binaries that duplicate what is already tracked.

   For the file that actually gets uploaded to Claude's skill importer,
   prefer running the skill-creator skill's own `scripts/package_skill.py`
   against a copy of skill/ staged under the name `redfearn-group-style/`
   instead of this script's output: it runs the same frontmatter checks
   as the real uploader before zipping, and produces a `.skill` file via
   Python's zipfile, which normalizes path separators and sets file mode
   bits that PowerShell's Compress-Archive (used below) leaves zeroed.
   This script is fine for the dated GitHub-release backup snapshot; it
   is not the thing to hand to the uploader. */

import { execFileSync } from "node:child_process";
import { existsSync, rmSync, mkdirSync, cpSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.join(ROOT, "skill");
const NAME = "redfearn-group-style";

if (!existsSync(SRC)) {
  console.error(`No skill/ directory at ${SRC}`);
  process.exit(1);
}

/* Mirrors the field checks in skill-creator's quick_validate.py. A skill
   with an oversized/malformed frontmatter field packages and zips just
   fine, then gets silently rejected on upload with an error message that
   has nothing to do with the actual cause (e.g. "invalid characters" for
   what was really an over-length description). Catch it here instead of
   finding out after a round trip through the uploader. */
function validateFrontmatter() {
  const content = readFileSync(path.join(SRC, "SKILL.md"), "utf-8");
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) {
    console.error("SKILL.md has no YAML frontmatter block.");
    process.exit(1);
  }
  const fm = match[1];
  const nameMatch = fm.match(/^name:\s*(.+)$/m);
  const descMatch = fm.match(/^description:\s*['"]?([\s\S]*?)['"]?$/m);

  const name = nameMatch?.[1]?.trim() ?? "";
  if (!/^[a-z0-9-]+$/.test(name) || name.length > 64) {
    console.error(`Invalid name "${name}": must be kebab-case, max 64 characters.`);
    process.exit(1);
  }

  // The description spans multiple lines when block-quoted; re-extract by
  // taking everything between "description:" and the closing quote/EOF
  // rather than trusting a single-line regex capture.
  const descBlockMatch = fm.match(/description:\s*['"]?([\s\S]*)/);
  const rawDesc = (descBlockMatch?.[1] ?? "").replace(/['"]\s*$/, "").trim();
  if (rawDesc.length > 1024) {
    console.error(`Description is ${rawDesc.length} characters, over the 1024 limit by ${rawDesc.length - 1024}.`);
    process.exit(1);
  }
  if (rawDesc.includes("<") || rawDesc.includes(">")) {
    console.error("Description contains angle brackets, which the uploader rejects.");
    process.exit(1);
  }
  console.log(`Frontmatter OK: name "${name}" (${name.length}/64), description ${rawDesc.length}/1024 chars.`);
}

validateFrontmatter();

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
