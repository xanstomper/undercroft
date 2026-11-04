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
                 "drift", "prioritize", "export", "report", "verify",
                 "scan", "stateflow", "replay", "precision", "entropy", "corpus",
                 "map", "descend", "run", "jwt"):
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


# ── v2.1.0 descent kit ────────────────────────────────────────────────────────

SCAN_PATTERNS = [
    ("trust", "client-side auth/role state", r"(localStorage|sessionStorage)[.\[]\s*['\"]?[^'\"]*(token|jwt|auth|admin|role|perm)"),
    ("trust", "admin/role flag in client state", r"(isAdmin|is_admin|admin['\"]?\s*[:=]\s*(true|1|yes)|role['\"]?\s*[:=]\s*['\"]admin)"),
    ("injection", "HTML sink (XSS)", r"(innerHTML|outerHTML|document\.write|dangerouslySetInnerHTML)\s*[=(]"),
    ("injection", "dynamic code execution", r"\beval\s*\(|new\s+Function\s*\(|setTimeout\s*\(\s*['\"]"),
    ("crypto", "hardcoded secret/credential", r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"),
    ("crypto", "hardcoded JWT", r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}"),
    ("authz", "org/tenant id in client calls (boundary candidates)", r"(?i)(org[_-]?id|tenant[_-]?id|workspace[_-]?id|account[_-]?id)\s*[:=]"),
    ("trust", "client-assigned value fields", r"(?i)\.(price|total|amount|balance|quantity|discount)\s*=\s*"),
    ("injection", "SQL by concat", r'''(?i)(SELECT|INSERT|UPDATE|DELETE)[^;'"]*['"]\s*\+|\.query\s*\([^)]*\+'''),
    ("trust", "open redirect sink", r"(window\.location\s*=|location\.href\s*=|location\.replace\s*\()"),
    ("trust", "postMessage wildcard target", r"postMessage\s*\([^)]*,\s*['\"]\*['\"]"),
    ("crypto", "weak/own crypto usage", r"(?i)\b(md5|sha1|des|ecb|createCipher)\b"),
]
SOURCE_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".py", ".php", ".rb", ".go", ".json", ".html"}


def _iter_sources(path):
    p = Path(path).expanduser()
    if p.is_file():
        yield p
        return
    for f in sorted(p.rglob("*")):
        if f.is_file() and f.suffix.lower() in SOURCE_EXTS and f.stat().st_size < 5_000_000:
            yield f


def _scan_findings(path):
    """Static seam scan over bundles/source. Returns findings list."""
    import re as _re
    compiled = [(seam, desc, _re.compile(rx)) for seam, desc, rx in SCAN_PATTERNS]
    findings = []
    for f in _iter_sources(path):
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for seam, desc, rx in compiled:
                m = rx.search(line)
                if m:
                    findings.append({"file": str(f), "line": lineno, "seam": seam,
                                     "desc": desc, "match": line.strip()[:110],
                                     "at": datetime.now(timezone.utc).isoformat()})
    return findings


def cmd_scan(args):
    """Static seam scanner: bundles/source → undercroft seams (read-only, local)."""
    findings = _scan_findings(args.path)
    by_seam = {}
    for x in findings:
        by_seam.setdefault(x["seam"], []).append(x)
    print(f"▸ scan: {args.path} — {len(findings)} seam hits")
    for seam in sorted(by_seam):
        print(f"  [{seam}] ×{len(by_seam[seam])}")
        for x in by_seam[seam][:args.limit]:
            print(f"    {x['file']}:{x['line']}  {x['desc']}")
            print(f"      └ {x['match'][:100]}")
    if args.target:
        st = base(args.target)
        code = st.setdefault("code", [])
        known = {(c.get("asset"), c.get("seam")) for c in code}
        for x in findings:
            key = (f"{x['file']}:{x['line']}", x["seam"])
            if key not in known:
                code.append({"asset": key[0], "seam": x["seam"],
                             "note": f"scan: {x['desc']}",
                             "at": datetime.now(timezone.utc).isoformat()})
        save(args.target, st)
        print(f"▸ registered into {args.target} code ledger")
    return 0


