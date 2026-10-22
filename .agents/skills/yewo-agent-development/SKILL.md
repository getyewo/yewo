---
name: yewo-agent-development
description: Implement or review Python changes to Yewo's CLI, mobile-agent loop, planning, perception, actuation, device lifecycle, configuration, or reporting. Use for production changes under src/yewo.
---

# Yewo agent development

Work on Yewo as a Python 3.12+ mobile-testing agent. Use `uv` and
`pyproject.toml` for Python dependencies.

## Locate the owner

Inspect the implementation and its callers before editing. Use the current
package boundaries:

- `src/yewo/cli`: command parsing and dispatch
- `src/yewo/agent`: the observe-plan-act loop, what it asks the model, and
  the record it keeps
- `src/yewo/agent/step`: what one step needs and nothing its callers do —
  observation, targeting, staleness, narration, artifacts, outcomes
- `src/yewo/agent/perception`: screenshots, OCR, detections, and annotations
- `src/yewo/agent/actuation`: action contracts and dispatch
- `src/yewo/agent/device`: Appium sessions, platform mechanics, app launch
- `src/yewo/devices`: device discovery and provisioning
- `src/yewo/llm`: model transport, messages, schemas, and usage callbacks
- `src/yewo/testing`: journey generation, execution, progress, and reports
- `src/yewo/setup` and `src/yewo/doctor`: setup and diagnostics
- `src/yewo/utils`: shared platform, subprocess, redaction, and secret helpers

`main.py` is a deprecated compatibility shim. Add CLI behavior through
`src/yewo/cli` and the `yewo` entry point.

## Preserve the execution model

- Keep perception independent from actuation. Planning produces validated
  actions; device code owns platform mechanics.
- Treat model responses and detected coordinates as untrusted. Validate action
  kinds, required fields, dimensions, bounds, and durations before dispatch.
- Make screenshot-to-device coordinate conversion explicit. Re-observe after an
  action before making decisions that depend on the new screen.
- Bound loops, retries, subprocesses, and timeouts. Never blindly retry a
  non-idempotent tap, submission, or text entry.
- Distinguish goal completion, failed verification, exhausted steps, app
  defects, app crashes, infrastructure failures, interruption, and skipped
  work. A model's claim of completion is not sufficient evidence.
- Own cleanup for partial startup, exceptions, and cancellation. Stop only
  resources created by the current run.
- Keep Android ADB and iOS simulator behavior separate. Run platform preflight
  before changing device state, and do not assume iOS tooling exists off macOS.
- Keep slow SDK, model, and device calls explicit at synchronous/asynchronous
  boundaries.

## Protect contracts and artifacts

Preserve public Pydantic schemas, action values, journey fields, CLI flags,
defaults, exit behavior, and report formats unless the task changes the
contract. Update callers, documentation, and tests together when a contract
changes.

Sanitize journey-derived artifact paths, isolate parallel runs, and keep
Markdown, JUnit, progress, and usage results consistent. Surface report-writing
failures. Never expose API credentials or sensitive app content in logs,
screenshots, prompts, recordings, or reports, and do not read or print `.env`.
Do not silently change providers, models, or spending defaults.

## Keep changes maintainable

Prefer focused functions, explicit types, constructor-injected boundaries, and
one owner for shared validation or conversion logic. Do not add abstraction
layers without an actual interchangeable boundary or data owner. Preserve
public names unless their callers are migrated.

Use controlled language for prompts, error messages, tool descriptions, and
safety text. Write short active sentences. State one instruction or condition
per sentence. Use one name for one thing. Preserve conditions and uncertainty;
do not simplify a qualified claim into an unconditional one.

Do not use `getattr`, `hasattr`, or `setattr` inside a typed internal contract
to compensate for an unclear model. Use a discriminated Pydantic model,
`isinstance`, `match`, a protocol, or an explicit adapter instead. At an SDK,
driver, or untrusted-model boundary, dynamic access is allowed only while
normalizing the value into a validated, typed contract. Keep that adaptation at
the boundary; do not pass dynamic objects into agent logic.

For production changes, apply the measurable ratchets in the
[quality-gates reference](../yewo-test-engineering/references/quality-gates.md).
Do not increase an existing exception merely because it is baselined.

Comments should explain rationale, units, ownership, platform constraints, or
retry safety that the code cannot express. Preserve Pydantic field descriptions
and prompt text that affect model behavior. Avoid narrated steps, redundant
docstrings, decorative sections, and commented-out code.

For test design and verification, also read the `yewo-test-engineering` skill.
Do not start emulators, download model weights, or make paid model calls as an
incidental check.
