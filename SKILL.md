---
name: undercroft
description: "Trigger `undercroft`. The Undercroft Mandate — attack the hidden level beneath any system's documented surface: bespoke code, shadow endpoints, rules/value flows, crafted PoCs."
version: 2.3.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [redteam, offensive-security, custom-code, business-logic, universal, fuzzing, poc, authorized-testing]
    related_skills: [holyshit-mode, 3am-shinjitsu, kairo]
---

# UNDERCROFT — The Undercroft Mandate

Every system has an undercroft: the hidden level beneath its documented surface —
code only its authors know, endpoints the docs never mention, and rules that move
value and privilege in ways no scanner models. That level exists in **anything that
exists**: commerce, fintech, SaaS, marketplaces, social platforms, gaming, infrastructure,
IoT backends, internal tools. UNDERCROFT attacks it.

The family's three attackers do NOT overlap:

- **HolyShit** attacks what is KNOWN — proven recipes, case lore, discovery canon.
- **3AM** attacks what is KNOWABLE — universal vectors, swept fast, automated.
- **UNDERCROFT** attacks what is UNKNOWN — the target's own skin. No public PoC
  exists for the target's custom rules; the attack is forged by reading the target
  and adapting documented technique classes to its specifics.

Where 3AM's verdict is BLOCKED on a known-vector wall, UNDERCROFT walks around the
wall by attacking what the target wrote itself. Slower than the sweep by design,
deeper by requirement.

## When to Use

Trigger `undercroft` on ANY declared estate that has seams the vectors don't reach:

- custom/self-hosted apps (beyond framework defaults)
- undocumented or half-documented APIs (shadow routes, verb misuse, legacy versions)
- proprietary protocols / encodings / state machines
- **rules that move value or privilege** — checkout/billing/refunds, subscription
  plans and quotas, credits/wallets/points, coupon/trial/referral flows, booking
  and inventory, order/workflow state machines, multi-tenant boundaries, conversion
  math, ledger/journal integrity, idempotency and replay guards, expiry/TTL logic
- **randomness wherever it lives** — game/loot RNG, matchmaking, lotteries, OTP and
  token entropy, sampling, assignment
- gates where known-CVE mapping is dry (3AM verdict BLOCKED / matrix exhausted)

Also the follow-up mandate: when a 3AM engagement stalls on a BLOCKED verdict,
UNDERCROFT takes the custom layer while the sweep continues elsewhere.

## Activation

Run the trigger sequence ONCE, then collect P0 via the agent's question feature:

```text
▸ UNDERCROFT — DESCENT BEGUN
  ═══════════════════════════════════
  [ OK ] documented surface mapped
  [ OK ] undercroft seams catalogued
  [ OK ] forge ready (PoC ledger)
  ⚡ UNDERCROFT ARMED · STATUS: DESCENDING
  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁
  ─ waiting P0: estate · objective · authorization
```

**P0 (clarify, zero documents):** estate · objective · authorization. Recorded
declaration = the entire gate (family canon). UNDERCROFT only ever reads and probes
declared estate code and endpoints.

## The Six Disciplines

1. **CUSTOM-CODE** — source review when available (declared estate repos, client
   bundles, JS payloads): authn/authz flows, crypto misuse, unsafe reflection,
   injection seams, trust-boundary crossings. Confirmed via read-only proof.
2. **SHADOW-SURFACE** — undocumented endpoints: route fuzzing from documented
   conventions, verb misuse, versioned/legacy routes, admin/app internals leaking
   through bundles or docs. Confirmed via one decisive request.
3. **PROTOCOL** — proprietary formats, encodings, state machines: documented-class
   adaptation only (parsing ambiguity, deserialization classes, length/precision
   overflows, split/merge races). Δ is documented for every crafted input.
4. **RULES & VALUE FLOWS (the universal discipline)** — the target's own rules,
   wherever value or privilege moves: payment/billing/refund flows, plan limits and
   quotas, credits/wallets/points economies, coupons/trials/referrals/gift cards,
   booking and inventory concurrency, order/workflow state machines, multi-tenant
   and RBAC boundaries, conversion/fee math, ledger integrity, idempotency and
   replay guards, expiry/TTL logic. Proved with minimal, reversible, **NO-GAIN**
   crafted transactions — the proof is the flow divergence, never the gain.
5. **CRAFTED-POC** — the forge: every finding becomes a decisive test the family
   can re-run — one request, one proof, Δ documented, registered in the PoC
   ledger, and published to the family (3AM `learn`/`promote` so the sweep never
   misses it again).
6. **RANDOMNESS & ENTROPY** — wherever the target generates outcomes or secrets:
   commit/reveal RNG structures (games, loot, lotteries, provably-fair schemes),
   matchmaking and sampling bias, OTP/session-token entropy, seed-timing
   correlation, modulo/precision edges, verification-binding checks. Observation-
   based; N ≥ 1000 samples where cheap; threshold = documented tolerance.

