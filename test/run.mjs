/* Runs test/kit.test.ts against the kit.
   `node test/run.mjs` from the repo root.

   The kit ships bare relative imports ("./date"), which is what Astro and
   Vite expect. Node's type stripping requires explicit extensions, so the
   kit is copied to .kit-build/ with the imports rewritten rather than
   changing what ships. */
import { readdirSync, readFileSync, writeFileSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, ".kit-build");

rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

for (const f of readdirSync(path.join(ROOT, "kit")).filter((f) => f.endsWith(".ts"))) {
  const src = readFileSync(path.join(ROOT, "kit", f), "utf-8");
  writeFileSync(path.join(OUT, f), src.replace(/from "\.\/([a-zA-Z0-9_-]+)"/g, 'from "./$1.ts"'));
}

const r = spawnSync(process.execPath,
  ["--experimental-strip-types", "--no-warnings", path.join(ROOT, "test", "kit.test.ts")],
  { stdio: "inherit" });

rmSync(OUT, { recursive: true, force: true });
process.exit(r.status ?? 1);