def cmd_stateflow(args):
    """Out-of-order transition bypass matrix for a declared flow."""
    states = [s.strip() for s in args.states.split(",") if s.strip()]
    if len(states) < 3:
        print("✗ need ≥3 states", file=sys.stderr)
        return 2
    guards = {}
    for g in (args.guard or "").split(","):
        if ":" in g:
            dst, pre = g.split(":", 1)
            guards[dst.strip()] = pre.strip()
    print(f"▸ stateflow: {' → '.join(states)}")
    print(f"  guards: {guards or 'none declared'}")
    n = 0
    for i, dst in enumerate(states):
        if i == 0:
            continue
        for j, cur in enumerate(states):
            if j >= i:
                continue
            n += 1
            skipped = states[j + 1:i]
            note = f" (skips: {', '.join(skipped)})" if skipped else ""
            print(f"  {n:2d}. fire '{dst}' while at '{cur}'{note}")
            if dst in guards and guards[dst] in skipped:
                print(f"      └ GUARD BYPASS candidate: '{dst}' declares guard '{guards[dst]}'")
    if args.target:
        st = base(args.target)
        st.setdefault("logic", []).append({
            "seam": f"stateflow {'→'.join(states)}", "where": args.flow or "declared flow",
            "status": "PROBED", "proof": "", "delta": f"{n} out-of-order probes",
            "at": datetime.now(timezone.utc).isoformat()})
        save(args.target, st)
        print(f"▸ registered {n}-probe matrix into {args.target} logic ledger")
    return 0


def cmd_replay(args):
    """Idempotency/replay harness: same request N times, diff responses."""
    import hashlib
    import urllib.error
    import urllib.request
    if args.method.upper() in ("POST", "PUT", "PATCH", "DELETE") and not args.confirm:
        print("✗ state-changing replay needs --confirm (own endpoints only)", file=sys.stderr)
        return 2
    req_headers = {"User-Agent": "undercroft/2.1"}
    for h in args.header or []:
        k, _, v = h.partition(":")
        req_headers[k.strip()] = v.strip()
    body = args.body.encode() if args.body else None
    if body and args.method.upper() in ("POST", "PUT", "PATCH"):
        req_headers.setdefault("Content-Type", "application/json")
    seen, results = {}, []
    for i in range(1, args.times + 1):
        r = urllib.request.Request(args.url, data=body, method=args.method.upper(),
                                   headers=req_headers)
        try:
            with urllib.request.urlopen(r, timeout=args.timeout) as resp:
                payload, code = resp.read(), resp.status
        except urllib.error.HTTPError as e:
            payload, code = e.read(), e.code
        except Exception as e:
            print(f"  {i}: transport error — {e}")
            continue
        h = hashlib.sha256(payload).hexdigest()[:12]
        results.append((i, code, h, len(payload)))
        seen.setdefault(h, []).append(i)
    for i, code, h, size in results:
        print(f"  {i}: {code} · {h} · {size}B")
    distinct = len({h for _, _, h, _ in results})
    print(f"▸ {len(results)} replays → {distinct} distinct response(s)")
    if distinct > 1:
        print("  ! IDEMPOTENCY GAP — identical request produced different effects")
        if args.target:
            st = base(args.target)
            st.setdefault("logic", []).append({
                "seam": "idempotency/replay", "where": args.url, "status": "CONFIRMED",
                "proof": f"{distinct} distinct responses over {len(results)} replays",
                "delta": f"{args.method} ×{args.times}", "at": datetime.now(timezone.utc).isoformat()})
            save(args.target, st)
            print(f"▸ registered CONFIRMED into {args.target} logic ledger")
    return 0