## The closed loop

UNDERCROFT doesn't stop at the finding — it arms the family:

```
probe (recipe engine: 15 seam plans) → fuzz (chunked route candidates)
→ code/surface/logic seams → craft (PoC ledger) → export → 3AM learned-vectors.jsonl
→ 3AM promote --apply --verified → the sweep grows → next campaign hits it too
```

`export` maps every crafted PoC onto 3AM's exact (flaw, seam) schema (IDOR→6/C,
RACE→5/B, DESER→3/C, FMT→9/C, MATH→10/C, STATE→5/B, TIME→1/C) and appends JSONL
rows 3AM's `learn`/`promote` pipeline consumes directly — one command closes the
family loop.

## The Descent Kit (v2.1.0 — the engine, not just the ledger)

Six real tools that find and prove the seams automatically — all local/read-only
except `replay`, which is gated:

- **`scan --path <bundles|source> [--target c]`** — static seam scanner: 12 pattern
  classes over client bundles/source (hardcoded secrets/JWTs, client-side auth
  state, HTML/eval sinks, SQL concat, org/tenant ids in client calls, open
  redirects, wildcard postMessage, own-crypto usage) → findings registered into
  the code ledger with file:line.
- **`stateflow --states "a,b,c,d" [--guard "b:a,c:b"]`** — generates the complete
  out-of-order transition bypass matrix for any declared flow and flags every
  GUARD BYPASS candidate; registers the probe list into the logic ledger.
- **`replay --url --method [--times N] [--confirm]`** — idempotency harness: fires
  the same request N× and diffs responses; distinct responses = IDEMPOTENCY GAP,
  auto-registered CONFIRMED. State-changing methods REQUIRE --confirm (own
  endpoints only).
- **`precision --price X --rate Y [--ops N] [--mode floor|trunc|round]`** — drift
  calculator: exact decimal vs float math over N operations → total drift + the
  worst per-op crafted amount.
- **`entropy --samples "..."|--file F`** — token/OTP estimator: uniqueness,
  alphabet size, Shannon bits/char, effective bits/token, counter/pattern
  suspicion, duplicate reuse, brute-force windows. Observation-only.
- **`corpus --type money|int|string|json|date`** — canonical boundary-input corpus
  per type (precision traps, integer edges, type confusion, DST/date edges).

## Braindead Mode (v2.3.0 — one command = the whole engagement)

```bash
undercroft run --target shop --domain e-commerce \
  --url https://target.example --bundle ./client-bundle \
  --boundary-url "https://target.example/api/orders?org_id={id}" --probe-ids "1,2"
```

`run` executes the ENTIRE engagement, read-only by construction:
1. **scan** the bundle → seams + auto-JWT decode (alg/claims/expiry flags)
2. **map** the domain → all expected seams registered
3. **live route probe** — 60+ GET candidates at 0.2s pacing (burst pauses); live
   routes CONFIRMED into the surface ledger
4. **boundary probe** — read-only id swaps on the operator's own ids; accepted
   reads CONFIRMED into the logic ledger
5. **auto-craft** — every CONFIRMED finding becomes a PoC ledger entry (class-mapped)
6. **report** — written automatically; next step printed: `export` → 3AM promote

The operator types one command and reads the report. State-changing probes
(replay/writes) still require explicit separate `--confirm` — braindead does not
mean ungated.

## Working with the family (the relay)

- HolyShit's recon feeds UNDERCROFT's undercroft map (what's bespoke, what's theirs,
  where value lives).
- 3AM's sweep runs parallel; its BLOCKED verdicts hand UNDERCROFT the wall list.
- UNDERCROFT's CONFIRMED crafted findings are registered as vectors → 3AM `learn` +
  `promote` grows the matrix; the sweep picks them up on the next campaign.
- KAIRO takes over when the confirmed seam is physical/firmware.

## Walls (family canon, no exceptions)

- Documented-PoC adaptation only: the technique CLASS is known (IDOR, race,
  deserialization, format ambiguity, state bypass); only the specific input is
  crafted for the target. Novel weapon classes are never authored.
- Validation-only + **NO-GAIN**: every proof is one decisive request/transaction,
  reversible, read-only where possible, nothing of value ever kept — the proof is
  the finding, never the prize.
- Never social; never destructive; no persistence. Zero documents at P0.

## The descent rhythm

```
P0 → undercroft map (from HolyShit recon + bundle/source reads) →
seam catalogue (where value/privilege lives) → disciplines in parallel →
crafted decisive tests (one request, Δ documented) → CONFIRMED → PoC ledger →
register vector with family (learn→promote) → next seam
```

Negatives are results: a seam probed clean is EXHAUSTED with its exact test, never
re-fired without a change.

