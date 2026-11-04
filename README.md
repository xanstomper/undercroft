<div align="center">

```
   ██╗   ██╗███╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██████╗ ███████╗████████╗
   ██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
   ██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝██████╔╝██║  ██║█████╗     ██║
   ██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗██╔═══╝ ██║  ██║██╔══╝     ██║
   ╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║██║     ██████╔╝███████╗   ██║
    ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝     ╚═════╝ ╚══════╝   ╚═╝
```

# ⛏️ UNDERCROFT

### *Attack the hidden level beneath the documented surface.*

**The Descent of the HolyShit family** — every system has an undercroft: code only
its authors know, endpoints the docs never mention, rules that move value and
privilege in ways no scanner models. UNDERCROFT attacks it — by reading the target
itself and adapting documented technique classes to its specifics.

[![Version](https://img.shields.io/badge/version-2.3.0-blueviolet?style=for-the-badge)](#the-cli)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](#quickstart)
[![Platform](https://img.shields.io/badge/platform-Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](#quickstart)
[![Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen?style=for-the-badge)](#why-its-powerful)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![CI](https://github.com/xanstomper/undercroft/actions/workflows/verify.yml/badge.svg)](https://github.com/xanstomper/undercroft/actions/workflows/verify.yml)
[![Use](https://img.shields.io/badge/use-AUTHORIZED%20TARGETS%20ONLY-crimson?style=for-the-badge)](#the-walls-non-negotiable)

**THE FAMILY** — six siblings and the dispatcher, one click each:

[![00 BARBICAN · the shield](https://img.shields.io/badge/00-BARBICAN%20·%20the%20shield-2E4057?style=for-the-badge)](https://github.com/xanstomper/barbican)
[![01 3AM · the performer](https://img.shields.io/badge/01-3AM%20·%20the%20performer-8B0000?style=for-the-badge)](https://github.com/xanstomper/3am-shinjitsu)
[![02 KAIRO · the synthesizer](https://img.shields.io/badge/02-KAIRO%20·%20the%20synthesizer-6B8E23?style=for-the-badge)](https://github.com/xanstomper/kairo)
[![04 HOLYSHIT · the finder](https://img.shields.io/badge/04-HOLYSHIT%20·%20the%20finder-B8860B?style=for-the-badge)](https://github.com/xanstomper/HolyShit)
[![05 SHIKI · the command](https://img.shields.io/badge/05-SHIKI%20·%20the%20command-111111?style=for-the-badge)](https://github.com/xanstomper/shiki)
[![06 SHUKAKU · the harvester](https://img.shields.io/badge/06-SHUKAKU%20·%20the%20harvester-8B4513?style=for-the-badge)](https://github.com/xanstomper/shukaku)
[![SPYDERMONKEY · the dispatcher](https://img.shields.io/badge/🕷️-SPYDERMONKEY%20·%20the%20dispatcher-blueviolet?style=for-the-badge)](https://github.com/xanstomper/spydermonkey)

[How it works](#how-it-works) · [Why it's powerful](#why-its-powerful) ·
[Quickstart](#quickstart) · [The CLI](#the-cli) · [The Walls](#the-walls-non-negotiable)

</div>

---

## What is this?

The family's three attackers do NOT overlap:

- **HolyShit** attacks what is KNOWN — proven recipes, case lore, discovery canon.
- **3AM** attacks what is KNOWABLE — universal vectors, swept fast, automated.
- **UNDERCROFT** attacks what is UNKNOWN — the target's own skin. No public PoC
  exists for the target's custom rules; the attack is forged by reading the target.

```
✓ UNDERCROFT verify: compile · subcommands · template — ALL PASS
```

Where 3AM's verdict is BLOCKED on a known-vector wall, UNDERCROFT walks around the
wall. Slower than the sweep by design, deeper by requirement.

## How it works

### The six disciplines

1. **CUSTOM-CODE** — source/bundle review: authn/authz flows, crypto misuse,
   unsafe reflection, injection seams, trust-boundary crossings
2. **SHADOW-SURFACE** — undocumented endpoints: route fuzzing, verb misuse,
   legacy versions, admin internals leaking through bundles
3. **PROTOCOL** — proprietary formats/encodings/state machines, Δ documented per input
4. **RULES & VALUE FLOWS** — the universal discipline: billing/refunds, quotas,
   wallets/coupons/trials, booking concurrency, workflow state machines, tenant
   boundaries, conversion math, ledger integrity, idempotency/replay guards
5. **CRAFTED-POC** — the forge: every finding becomes a decisive test the family
   can re-run — one request, one proof, Δ documented
6. **RANDOMNESS & ENTROPY** — RNG structures, matchmaking bias, OTP/token entropy,
   seed-timing correlation

### The descent kit — six real tools

```bash
undercroft scan --path ./client-bundle            # static seam scanner, 12 pattern classes
undercroft stateflow --states "a,b,c,d" --guard "b:a"   # out-of-order transition bypass matrix
undercroft replay --url U --method POST --times 5 # idempotency harness (state-changing: --confirm)
undercroft precision --price 19.99 --rate 1.1 --ops 1000 # exact-vs-float drift calculator
undercroft entropy --samples "..."                # token/OTP entropy estimator
undercroft corpus --type money                    # canonical boundary-input corpus
```

### Braindead mode — one command, the whole engagement

```bash
undercroft run --target shop --domain e-commerce \
  --url https://target.example --bundle ./client-bundle \
  --boundary-url "https://target.example/api/orders?org_id={id}" --probe-ids "1,2"
```

`run` executes the ENTIRE engagement, read-only by construction: bundle scan +
JWT decode → domain map → 60+ live GET route probes at disciplined pacing →
boundary id-swaps on the operator's own ids → **auto-craft** every CONFIRMED
finding into the PoC ledger → report written, next step printed. State-changing
probes still require explicit separate `--confirm` — braindead does not mean ungated.

### The closed loop — it arms the family

```
probe (15 seam plans) → fuzz → code/surface/logic seams → craft (PoC ledger)
→ export → 3AM learned-vectors.jsonl → 3AM promote --apply --verified
→ the sweep grows → the next campaign hits it too
```

`export` maps every crafted PoC onto 3AM's exact `(flaw, seam)` schema — one
command closes the family loop.

## Why it's powerful

- **It attacks what scanners can't.** Value/privilege rules are invisible to CVE
  matching — UNDERCROFT reads the target's own logic and forges the input.
- **15 NO-GAIN probe plans, in the box.** `probe` prints the full engine — the
  exact Δ, probe shape, verify condition, and reversibility cost per seam class:

```
━━ precision — Value :: rounding/precision
  Δ             amounts at max precision + unit conversion (currency, %, units)
  probe         submit crafted amount × N repetitions on own account
  verify        reconciled result drifts ≥ 1 smallest unit after N ops
  cost          N × smallest unit, fully reversible (refund each op)
  confirmed_when balance/statement ≠ naive sum; drift recorded
```

- **The proof is the finding, never the prize.** Minimal, reversible, NO-GAIN
  crafted transactions — nothing of value is ever kept.
- **Negatives are results.** A seam probed clean is EXHAUSTED with its exact test,
  never re-fired without a change.
- **The loop compounds.** Every CONFIRMED craft becomes a family vector — 3AM's
  matrix grows, and the next engagement starts smarter.
- **Zero dependencies.** Pure Python stdlib. Clone and run.

## Quickstart

```bash
git clone https://github.com/xanstomper/undercroft.git
python3 undercroft/scripts/undercroft.py verify     # → ALL PASS
python3 undercroft/scripts/undercroft.py probe      # the full NO-GAIN probe-plan engine
python3 undercroft/scripts/undercroft.py map --domain fintech   # instant seam inventory
python3 undercroft/scripts/undercroft.py descend --target t --domain e-commerce
```

## The CLI

| Command | What it does |
|---|---|
| `run --target C --domain D --url URL [--bundle P] [--boundary-url U] [--probe-ids 1,2]` | **braindead mode** — the entire read-only engagement, auto-crafted |
| `descend --target C --domain D [--path bundles]` | the press-button loop: scan → map → prioritized plan |
| `code / surface / logic` | the three seam ledgers (custom-code, shadow-surface, rules) |
| `probe [--class K]` | 15 NO-GAIN probe plans |
| `fuzz / scan / jwt / stateflow / replay / precision / entropy / corpus` | the descent kit |
| `craft --target C --add ID --request R --proof P --class K` | PoC ledger — feeds the family |
| `export --target C` | forge → 3AM: `(flaw, seam, probe, confirmed_when)` JSONL rows |
| `drift / prioritize / report` | stale re-verify flags, attack order, the report |
| `verify` | self-check |

## The Walls (non-negotiable)

Documented-PoC adaptation only — novel weapon classes are never authored ·
validation-only + NO-GAIN · never social, never destructive, no persistence ·
zero documents · read-only by construction, state-changing probes gated by
`--confirm` — family canon at every layer.

## Files

```
undercroft/
├── SKILL.md                        # the doctrine
├── scripts/
│   └── undercroft.py               # the full descent CLI (1,000+ lines, stdlib)
├── references/
│   └── undercroft-playbook.md      # per-discipline decisive-test batteries + domain map
└── templates/
    └── undercroft-state.json       # per-target state starter
```

## Relations

`spydermonkey` dispatches it · `barbican` gates it · `shiki` conducts it (the
descent is assault step 2) · `holyshit-mode` feeds the map · `3am-shinjitsu` hands
it BLOCKED walls and absorbs its vectors · `kairo` compiles its seams for everyone ·
`shukaku` prices what its confirmations make reachable.

## License

[MIT](LICENSE) — descend with it, build for it, route through it.

<div align="center">

*The proof is the finding. Never the prize.*

</div>