def cmd_precision(args):
    """Drift calculator: float math vs exact decimal → worst crafted amount."""
    from decimal import Decimal, ROUND_FLOOR, ROUND_DOWN, ROUND_HALF_UP
    modes = {"floor": ROUND_FLOOR, "trunc": ROUND_DOWN, "round": ROUND_HALF_UP}
    rnd = modes.get(args.mode, ROUND_HALF_UP)
    price, rate, ops = Decimal(str(args.price)), Decimal(str(args.rate)), args.ops
    exact_total = Decimal(0)
    float_total = 0.0
    worst = None
    for i in range(ops):
        amt = price * (Decimal(1) + Decimal(i) / Decimal(10 ** 6))
        fee_exact = (amt * rate).quantize(Decimal("0.01"), rounding=rnd)
        exact_total += fee_exact
        f = float(amt) * float(rate)
        fee_float = float(Decimal(str(round(f, 2)) if rnd == ROUND_HALF_UP else
                                  (str(int(f * 100) / 100) if rnd != ROUND_FLOOR else
                                   str((Decimal(str(f)).quantize(Decimal("0.01"), rounding=ROUND_FLOOR))))))
        float_total += fee_float
        d = abs(Decimal(str(fee_float)) - fee_exact)
        if worst is None or d > worst[1]:
            worst = (str(amt.quantize(Decimal("0.000001")).normalize()), d)
    print(f"▸ precision: price={price} rate={rate} mode={args.mode} ops={ops}")
    print(f"  exact total:    {exact_total}")
    print(f"  float total:    {float_total}")
    drift = abs(Decimal(str(float_total)) - exact_total)
    print(f"  total drift:    {drift}  (per-op worst: {worst[1]} at amount {worst[0]})")
    if drift > 0:
        print(f"  → crafted-input candidates: {worst[0]} class amounts; drift grows linearly with ops")
    return 0


def cmd_entropy(args):
    """Token/OTP entropy estimator: samples → effective bits + patterns."""
    from collections import Counter
    from math import log2
    if args.samples:
        samples = args.samples.split()
    elif args.file:
        samples = [l.strip() for l in Path(args.file).read_text().splitlines() if l.strip()]
    else:
        print("✗ need --samples or --file", file=sys.stderr)
        return 2
    if len(samples) < 5:
        print("✗ need ≥5 samples", file=sys.stderr)
        return 2
    uniq = len(set(samples))
    lengths = Counter(len(s) for s in samples)
    alphabets = Counter(ch for s in samples for ch in s)
    total_chars = sum(alphabets.values())
    shannon = -sum((c / total_chars) * log2(c / total_chars) for c in alphabets.values())
    prefixes = Counter(s[:3] for s in samples)
    top_prefix, top_n = prefixes.most_common(1)[0]
    print(f"▸ entropy: {len(samples)} samples, {uniq} unique ({100 * uniq / len(samples):.0f}%)")
    print(f"  lengths: {dict(sorted(lengths.items()))}")
    print(f"  alphabet size: {len(alphabets)} · Shannon/char: {shannon:.2f} bits")
    print(f"  common 3-char prefix: '{top_prefix}' on {top_n}/{len(samples)} samples")
    bits = shannon * (sum(lengths.values()) / len(samples))
    print(f"  effective entropy ≈ {bits:.1f} bits/token")
    if uniq < len(samples):
        print("  ! DUPLICATES present — reuse detected")
    if top_n / len(samples) > 0.2:
        print(f"  ! COUNTER/PATTERN suspicion — {top_n}/{len(samples)} share prefix '{top_prefix}'")
    if len(alphabets) <= 16:
        print(f"  ! SMALL ALPHABET ({len(alphabets)} chars) — brute-forceable window")
    return 0


