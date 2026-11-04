# UNDERCROFT — Playbook (per-discipline decisive tests, universal scope)

The undercroft exists in every system: the seams between what's documented and
what's actually there. Every probe: ONE decisive request, Δ documented (what was
crafted vs the documented class), read-only or reversible, **NO-GAIN** on any seam
that moves value. Ledger negatives with the exact test. CONFIRMED findings enter
the PoC ledger and the family's vector registry.

## D1 — CUSTOM-CODE

| Seam | How to read it | Confirmed-when |
|---|---|---|
| authn bypass | session construction, token verify order, admin flags in payloads | one unprivileged request authenticated as privileged |
| authz | route guards, tenant filters, org-id in body/params | one cross-tenant/cross-role read 200 |
| crypto | own crypto, key reuse, ECB/malleable modes, magic bytes in JWT alg | one forged/decoded proof read |
| injection | raw concat into query/exec/template (runtime-expanded) | one harmless probe reflected/executed (read-only) |
| trust boundary | client-validated totals, server-trusted fields in hidden inputs | one altered field accepted |

Source reads: declared repos, client bundles, JS payloads — always on-estate assets.

## D2 — SHADOW-SURFACE

| Probe | Test | Confirmed-when |
|---|---|---|
| route fuzz | documented conventions + wordlist on declared origin (chunked) | undocumented route answers |
| verb misuse | OPTIONS/PUT/PATCH/DELETE on documented routes | unexpected handler branch |
| legacy/versioned | /v1 /v2, /admin, /internal from bundle strings + CT history | legacy route live |
| method-of-admin | bundle/admin docs revealing internal call shapes | internal endpoint reachable |
| debug telemetry | /metrics /health /debug /actuator-class endpoints | info-leak/exec surface |

One request per candidate; bulk fuzz chunked within family noise budgets.

## D3 — PROTOCOL

| Class (documented) | Crafted input (Δ) | Confirmed-when |
|---|---|---|
| parsing ambiguity | double-encoded/overlapping tokens in declared formats | server consumes two meanings |
| deserialization class | type-confused field in declared schema | unexpected object/error path |
| length/precision | boundary ints, negative/NaN, max-precision floats | divergent handling |
| split/merge race | concurrent chunked submits on the same logical unit | duplicate/desync accepted |
| state machine | out-of-order transitions on declared flows | illegal-but-accepted state |

Δ must state the class + the modification. Never craft for unknown parser internals
beyond observed behavior (black-box adaptation stays within documented classes).

## D4 — RULES & VALUE FLOWS (the universal discipline)

Every rule seam ships with a NO-GAIN probe plan from the engine
(`undercroft probe --class <seam>`): 15 seam classes — precision, concurrency,
arbitrage, entitlement, calculation, randomness, conversion, credits, boundary,
journal, riskless, bounds, state, webhook, time. Each plan fixes Δ, the minimal
probe, the verify, the cost (reversible), and confirmed-when.

**Where these seams live (domain map — the same seams, any system):**

| Domain | Typical undercroft seams |
|---|---|
| e-commerce / marketplaces | cart/checkout state races, refund math, price/quote arbitrage, coupon stacking, inventory decrement races, seller payout calc |
| fintech / payments / crypto | conversion/fee asymmetry, ledger drift, idempotency-key replay, double-spend concurrency, withdrawal bounds, rounding direction at scale |
| SaaS / subscriptions | plan-limit bypass, seat/entitlement inflation, trial/TTL logic, proration math, quota reset seams, feature-gate trust in client |
| booking / logistics / travel | double-book concurrency, cancellation/void counting, timezone/DST edges, overbooking bounds, state-machine bypass on orders |
| social / platforms | rate/credit economies, referral loops, moderation-workflow state bypass, cross-tenant reads (org/workspace id in body) |
| gaming / gambling | RNG structure (provably-fair or not), loot/odds math, bonus flows, currency conversion, balance races |
| infra / IoT backends | device-claim entitlement, command replay (webhooks/queues), OTA/update state machines, telemetry journal integrity |

NO-GAIN: probe minimally, reverse every transaction, record refunds — nothing of
value is ever kept. The proof is the flow divergence, never the gain.

| Seam | Probe (minimal, reversible, NO-GAIN) | Confirmed-when |
|---|---|---|
| precision/rounding | max-precision + unit-conversion edges on crafted amounts | reconciled result ≠ naive sum; drift recorded |
| concurrency | N parallel submits of the same logical unit (own account) | duplicate applied / negative state |
| arbitrage | two correlated values priced inconsistently; minimal opposing actions | riskless-gain window exists |
| entitlement | flow-order inversion / parallel claim on promo-trial-referral flows | duplicate or unearned grant accepted |
| calculation | crafted inputs outside documented bounds through the calc | result overpays/diverges from independent math |
| randomness | N observed outcomes; check structure + distribution | bias/reuse/predictable window ≥ tolerance |
| conversion | round-trip conversions at boundary amounts (fees + rounding direction) | nonzero drift / fee asymmetry |
| credits | earn/burn inversion or account-merge arithmetic (own accounts) | value created from nothing |
| boundary | org/plan/tenant id switch in scoped requests | foreign resource 200 |
| journal | statement vs journal divergence; voided/cancelled op counting | reconciliation gap (read-only) |
| riskless | spendability scope of demo/trial/free credits | credit accepted where terms forbid |
| bounds | max+1 / negative / fractional inputs through validation | out-of-bounds accepted |
| state | out-of-order transitions on order/workflow/approval flows | illegal-but-accepted state |
| webhook | replay a captured callback with same dedup key (own endpoint) | duplicate effect / missing idempotency |
| time | expiry/grace/TTL edges: renew before/after boundary, clock skew | expired-but-accepted / pre-expiry grant |

