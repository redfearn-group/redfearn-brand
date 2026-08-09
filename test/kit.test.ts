import { formatDate, formatMonth, addMonths, daysBetween, today } from "../.kit-build/date.ts";
import { dateDue } from "../.kit-build/due.ts";

let fail = 0;
const eq = (label: string, got: unknown, want: unknown) => {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (!ok) { fail++; console.log(`  FAIL ${label}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`); }
  else console.log(`  ok   ${label}`);
};

console.log("formatDate");
eq("plain", formatDate("2023-06-19"), "19 Jun 2023");
eq("null default", formatDate(null), "");
eq("null with empty opt", formatDate(null, { empty: "\u2014" }), "\u2014");
eq("non-date passthrough", formatDate("whenever"), "whenever");
eq("backward compat 1-arg", formatDate("2026-01-01"), "01 Jan 2026");

console.log("formatMonth");
eq("yyyy-mm", formatMonth("2026-06"), "Jun 2026");
eq("yyyy-mm-dd", formatMonth("2026-06-14"), "Jun 2026");
eq("null", formatMonth(null, { empty: "\u2014" }), "\u2014");

console.log("addMonths (must match the 3 replaced impls exactly)");
eq("overflow 31 Jan +1", addMonths("2026-01-31", 1), "2026-03-03");
eq("overflow 31 Jan +3", addMonths("2026-01-31", 3), "2026-05-01");
eq("leap +12", addMonths("2024-02-29", 12), "2025-03-01");
eq("year roll", addMonths("2026-12-15", 1), "2027-01-15");
eq("negative", addMonths("2026-03-15", -2), "2026-01-15");
eq("bad input", addMonths("nope", 1), null);

console.log("daysBetween");
eq("forward", daysBetween("2026-08-08", "2026-08-18"), 10);
eq("backward", daysBetween("2026-08-18", "2026-08-08"), -10);
eq("same", daysBetween("2026-08-08", "2026-08-08"), 0);
eq("bad", daysBetween("x", "2026-08-08"), null);

console.log("today() is local, not UTC");
const d = new Date();
const p = (n: number) => String(n).padStart(2, "0");
eq("matches local calendar day", today(), `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())}`);

console.log("dateDue");
eq("never done", dateDue({ lastDone: null, intervalMonths: 6, today: "2026-08-08", dueSoonDays: 30 }),
   { dueDate: null, overdue: false, dueSoon: false });
eq("no interval", dateDue({ lastDone: "2026-01-01", intervalMonths: null, today: "2026-08-08", dueSoonDays: 30 }),
   { dueDate: null, overdue: false, dueSoon: false });
eq("ok", dateDue({ lastDone: "2026-06-01", intervalMonths: 6, today: "2026-08-08", dueSoonDays: 30 }),
   { dueDate: "2026-12-01", overdue: false, dueSoon: false });
eq("due soon boundary (30)", dateDue({ lastDone: "2026-03-07", intervalMonths: 6, today: "2026-08-08", dueSoonDays: 30 }),
   { dueDate: "2026-09-07", overdue: false, dueSoon: true });
eq("overdue", dateDue({ lastDone: "2026-01-01", intervalMonths: 6, today: "2026-08-08", dueSoonDays: 30 }),
   { dueDate: "2026-07-01", overdue: true, dueSoon: false });
eq("due exactly today counts overdue", dateDue({ lastDone: "2026-02-08", intervalMonths: 6, today: "2026-08-08", dueSoonDays: 30 }),
   { dueDate: "2026-08-08", overdue: true, dueSoon: false });

console.log(fail === 0 ? "\nALL PASS" : `\n${fail} FAILURES`);
process.exit(fail === 0 ? 0 : 1);