def cmd_corpus(args):
    """Boundary-input corpus generator per type."""
    corpora = {
        "money": ["0", "0.005", "0.015", "0.1", "0.3", "1e-8", "9007199254.099", "1e308",
                  "-0.01", "-1", "0.1+0.2", "99999999999999999999", "0x10", "1_000",
                  "1.0000000000000001", "%2e2e", "１２３ (fullwidth)"],
        "int": ["-1", "0", "1", "2147483647", "2147483648", "-2147483648", "9223372036854775807",
                "9223372036854775808", "0x41", "0b101", "1e5", "1_000", "007", " 7", "7 "],
        "string": ["", " ", "%00", "\x00", "A" * 5000, "../../etc/passwd", "%c0%af",
                   "‮unicode bidi", "𝕏𝕐𝕏 unicode", "f'%s' format", "${jndi:x}", "null", "undefined"],
        "json": ['{"a":1}', '{"a":[1,2]}', '[{"a":{"b":[{}]}}]', '{"a":null}', '{"a":"1"}',
                 '{"a":1e400}', '{"a":-0}', '{"a":[]}', '"string"', '[]', 'null',
                 '{"__proto__":{"isAdmin":true}}', '{"a":{"length":1e9}}'],
        "date": ["1970-01-01", "1970-01-01T00:00:00Z", "9999-12-31", "2024-02-29", "2023-02-29",
                 "2024-03-10T02:30:00 (DST gap)", "2024-11-03T01:30:00 (DST overlap)",
                 "-0001-01-01", "now", "+10000-01-01"],
    }
    if args.type not in corpora:
        print(f"✗ type {list(corpora)}", file=sys.stderr)
        return 2
    print(f"▸ corpus: {args.type} ({len(corpora[args.type])} inputs)")
    for x in corpora[args.type]:
        print(f"  {x}")
    return 0


# ── v2.2.0 domain maps + the descend loop ─────────────────────────────────────

DOMAIN_MAP = {
    "e-commerce": [("state", "checkout flow states", "cart→paid→fulfilled handlers"),
                   ("webhook", "payment callback idempotency", "webhook handler"),
                   ("precision", "refund/partial-math", "refund endpoint math"),
                   ("arbitrage", "price/quote inconsistency", "pricing/quote endpoints"),
                   ("entitlement", "coupon stacking", "cart apply endpoint"),
                   ("bounds", "quantity/input validation", "cart/order inputs"),
                   ("concurrency", "inventory decrement race", "checkout reserve"),
                   ("boundary", "multi-seller tenant reads", "seller-scoped endpoints")],
    "fintech": [("precision", "fee/interest math", "fee calculation"),
                ("conversion", "FX asymmetry", "conversion endpoint"),
                ("journal", "ledger/statement integrity", "statements + journal"),
                ("concurrency", "double-spend", "transfer/withdraw endpoints"),
                ("bounds", "withdrawal limits", "withdraw validation"),
                ("state", "transaction state machine", "txn workflow"),
                ("webhook", "idempotency keys", "payment callbacks"),
                ("randomness", "OTP entropy", "auth/OTP delivery")],
    "saas": [("boundary", "plan/seat limits", "seat & quota endpoints"),
             ("entitlement", "seat/feature inflation", "invites & feature gates"),
             ("precision", "proration math", "plan-change math"),
             ("time", "trial/TTL logic", "trial expiry checks"),
             ("state", "subscription workflow", "sub state machine"),
             ("journal", "usage metering", "metering pipeline")],
    "booking": [("concurrency", "double-book race", "reserve endpoint"),
                ("state", "booking state machine", "booking workflow"),
                ("time", "cancellation windows", "cancel/refund policy"),
                ("boundary", "cross-org reads", "org-scoped queries"),
                ("precision", "proration/refund math", "cancellation math"),
                ("journal", "void counting", "booking ledger")],
    "social": [("credits", "rate/credit economies", "boosts/credits"),
               ("entitlement", "referral loops", "referral handler"),
               ("boundary", "workspace/org reads", "scoped queries"),
               ("state", "moderation workflow", "report flow"),
               ("randomness", "matchmaking/feed", "assignment logic"),
               ("webhook", "fanout replay", "integration callbacks")],
    "gaming": [("randomness", "RNG structure", "outcome engine"),
               ("entitlement", "loot/bonus flows", "reward handlers"),
               ("precision", "odds/payout math", "shipped odds tables"),
               ("credits", "currency economy", "shop/wallet"),
               ("state", "match/round flow", "game state machine"),
               ("conversion", "shop math", "currency exchange")],
    "infra": [("entitlement", "device/tenant claim", "provisioning API"),
              ("webhook", "command replay", "device command queue"),
              ("state", "OTA/update flow", "update state machine"),
              ("journal", "telemetry integrity", "telemetry pipeline"),
              ("time", "cert/token TTL", "device auth"),
              ("boundary", "fleet tenant reads", "fleet-scoped queries")],
}
DOMAIN_ALIASES = {"commerce": "e-commerce", "shop": "e-commerce", "payments": "fintech",
                  "fintech": "fintech", "saas": "saas", "booking": "booking",
                  "travel": "booking", "social": "social", "gaming": "gaming",
                  "casino": "gaming", "infra": "infra", "iot": "infra"}