## D5 — CRAFTED-PoC (the forge)

Every finding ships as: `class · request (one line) · proof (one line) · Δ · impact`.
Register in `undercroft state` (craft) and hand to 3AM: `learn` the vector, `promote`
into the living matrix when verified. The family only gets faster campaign-over-
campaign; UNDERCROFT is the vector forge that feeds it.

## D6 — RANDOMNESS & ENTROPY (universal)

Wherever the target generates outcomes or secrets. Observation-based on declared
estate flows; sampling on the operator's own accounts; threshold = documented
tolerance, never noise.

| Seam | Analysis (observation) | Confirmed-when |
|---|---|---|
| commit-reveal RNG | seed/nonce structure: what is revealed, when, by whom (games/lotteries/provably-fair) | nonce reuse or predictable seed window |
| distribution bias | skew on N ≥ 1000 observed outcomes vs documented expectation | divergence beyond documented tolerance |
| seed-timing | correlation between seed selection and server event stream | seed-timing dependency |
| modulo/precision | RNG loop boundaries: drift, modulo bias, precision edges | measurable bias on crafted input |
| verification binding | any player-verifiable check actually binds the server-side value | server value unconstrained by the check |
| token/OTP entropy | generation structure of OTPs/tokens (alphabet, TTL, rate, retry) | reduced entropy / predictable window / replay |

### Worked domain example — auditing shipped odds math from client bundles (casino RTP audit)

1. Extract game-config regions from the verifier/game chunks: search for
   `fairValueProduces|roundMultiplier|weights|slug:"` and pull ±12KB context.
2. Reconstruct the fair multiplier per outcome: `fair = 1/P(outcome)` where P comes
   from the shipped `weights` table (weights summing to 100 are percentages).
3. Verify every ladder rung against `rung(f) = edge × fair^floor` — a consistent
   constant across ALL difficulties/floors means the math is sound; a rung
   off-formula, or an inverted derivation for one mode, is the finding.
4. Check rounding direction on every printed value: flooring in the USER's favor
   at scale is a margin finding even when the formula is right.
5. If outcome derivation never ships client-side (server-only math), say so — the
   audit ends EXHAUSTED, not INCONCLUSIVE; the remaining test needs an account +
   browser vantage and is a parked decisive test, not a hole in the sweep.

The same method transfers to ANY shipped-math audit: pricing ladders, fee tables,
scoring formulas, rank/elo curves — reconstruct, verify against formula, check
rounding direction, park what needs a live vantage.

## Worked recipes (universal, step-by-step)

### R1 — Webhook replay → duplicate effect (payments/integrations)

1. Trigger ONE legitimate event on your own account (e.g. a test payment/callback).
2. Capture the outbound callback the platform sent your endpoint (request log,
   webhook debugger, or your own receiver log): full method+headers+body.
3. `undercroft replay --url <your-endpoint> --method POST --header "X-Sig: <as captured>" --body '<captured>' --times 3 --confirm`
4. Check: one effect or N? (order created once vs N; ledger entry duplicated).
5. CONFIRMED when the platform's own dedup key fails to gate the replay. Reverse:
   refund/delete the duplicates immediately (NO-GAIN).
6. `craft` as STATE; `export` → 3AM.

### R2 — Plan/seat-limit bypass via client-supplied scope ids (SaaS)

1. From the bundle, find the scope id the client sends (`scan` flags `org_id`/
   `tenant_id`/`workspace_id` in client calls).
2. On your own tenant at plan limit, send the upgrade/invite/seat request with a
   forged scope id in the BODY (server should read it from the session).
3. Decisive test: create limit+1 resources; count.
4. CONFIRMED when limit+1 exists. Reverse: delete the extra resources.
5. `craft` as IDOR (scope trust), `export`.

### R3 — Refund/fee drift via precision edges (fintech/e-commerce)

1. `undercroft precision --price <typical> --rate <fee> --ops 10000 --mode floor`
   → total drift + worst per-op amount.
2. On your own account: run the worst amount through the real refund/fee flow ×N.
3. Reconcile your statement vs the formula's exact total (`journal` seam).
4. CONFIRMED when real-world balance drifts in your favor beyond 1 smallest unit.
   Reverse: contact/void — nothing kept.
5. `craft` as MATH, `export`.

### R4 — Trial/TTL boundary crossing (SaaS/booking/anything time-gated)

1. Map the documented boundary: trial end, grace period, token TTL.
2. Fire the gated action at boundary−1s, boundary+1s (clock skew only on
   infrastructure you control).
3. CONFIRMED when expired-but-accepted (or pre-expiry grant) occurs.
4. Reverse: revert the granted state. `craft` as TIME, `export`.

### R5 — Checkout/order state-machine bypass (e-commerce/booking)

1. `undercroft stateflow --states "cart,paid,fulfilled,refunded" --guard "fulfilled:paid,refunded:paid" --flow checkout --target <c>`
2. Drive the generated matrix with your own orders: fire later transitions from
   earlier states (N+2 before N+1).
3. CONFIRMED when the flow lands in an undocumented state (e.g. refunded order
   that still fulfills, fulfilled without payment).
4. Reverse: cancel/void your own test orders. `craft` as STATE, `export`.

## Rhythm & hygiene

- Seams probed clean: EXHAUSTED with exact test string; never re-fired without a
  change in target state.
- Drift: re-verify before re-asserting a CONFIRMED seam from an earlier session.
- Chunking + noise budgets: family §12; bundles parsed locally, never uploaded.
- PII minimality inherited; samples ≤3, redacted.