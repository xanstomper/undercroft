#!/usr/bin/env python3
"""
UNDERCROFT — Mandate CLI. Attack the hidden level beneath any system's documented
surface: bespoke code, shadow endpoints, rules/value flows, crafted PoCs.
stdlib-only. State: ~/.redteam/campaigns/<target>/undercroft-state.json

Commands:
  code        --target <c> --asset "<file|route|component>" --seam authn|authz|crypto|injection|trust [--note ...]
  surface     --target <c> --add "<endpoint>" --kind hidden|misused|legacy|admin --status PROBED|CONFIRMED|EXHAUSTED [--proof ...]
  logic       --target <c> --add "<rule seam>" --where "<flow>" --status PROBED|CONFIRMED|EXHAUSTED [--proof ...] [--delta "..."]
  probe       [--class precision|concurrency|arbitrage|entitlement|calculation|randomness|conversion|credits|boundary|journal|riskless|bounds|state|webhook|time]
  fuzz        --base "<origin[,origin...]>" [--methods GET,POST]
  drift       --target <c> [--days N]
  prioritize  --target <c>
  craft       --target <c> --add "<finding id>" --request "<one decisive test>" --proof "<read-only result>" --class IDOR|RACE|DESER|FMT|MATH|STATE|TIME|OTHER
  export      --target <c>          forge → 3AM learned-vectors.jsonl (schema-true)
  report      --target <c> [--output F]
  verify      self-check

Exit codes: 0 ok · 2 usage/state error.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from itertools import product
from pathlib import Path

SEAMS = ("authn", "authz", "crypto", "injection", "trust")
KINDS = ("hidden", "misused", "legacy", "admin")
STATUS = ("PROBED", "CONFIRMED", "EXHAUSTED")
CLASSES = ("IDOR", "RACE", "DESER", "FMT", "MATH", "STATE", "TIME", "OTHER")


def state_path(t):
    return Path.home() / ".redteam" / "campaigns" / t / "undercroft-state.json"


def load(t):
    p = state_path(t)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def save(t, st):
    p = state_path(t)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(st, indent=2) + "\n")


def base(t):
    st = load(t)
    if st is None:
        st = {"target": t, "code": [], "surface": [], "logic": [], "pocs": [],
              "created": datetime.now(timezone.utc).isoformat()}
        save(t, st)
    return st


def cmd_code(args):
    st = base(args.target)
    if args.seam not in SEAMS:
        print(f"✗ seam {SEAMS}", file=sys.stderr)
        return 2
    st.setdefault("code", []).append({"asset": args.asset, "seam": args.seam,
                                      "note": args.note or "",
                                      "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    print(f"▸ code seam: {args.asset} [{args.seam}]" + (f" — {args.note[:70]}" if args.note else ""))
    return 0


def cmd_surface(args):
    st = base(args.target)
    if args.kind not in KINDS or args.status not in STATUS:
        print(f"✗ kind {KINDS} · status {STATUS}", file=sys.stderr)
        return 2
    s = st.setdefault("surface", [])
    if any(x.get("endpoint") == args.add for x in s):
        for x in s:
            if x.get("endpoint") == args.add:
                x.update({"kind": args.kind, "status": args.status, "proof": args.proof or "",
                          "at": datetime.now(timezone.utc).isoformat()})
        save(args.target, st)
        print(f"▸ surface updated: {args.add} → {args.status}")
        return 0
    s.append({"endpoint": args.add, "kind": args.kind, "status": args.status,
              "proof": args.proof or "", "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    print(f"▸ surface: {args.add} [{args.kind}] {args.status}")
    return 0


def cmd_logic(args):
    st = base(args.target)
    if args.status not in STATUS:
        print(f"✗ status {STATUS}", file=sys.stderr)
        return 2
    l = st.setdefault("logic", [])
    if any(x.get("seam") == args.add for x in l):
        for x in l:
            if x.get("seam") == args.add:
                x.update({"where": args.where or "", "status": args.status,
                          "proof": args.proof or "", "delta": args.delta or "",
                          "at": datetime.now(timezone.utc).isoformat()})
        save(args.target, st)
        print(f"▸ logic updated: {args.add} → {args.status}")
        return 0
    l.append({"seam": args.add, "where": args.where or "", "status": args.status,
              "proof": args.proof or "", "delta": args.delta or "",
              "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    print(f"▸ logic seam: {args.add} ({args.where}) {args.status}" + (f" Δ {args.delta[:60]}" if args.delta else ""))
    return 0


def cmd_craft(args):
    st = base(args.target)
    if args.cls not in CLASSES:
        print(f"✗ class {CLASSES}", file=sys.stderr)
        return 2
    st.setdefault("pocs", []).append({"finding": args.add, "request": args.request,
                                      "proof": args.proof, "class": args.cls,
                                      "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    print(f"▸ PoC crafted: {args.add} [{args.cls}] — {args.request[:60]}")
    print("  → feed family: 3AM learn+promote (vector registry growth)")
    return 0


def cmd_report(args):
    st = base(args.target)
    out = args.output or f"{args.target}-undercroft-report.md"
    L = [f"# UNDERCROFT Report — {args.target}", ""]
    L.append("## Custom-code seams")
    L += [f"- {c['asset']} [{c['seam']}]" + (f" — {c['note']}" if c.get("note") else "") for c in st.get("code", [])]
    if not st.get("code"):
        L.append("- none")
    L += ["", "## Shadow surface"]
    for s in st.get("surface", []):
        L.append(f"- {s['endpoint']} [{s['kind']}] {s['status']}" + (f" — {s['proof']}" if s.get("proof") else ""))
    if not st.get("surface"):
        L.append("- none")
    L += ["", "## Rules & value flows"]
    for l in st.get("logic", []):
        L.append(f"- {l['status']} — {l['seam']} (in {l['where']})"
                 + (f" Δ {l['delta']}" if l.get("delta") else "")
                 + (f" proof: {l['proof']}" if l.get("proof") else ""))
    if not st.get("logic"):
        L.append("- none")
    L += ["", "## Crafted PoCs (family register)"]
    for p in st.get("pocs", []):
        L.append(f"- **{p['finding']}** [{p['class']}]: {p['request']} → {p['proof']}")
    if not st.get("pocs"):
        L.append("- none")
    Path(out).write_text("\n".join(L) + "\n")
    print(f"▸ undercroft report written: {out}")
    return 0


def cmd_verify(args):
    bad = []
    self = Path(__file__).resolve()
    if subprocess.run([sys.executable, "-m", "py_compile", str(self)],
                      capture_output=True).returncode != 0:
        bad.append("compile")
    help_out = subprocess.run([sys.executable, str(self), "--help"],
                              capture_output=True, text=True).stdout
    for want in ("code", "surface", "logic", "craft", "probe", "fuzz",
                 "drift", "prioritize", "export", "report", "verify"):
        if want not in help_out:
            bad.append(f"subcommand {want}")
    tmpl = Path(__file__).resolve().parent.parent / "templates" / "undercroft-state.json"
    if tmpl.exists():
        try:
            json.loads(tmpl.read_text())
        except Exception:
            bad.append("template json")
    if bad:
        print(f"✗ UNDERCROFT verify FAILED: {bad}")
        return 1
    print("✓ UNDERCROFT verify: compile · subcommands · template — ALL PASS")
    return 0


# ── probe-plan engine (15 universal seam classes) ────────────────────────────

PROBES = {
    "precision": ("Value :: rounding/precision", [
        ("Δ", "amounts at max precision + unit conversion (currency, %, units)"),
        ("probe", "submit crafted amount × N repetitions on own account"),
        ("verify", "reconciled result drifts ≥ 1 smallest unit after N ops"),
        ("cost", "N × smallest unit, fully reversible (refund each op)"),
        ("confirmed_when", "balance/statement ≠ naive sum; drift recorded"),
    ]),
    "concurrency": ("State :: double-spend / parallel submits", [
        ("Δ", "N parallel submits of the SAME logical unit (own account)"),
        ("probe", "fire concurrently (no await between); watch state + journal"),
        ("verify", "two ops accepted against one state; negative state possible"),
        ("cost", "one unit + refunds; nothing leaves the estate"),
        ("confirmed_when", "journal shows double-count or inconsistent state"),
    ]),
    "arbitrage": ("Value :: price/quote inconsistency", [
        ("Δ", "two correlated values priced inconsistently on own account"),
        ("probe", "minimal opposing actions exploiting the gap"),
        ("verify", "guaranteed gain > 0 exists for any outcome"),
        ("cost", "minimal units, reversed"),
        ("confirmed_when", "riskless-gain window proven"),
    ]),
    "entitlement": ("Privilege :: promo/trial/referral abuse", [
        ("Δ", "re-order or parallel-claim the documented grant flow"),
        ("probe", "claim N× via flow-order inversion (own account)"),
        ("verify", "terms-bypass: grant duplicated beyond entitlement"),
        ("cost", "nothing kept; reversed"),
        ("confirmed_when", "duplicate/extra grant accepted"),
    ]),
    "calculation": ("Value :: calc overpay/divergence", [
        ("Δ", "inputs outside documented bounds through the calc"),
        ("probe", "crafted boundary values at minimum stakes/quantities"),
        ("verify", "result diverges from independent calculation"),
        ("cost", "floor units, reversed"),
        ("confirmed_when", "settled result ≠ expected formula"),
    ]),
    "randomness": ("Outcomes :: RNG structure/bias", [
        ("Δ", "commit-reveal analysis: seed/nonce reuse, timing, distribution"),
        ("probe", "N observed outcomes on own account; check structure + uniformity"),
        ("verify", "nonce reuse / measurable bias / seed-timing correlation"),
        ("cost", "observation-only where possible; floor units otherwise"),
        ("confirmed_when", "divergence beyond documented tolerance"),
    ]),
    "conversion": ("Value :: conversion/fee asymmetry", [
        ("Δ", "conversion chains with fractional fees and rounding direction"),
        ("probe", "round-trip own balance A→B→A at boundary amounts"),
        ("verify", "round-trip ≠ 0 drift; fee-direction inconsistency"),
        ("cost", "conversion fees only, reversed"),
        ("confirmed_when", "nonzero drift or exploitable asymmetry"),
    ]),
    "credits": ("Value :: credits/points economy", [
        ("Δ", "earn/burn inversion or multi-account merge (own accounts)"),
        ("probe", "burn→refund ordering; merge arithmetic"),
        ("verify", "credit created from nothing / negative pool"),
        ("cost", "own credits only"),
        ("confirmed_when", "balance injection or inversion"),
    ]),
    "boundary": ("Privilege :: multi-tenant / plan limits", [
        ("Δ", "org/plan/tenant id switch in scoped requests"),
        ("probe", "cross-tenant read with own identity (id in body/param)"),
        ("verify", "foreign resource 200"),
        ("cost", "read-only"),
        ("confirmed_when", "unauthorized boundary crossed"),
    ]),
    "journal": ("State :: statement/journal integrity", [
        ("Δ", "statement pagination or snapshot/current divergence"),
        ("probe", "paged reads vs journal sum; cancelled/voided entries"),
        ("verify", "statement ≠ journal; voided op still counted"),
        ("cost", "read-only"),
        ("confirmed_when", "reconciliation gap on own account"),
    ]),
    "riskless": ("Value :: riskless-asset scope", [
        ("Δ", "spendability scope of demo/trial/free assets (allowlist)"),
        ("probe", "use free asset on restricted instrument/feature"),
        ("verify", "asset accepted where terms forbid"),
        ("cost", "free assets only, reversed"),
        ("confirmed_when", "terms-bypass accept"),
    ]),
    "bounds": ("Input :: validation bounds", [
        ("Δ", "max+1 / negative / fractional precision through validation"),
        ("probe", "boundary inputs on own account"),
        ("verify", "accepted / settled with altered semantics"),
        ("cost", "floor-adjacent, reversed"),
        ("confirmed_when", "out-of-bounds accepted"),
    ]),
    "state": ("State :: state-machine bypass", [
        ("Δ", "out-of-order transitions on order/workflow/approval flows"),
        ("probe", "drive the flow with transition N+2 before N+1 (own objects)"),
        ("verify", "illegal-but-accepted state; skipped guard effects"),
        ("cost", "own objects only; reversible"),
        ("confirmed_when", "flow completes in an undocumented state"),
    ]),
    "webhook": ("State :: replay / idempotency", [
        ("Δ", "replay a captured callback with the same dedup key (own endpoint)"),
        ("probe", "re-send captured callback N×; observe effects"),
        ("verify", "duplicate effect applied / no idempotency guard"),
        ("cost", "own endpoints only"),
        ("confirmed_when", "replay accepted with duplicate effect"),
    ]),
    "time": ("State :: expiry/TTL/grace edges", [
        ("Δ", "act just before/after documented expiry or grace boundary"),
        ("probe", "boundary-crossing requests on own objects (clock skew if permitted)"),
        ("verify", "expired-but-accepted / pre-expiry grant"),
        ("cost", "read-only or reversible"),
        ("confirmed_when", "TTL logic diverges from documented behavior"),
    ]),
}

ROUTE_WORDS = ["v1", "v2", "v3", "internal", "admin", "debug", "metrics", "health",
               "status", "actuator", "webhook", "callback", "test", "staging",
               "beta", "dev", "preview", "sandbox", "mobile", "partner", "affiliate",
               "bonus", "odds", "cashier", "payments", "wallet", "promo", "raffle",
               "leaderboard", "jackpot", "tournament", "config", "migration", "cron",
               "export", "import", "backup", "swagger", "openapi", "graphql", "rpc"]

CLASS_MAP = {  # UNDERCROFT PoC class → 3AM (flaw, seam)
    "IDOR": (6, "C"), "RACE": (5, "B"), "DESER": (3, "C"), "FMT": (9, "C"),
    "MATH": (10, "C"), "STATE": (5, "B"), "TIME": (1, "C"), "OTHER": (1, "C"),
}
FLAW_NAMES = {1: "validation-order", 3: "type-coercion", 5: "state-machine-gaps",
              6: "identifier-trust", 9: "header/parser-differential", 10: "entropy/forge"}
SEAM_NAMES = {"B": "client<->server-validation", "C": "auth<->backend-binding"}


def cmd_probe(args):
    if args.cls and args.cls not in PROBES:
        print(f"✗ seam class {list(PROBES)}", file=sys.stderr)
        return 2
    names = [args.cls] if args.cls else list(PROBES)
    for n in names:
        title, steps = PROBES[n]
        print(f"━━ {n} — {title}")
        for k, v in steps:
            print(f"  {k:13s} {v}")
    return 0


def cmd_fuzz(args):
    methods = args.methods.upper().split(",") if args.methods else ["GET", "POST"]
    bases = [b for b in args.base.split(",") if b]
    cands = []
    for b, w in product(bases, ROUTE_WORDS):
        cands.append(f"{b}/{w}")
    for b in bases:
        for w in ROUTE_WORDS:
            cands.append(f"{b}/api/{w}")
    seen, out = set(), []
    for c in cands:
        if c not in seen:
            seen.add(c)
            for m in methods:
                out.append(f"{m} {c}")
    chunk = 25
    for i in range(0, len(out), chunk):
        print(f"▸ burst {i // chunk + 1} ({chunk} candidates)")
        for line in out[i:i + chunk]:
            print(f"  {line}")
    print(f"▸ {len(out)} candidates in {len(out) // chunk + 1} bursts "
          f"(noise-budget chunked; one request per candidate)")
    return 0


def cmd_drift(args):
    st = base(args.target)
    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()
    hits = []
    for group in ("surface", "logic"):
        for x in st.get(group, []):
            if x.get("status") == "CONFIRMED" and x.get("at", "") < cutoff:
                hits.append((group, x))
    if not hits:
        print("▸ no stale CONFIRMED seams — nothing to re-verify")
        return 0
    for g, x in hits:
        print(f"  ! {g}: {x.get('endpoint') or x.get('seam')} CONFIRMED at {x.get('at')} "
              f"— re-verify (drift before re-assert)")
    print(f"▸ {len(hits)} stale seam(s) — re-probe or update state")
    return 0


def cmd_prioritize(args):
    st = base(args.target)
    value = {"surface": 2, "logic": 3, "code": 3}
    rows = []
    for g, items in (("surface", st.get("surface", [])), ("logic", st.get("logic", []))):
        for x in items:
            if x.get("status") in ("PROBED", "CONFIRMED"):
                rows.append((value[g], x.get("endpoint") or x.get("seam"), g, x.get("status")))
    rows.sort(reverse=True)
    print("▸ ATTACK ORDER (value × status)")
    for i, (v, name, g, s) in enumerate(rows, 1):
        print(f"  {i:2d}. ({v}) [{g}] {name} — {s}")
    if not rows:
        print("  (no opened seams)")
    return 0


def cmd_export(args):
    st = base(args.target)
    pocs = [p for p in st.get("pocs", []) if p.get("proof")]
    if not pocs:
        print("✗ no crafted PoCs with proof — craft first", file=sys.stderr)
        return 2
    learned = Path.home() / ".redteam" / "learned-vectors.jsonl"
    learned.parent.mkdir(parents=True, exist_ok=True)
    for p in pocs:
        flaw, seam = CLASS_MAP.get(p.get("class"), CLASS_MAP["OTHER"])
        row = {"flaw": flaw, "seam": seam,
               "probe": f"UNDERCROFT {p['class']} :: {p['request']}",
               "confirmed_when": p["proof"]}
        with learned.open("a") as f:
            f.write(json.dumps(row) + "\n")
        print(f"▸ exported → {learned}: flaw={flaw}({FLAW_NAMES[flaw]}) seam={seam}"
              f"({SEAM_NAMES[seam]}) :: {p['request'][:60]}")
    print(f"\n  next: 3AM promote --apply --verified   (merges into scripts/matrix.json)")
    return 0


def main():
    ap = argparse.ArgumentParser(description="UNDERCROFT — custom-surface mandate CLI")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("code", help="custom-code seam")
    c.add_argument("--target", required=True)
    c.add_argument("--asset", required=True)
    c.add_argument("--seam", required=True, choices=SEAMS)
    c.add_argument("--note")
    s = sub.add_parser("surface", help="shadow-surface ledger")
    s.add_argument("--target", required=True)
    s.add_argument("--add", required=True)
    s.add_argument("--kind", required=True, choices=KINDS)
    s.add_argument("--status", required=True, choices=STATUS)
    s.add_argument("--proof")
    l = sub.add_parser("logic", help="rules/value-flow seam")
    l.add_argument("--target", required=True)
    l.add_argument("--add", required=True)
    l.add_argument("--where", required=True)
    l.add_argument("--status", required=True, choices=STATUS)
    l.add_argument("--proof")
    l.add_argument("--delta")
    f = sub.add_parser("craft", help="crafted PoC (family register)")
    f.add_argument("--target", required=True)
    f.add_argument("--add", required=True)
    f.add_argument("--request", required=True)
    f.add_argument("--proof", required=True)
    f.add_argument("--class", dest="cls", required=True, choices=CLASSES)
    r = sub.add_parser("report", help="undercroft report")
    r.add_argument("--target", required=True)
    r.add_argument("--output")
    v = sub.add_parser("verify", help="self-check")
    v.add_argument("--target")
    pr = sub.add_parser("probe", help="probe-plan engine (NO-GAIN plans per seam class)")
    pr.add_argument("--class", dest="cls", choices=list(PROBES), help="omit for the full table")
    fz = sub.add_parser("fuzz", help="shadow-surface route-candidate generator (chunked bursts)")
    fz.add_argument("--base", required=True)
    fz.add_argument("--methods", help="comma methods, default GET,POST")
    df = sub.add_parser("drift", help="stale-CONFIRMED re-verify flags")
    df.add_argument("--target", required=True)
    df.add_argument("--days", type=int, default=1)
    pi = sub.add_parser("prioritize", help="attack order (value × status)")
    pi.add_argument("--target", required=True)
    ex = sub.add_parser("export", help="forge → 3AM learned-vectors.jsonl")
    ex.add_argument("--target", required=True)
    a = ap.parse_args()
    if a.cmd == "code":
        return cmd_code(a)
    if a.cmd == "surface":
        return cmd_surface(a)
    if a.cmd == "logic":
        return cmd_logic(a)
    if a.cmd == "craft":
        return cmd_craft(a)
    if a.cmd == "probe":
        return cmd_probe(a)
    if a.cmd == "fuzz":
        return cmd_fuzz(a)
    if a.cmd == "drift":
        return cmd_drift(a)
    if a.cmd == "prioritize":
        return cmd_prioritize(a)
    if a.cmd == "export":
        return cmd_export(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "verify":
        return cmd_verify(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())