def cmd_map(args):
    """Instant undercroft inventory for a target domain."""
    d = DOMAIN_ALIASES.get(args.domain.lower(), args.domain.lower())
    if d not in DOMAIN_MAP:
        print(f"✗ domain {sorted(DOMAIN_MAP)} (aliases: {sorted(set(DOMAIN_ALIASES))})", file=sys.stderr)
        return 2
    print(f"▸ UNDERCROFT MAP — {d} ({len(DOMAIN_MAP[d])} seams)")
    for i, (cls, seam, where) in enumerate(DOMAIN_MAP[d], 1):
        print(f"  {i:2d}. [{cls:12s}] {seam}")
        print(f"      where: {where}")
        print(f"      plan:  undercroft probe --class {cls}")
    return 0


def cmd_descend(args):
    """The full loop in one command: scan → map → register → prioritized plan."""
    st = base(args.target)
    print(f"═══ UNDERCROFT DESCENT — {args.target} ═══")
    # 1. scan (if bundle path given)
    scan_n = 0
    if args.path:
        findings = _scan_findings(args.path)
        code = st.setdefault("code", [])
        known = {(c.get("asset"), c.get("seam")) for c in code}
        for x in findings:
            key = (f"{x['file']}:{x['line']}", x["seam"])
            if key not in known:
                code.append({"asset": key[0], "seam": x["seam"], "note": f"scan: {x['desc']}",
                             "at": datetime.now(timezone.utc).isoformat()})
        scan_n = len(findings)
        print(f"[1] scan: {scan_n} seam hits from {args.path}")
    # 2. domain map → register plan seams
    d = DOMAIN_ALIASES.get(args.domain.lower(), args.domain.lower())
    plan = []
    if d in DOMAIN_MAP:
        logic = st.setdefault("logic", [])
        known_logic = {(l.get("seam"), l.get("where")) for l in logic}
        for cls, seam, where in DOMAIN_MAP[d]:
            key = (seam, where)
            if key not in known_logic:
                logic.append({"seam": seam, "where": where, "status": "PROBED",
                              "proof": "", "delta": f"plan:{cls}",
                              "at": datetime.now(timezone.utc).isoformat()})
            plan.append((cls, seam, where))
        print(f"[2] map: {d} — {len(plan)} seams registered as PROBED")
    save(args.target, st)
    # 3. prioritized plan with probe plans inline
    value = {"precision": 3, "concurrency": 3, "boundary": 3, "entitlement": 3,
             "arbitrage": 3, "credits": 2, "webhook": 3, "state": 3, "randomness": 2,
             "conversion": 2, "journal": 2, "riskless": 2, "bounds": 2, "calculation": 3, "time": 2}
    ordered = sorted(plan, key=lambda x: -value.get(x[0], 1))
    print(f"[3] DESCENT PLAN (no-gain, one decisive test each):")
    for i, (cls, seam, where) in enumerate(ordered, 1):
        title, steps = PROBES[cls]
        print(f"\n  {i}. {seam}  [{cls}]  @ {where}")
        for k, v in steps:
            print(f"      {k:13s} {v}")
    print(f"\n═══ run each probe → confirm via logic/craft → export → 3AM promote ═══")
    return 0