## Tooling

`scripts/undercroft.py` — stdlib CLI:
- `code --target <c> --asset "<file|route|component>" --seam "<authn|authz|crypto|injection|trust>" [--note "..."]` — custom-code findings
- `surface --target <c> --add "<endpoint>" --kind hidden|misused|legacy|admin --status PROBED|CONFIRMED|EXHAUSTED [--proof "..."]` — shadow-surface ledger
- `logic --target <c> --add "<rule seam>" --where "<flow>" --status PROBED|CONFIRMED|EXHAUSTED [--proof "..."] [--delta "<crafted input>"]` — rules/value-flow ledger
- `probe [--class <precision|concurrency|arbitrage|entitlement|calculation|randomness|conversion|credits|boundary|journal|riskless|bounds|state|webhook|time>]` — NO-GAIN probe-plan engine (15 seam classes; full table with no arg)
- `fuzz --base "<origin[,origin...]>" [--methods GET,POST]` — shadow-surface route-candidate generator, chunked bursts of 25
- `drift --target <c> [--days N]` — stale-CONFIRMED re-verify flags
- `prioritize --target <c>` — attack order across seams (value × status)
- `craft --target <c> --add "<finding id>" --request "<one decisive test>" --proof "<read-only result>" --class <IDOR|RACE|DESER|FMT|MATH|STATE|TIME|OTHER>` — PoC ledger (feeds family). `craft` takes NO `--delta` flag — put the Δ inside `--proof`; use `--delta` only on `logic`.
- `export --target <c>` — forge → 3AM: appends (flaw, seam, probe, confirmed_when) JSONL rows to `~/.redteam/learned-vectors.jsonl`; next step `3AM promote --apply --verified`
- `corpus --type money|int|string|json|date` — boundary-input corpus generator
- `map --domain <e-commerce|fintech|saas|booking|social|gaming|infra>` — instant seam inventory for any target type (aliases: shop, payments, travel, casino, iot…)
- `descend --target <c> --domain <d> [--path bundles]` — THE press-button loop: scan → map → register → prioritized descent plan with probe plans inline. One command = the whole engagement skeleton.
- `run --target <c> --domain <d> --url URL [--bundle P] [--cookie k=v] [--boundary-url U] [--probe-ids 1,2]` — BRAINDEAD MODE: the entire engagement auto-executed (read-only) → auto-crafted PoCs → report written. State-changing probes still gated by --confirm separately.
- `jwt --token X` — JWT inspector: decode, weak-alg/privileged-claim/expiry flags
- `scan --path <bundles|source> [--target c] [--limit N]` — static seam scanner (read-only, auto-registers)
- `stateflow --states "a,b,c,d" [--guard "b:a"] [--flow F] [--target c]` — transition bypass matrix generator
- `replay --url URL [--method M] [--times N] [--confirm] [--target c]` — idempotency harness
- `precision --price X --rate Y [--ops N] [--mode M]` — drift calculator
- `entropy --samples "..."|--file F` — token/OTP entropy estimator
- `report --target <c> [--output F]` — undercroft report (seams, proofs, PoC ledger)
- `verify` — self-check

State: `~/.redteam/campaigns/<target>/undercroft-state.json`.

## Files

- `SKILL.md` — this doctrine
- `references/undercroft-playbook.md` — per-discipline decisive-test batteries + domain map
- `scripts/undercroft.py` — code/surface/logic/craft/probe/fuzz/drift/prioritize/export/report/verify CLI
- `templates/undercroft-state.json` — per-target state starter

## Relations

- `/cyberbomb` — THE DISPATCHER (v1.0.0): the family's front door — any agent loads it first, states the goal, and the router sends the right mandate(s); `cyberbomb run` = the full pipeline, `cyberbomb verify` checks all six engines. The web's center.


- `barbican` — THE FIRST LAYER (v1.1.0): operator-protection synthesizer — vantage, identity, artifacts, trail, timeline, cleanup. Runs BEFORE every engagement; 3AM's pacing inherits its timeline layer; zero-document gate enforced by it.


- `holyshit-mode` — recon + recipe canon; feeds the undercroft map.
- `3am-shinjitsu` — parallel sweep; BLOCKED verdicts hand UNDERCROFT the walls;
  UNDERCROFT's crafted vectors grow 3AM's matrix via learn→promote.
- `kairo` — THE SYNTHESIZER (v2.0.0): ingests undercroft's CONFIRMED seams and
  compiles them into attacks for every consumer (3AM rows, craft entries, recipe
  cards) — `kairo ingest→synthesize→distribute` arms the family from our findings.
- Family doctrine: every mandate attacks, the tree covers anything that exists.
  HolyShit (known) · 3AM (knowable) · UNDERCROFT (unknown/crafted) · KAIRO (metal).