# ── v2.3.0 braindead mode: the auto-engagement ────────────────────────────────

def _live_get(url, headers=None, timeout=5):
    """GET-only live probe. Returns (status, body_bytes) — read-only by construction."""
    import urllib.error
    import urllib.request
    req = urllib.request.Request(url, method="GET", headers=headers or
                                 {"User-Agent": "undercroft/2.3"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception:
        return None, b""


def cmd_jwt(args):
    """JWT inspector: decode (no verification), flag weak alg/admin claims/expiry."""
    import base64
    import json as _json
    tok = args.token.strip()
    parts = tok.split(".")
    if len(parts) != 3:
        print("✗ not a JWT (need 3 dot-separated parts)", file=sys.stderr)
        return 2
    def b64d(s):
        return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    try:
        header = _json.loads(b64d(parts[0]))
        payload = _json.loads(b64d(parts[1]))
    except Exception as e:
        print(f"✗ decode failed: {e}", file=sys.stderr)
        return 2
    print(f"▸ JWT header: {header}")
    print(f"▸ JWT payload ({len(payload)} claims):")
    for k, v in payload.items():
        print(f"    {k}: {v}")
    alg = str(header.get("alg", "?"))
    if alg.lower() == "none":
        print("  ! alg=none — unsigned token accepted by the target?")
    elif alg.startswith("HS"):
        print(f"  ! {alg} — symmetric MAC: forgeable if the secret leaks")
    for k, v in payload.items():
        if k.lower() in ("role", "admin", "is_admin", "scope") and str(v).lower() not in ("user", "false", "0"):
            print(f"  ! privileged claim: {k}={v}")
    if "exp" in payload:
        import datetime as _dt
        exp = _dt.datetime.fromtimestamp(payload["exp"], tz=_dt.timezone.utc)
        stale = exp < _dt.datetime.now(_dt.timezone.utc)
        print(f"  exp: {exp.isoformat()}" + ("  ! EXPIRED" if stale else " (valid)"))
    return 0


def cmd_run(args):
    """BRAINDEAD MODE: the whole engagement against a live target, read-only.
    scan → map → live route probe (GET) → boundary probe → auto-craft → report."""
    import hashlib
    import time as _time
    st = base(args.target)
    print(f"═══ UNDERCROFT RUN — {args.target} ({args.domain}) ═══")
    # [1] descend core: scan + map + register (reuse v2.2 pieces)
    if args.bundle:
        findings = _scan_findings(args.bundle)
        code = st.setdefault("code", [])
        known = {(c.get("asset"), c.get("seam")) for c in code}
        for x in findings:
            key = (f"{x['file']}:{x['line']}", x["seam"])
            if key not in known:
                code.append({"asset": key[0], "seam": x["seam"], "note": f"scan: {x['desc']}",
                             "at": datetime.now(timezone.utc).isoformat()})
        print(f"[1] scan: {len(findings)} seam hits")
        for x in findings[:6]:
            print(f"      {x['seam']:10s} {x['file']}:{x['line']} {x['desc']}")
        # jwt inspection for any token found
        import re as _re
        for m in _re.finditer(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]*",
                              " ".join(x["match"] for x in findings)):
            print(f"      jwt → decode:")
            args.token = m.group(0)
            cmd_jwt(args)
    d = DOMAIN_ALIASES.get(str(args.domain).lower(), str(args.domain).lower())
    plan = DOMAIN_MAP.get(d, [])
    logic = st.setdefault("logic", [])
    known_logic = {(str(l.get("seam") or ""), str(l.get("where") or "")) for l in logic}
    for cls, seam, where in plan:
        if (seam, where) not in known_logic:
            logic.append({"seam": seam, "where": where, "status": "PROBED",
                          "proof": "", "delta": f"plan:{cls}",
                          "at": datetime.now(timezone.utc).isoformat()})
    print(f"[2] map: {d} — {len(plan)} seams registered")
    # [3] live route probe (GET-only, polite pacing)
    live_hits = []
    if args.url:
        base_url = args.url.rstrip("/")
        hdrs = {"User-Agent": "undercroft/2.3"}
        if args.cookie:
            hdrs["Cookie"] = args.cookie
        for h in args.header or []:
            k, _, v = h.partition(":")
            hdrs[k.strip()] = v.strip()
        cands = [f"{base_url}/{w}" for w in ROUTE_WORDS] + \
                [f"{base_url}/api/{w}" for w in ROUTE_WORDS]
        cands = cands[:args.max_routes]
        print(f"[3] live route probe: {len(cands)} GET candidates (0.2s pacing)")
        burst = 0
        for c in cands:
            code_, body = _live_get(c, hdrs)
            burst += 1
            if burst % 25 == 0:
                _time.sleep(1)  # noise-budget pause per burst
            else:
                _time.sleep(0.2)
            if code_ in (200, 301, 403):
                live_hits.append((c, code_, len(body)))
                print(f"    LIVE {code_}  {c}  ({len(body)}B)")
        surface = st.setdefault("surface", [])
        known_s = {s.get("endpoint") for s in surface}
        for c, code_, size in live_hits:
            if c not in known_s:
                surface.append({"endpoint": c, "kind": "hidden", "status": "CONFIRMED",
                                "proof": f"live GET {code_} ({size}B)", "at": datetime.now(timezone.utc).isoformat()})
        print(f"    → {len(live_hits)} live route(s) CONFIRMED into surface ledger")
        # [4] boundary probe (read-only id swap on operator-supplied own ids)
        if args.boundary_url and args.probe_ids:
            print(f"[4] boundary probe: {args.boundary_url} ids={args.probe_ids}")
            for pid in args.probe_ids.split(","):
                u = args.boundary_url.replace("{id}", pid.strip())
                code_, body = _live_get(u, hdrs)
                ok = code_ == 200
                print(f"    id={pid.strip()}: {code_}" + ("  ← ACCEPTED" if ok else ""))
                if ok:
                    logic.append({"seam": f"boundary read (id={pid.strip()})",
                                  "where": args.boundary_url, "status": "CONFIRMED",
                                  "proof": f"GET {u} → 200 ({len(body)}B)",
                                  "delta": "read-only id swap",
                                  "at": datetime.now(timezone.utc).isoformat()})
    save(args.target, st)
    # [5] auto-craft CONFIRMED seams → PoC ledger
    pocs = st.setdefault("pocs", [])
    known_p = {p.get("finding") for p in pocs}
    crafted = 0
    seam_class = {"boundary": "IDOR", "concurrency": "RACE", "webhook": "STATE",
                  "state": "STATE", "precision": "MATH", "conversion": "MATH",
                  "time": "TIME", "journal": "OTHER", "entitlement": "IDOR"}
    for l in logic:
        if l.get("status") == "CONFIRMED" and l.get("seam") not in known_p:
            cls = seam_class.get(l.get("seam", "").split()[0], "OTHER")
            pocs.append({"finding": l["seam"], "request": f"GET/verify {l.get('where', '')}",
                         "proof": l.get("proof", ""), "class": cls,
                         "at": datetime.now(timezone.utc).isoformat()})
            crafted += 1
    save(args.target, st)
    print(f"[5] auto-craft: {crafted} CONFIRMED finding(s) → PoC ledger")
    # [6] report
    rep = Path(f"{args.target}-undercroft-report.md")
    args.output = str(rep)
    cmd_report(args)
    print(f"[6] report: {rep}")
    print("═══ next: undercroft export --target " + args.target + "  →  3AM promote ═══")
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
    sc = sub.add_parser("scan", help="static seam scanner: bundles/source → seams (read-only)")
    sc.add_argument("--path", required=True, help="file or dir of client bundles/source")
    sc.add_argument("--target", help="register findings into campaign code ledger")
    sc.add_argument("--limit", type=int, default=4, help="examples per seam class")
    sf = sub.add_parser("stateflow", help="out-of-order transition bypass matrix")
    sf.add_argument("--states", required=True, help="comma list in canonical order")
    sf.add_argument("--guard", help="comma guards, format 'state:prerequisite'")
    sf.add_argument("--flow", help="flow name for the ledger")
    sf.add_argument("--target", help="register matrix into campaign logic ledger")
    rp = sub.add_parser("replay", help="idempotency/replay harness (same request N×)")
    rp.add_argument("--url", required=True)
    rp.add_argument("--method", default="GET")
    rp.add_argument("--header", action="append", help="'K: V', repeatable")
    rp.add_argument("--body", help="request body (json)")
    rp.add_argument("--times", type=int, default=5)
    rp.add_argument("--timeout", type=int, default=5)
    rp.add_argument("--confirm", action="store_true", help="required for state-changing methods")
    rp.add_argument("--target", help="auto-register idempotency gap")
    pc = sub.add_parser("precision", help="drift calculator: float vs decimal, worst crafted amount")
    pc.add_argument("--price", type=float, required=True)
    pc.add_argument("--rate", type=float, required=True)
    pc.add_argument("--ops", type=int, default=1000)
    pc.add_argument("--mode", choices=["floor", "trunc", "round"], default="round")
    en = sub.add_parser("entropy", help="token/OTP entropy estimator (observation-only)")
    en.add_argument("--samples", help="space-separated tokens")
    en.add_argument("--file", help="one token per line")
    co = sub.add_parser("corpus", help="boundary-input corpus generator")
    co.add_argument("--type", required=True, choices=["money", "int", "string", "json", "date"])
    mp = sub.add_parser("map", help="instant undercroft inventory for a target domain")
    mp.add_argument("--domain", required=True, help="e-commerce|fintech|saas|booking|social|gaming|infra (+ aliases)")
    de = sub.add_parser("descend", help="the full loop: scan → map → register → prioritized plan")
    de.add_argument("--target", required=True)
    de.add_argument("--domain", required=True)
    de.add_argument("--path", help="optional bundle/source path to scan")
    rn = sub.add_parser("run", help="BRAINDEAD MODE: full auto-engagement (read-only) → report")
    rn.add_argument("--target", required=True)
    rn.add_argument("--domain", required=True)
    rn.add_argument("--url", help="live target base URL (GET-only probing)")
    rn.add_argument("--bundle", help="optional bundle/source path to scan")
    rn.add_argument("--cookie", help="own session cookie 'k=v' for authenticated read probes")
    rn.add_argument("--header", action="append", help="'K: V', repeatable")
    rn.add_argument("--boundary-url", help="URL template with {id} for read-only boundary probe")
    rn.add_argument("--probe-ids", help="comma own-ids to swap into boundary-url")
    rn.add_argument("--max-routes", type=int, default=60)
    jt = sub.add_parser("jwt", help="JWT inspector: decode + weak-alg/claim/expiry flags")
    jt.add_argument("--token", required=True)
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
    if a.cmd == "scan":
        return cmd_scan(a)
    if a.cmd == "stateflow":
        return cmd_stateflow(a)
    if a.cmd == "replay":
        return cmd_replay(a)
    if a.cmd == "precision":
        return cmd_precision(a)
    if a.cmd == "entropy":
        return cmd_entropy(a)
    if a.cmd == "corpus":
        return cmd_corpus(a)
    if a.cmd == "map":
        return cmd_map(a)
    if a.cmd == "descend":
        return cmd_descend(a)
    if a.cmd == "run":
        return cmd_run(a)
    if a.cmd == "jwt":
        return cmd_jwt(a)
    if a.cmd == "report":
        return cmd_report(a)
    if a.cmd == "verify":
        return cmd_verify(a)
    return 2


if __name__ == "__main__":
    sys.exit(main())