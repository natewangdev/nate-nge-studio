<!--
Sync Impact Report
- Version change: (none) → 1.0.0 (initial ratification)
- Modified principles: N/A (initial)
- Added sections: Core Principles I–VII; Platform & Product Constraints; Quality Gates; Governance
- Removed sections: N/A
- Deferred TODOs: none
-->
# NGE-STUDIO Constitution

This constitution governs **NGE-STUDIO**: a Windows desktop application that discovers,
configures, and runs game scripts built on the **NGE2** engine (`nate-game-engine`).
Feature specs define *what* to build; this document defines *non-negotiable how*.

Chinese companion (human-readable only): [`constitution.zh-CN.md`](./constitution.zh-CN.md).
Agents executing Spec Kit workflows MUST use this English file as the sole authority.

## Core Principles

### I. Desktop Product First

- NGE-STUDIO is an end-user **desktop application** (product shell), not a reusable library.
- Core user value is delivered through a visual interface: script catalog, launch parameters,
  lifecycle controls, and live logs.
- Shared non-UI logic (catalog discovery, run orchestration, settings persistence) MAY live in
  importable modules, but the primary deliverable is a runnable Windows app (including packaged
  executable distribution).
- Do not add modules whose only purpose is organizational convenience without a clear product
  or script-author contract.

### II. NGE2 as the Sole Game Engine

- All game scripts managed by Studio MUST run on **NGE2** (`nge2` from `nate-game-engine`).
- Studio MUST depend on NGE2 as a **pip-installable** package (editable local path and/or
  published distribution). Do not vendor a fork of the engine inside this repository.
- Launch parameters exposed in the UI MUST cover the full set of documented NGE2 construction
  parameters that script authors need, plus Studio-owned controls (e.g. run-duration timeout).
- When NGE2 public API changes, Studio MUST update its parameter surface and docs in the same
  feature change that adopts the new engine version.

### III. Packaged Script Catalog (NON-NEGOTIABLE)

- Game scripts live under a conventional tree and are **discovered at build/package time**, not
  by hot-scanning arbitrary external folders at runtime after an already-built executable ships.
- Adding a game folder or a new script under a game folder requires a **rebuild/repackage**
  before the catalog appears in the UI of that build.
- Every script directory MUST include a **manifest** describing display metadata and optional
  default launch parameters. Folder names are the stable game/script IDs.
- Scripts MUST implement a **unified entry protocol** defined by Studio (cooperative pause/stop
  via a run context). Ad-hoc entrypoints without the protocol are out of scope for the catalog.

### IV. Cooperative Lifecycle & Single Runner (NON-NEGOTIABLE)

- At most **one** script run is active at a time. Starting another run while one is active MUST
  be refused with a clear user-visible reason (HID/device exclusivity and product simplicity).
- **Pause** is cooperative: Studio signals pause; the script observes the run context and yields.
- **Stop** cancels via the run context and Studio MUST close the NGE2 engine instance after the
  run ends or is aborted (release devices/backends).
- Hard process kill is not the primary stop path. Forceful termination is only a last resort
  after documented timeouts or unrecoverable hangs, if a later feature explicitly requires it.

### V. Observability & Operator Control

- While a script runs, the UI MUST show **near-real-time** log output suitable for operators.
- Start / pause / stop MUST be available both as on-screen controls and as **global hotkeys**.
- Hotkey bindings are user-configurable and MUST persist across application restarts.
- Default bindings: Start = F9, Pause = F10, Stop = F11 (one binding each).

### VI. Bilingual Requirement Documents (NON-NEGOTIABLE)

- Every requirement-facing Markdown artifact produced by Spec Kit (including but not limited
  to `spec.md`, `plan.md`, `tasks.md`, checklists, and clarify/analyze reports under feature
  directories) MUST exist in **both** an English edition and a Simplified Chinese edition.
- Naming: English files keep the canonical Spec Kit names (e.g. `spec.md`). Chinese files
  use the same basename with a `.zh-CN` suffix before the extension (e.g. `spec.zh-CN.md`).
- Any create or update of a requirement Markdown file MUST update the English and Chinese
  editions in the **same change**. Divergent or single-language-only updates are not allowed.
- Content MUST stay information-equivalent across the pair (same intent, scope, acceptance
  criteria, and constraints). Wording may be localized; facts MUST NOT drift.
- **Execution authority**: when planning, implementing, analyzing, or converging, agents
  MUST read and follow **English** Markdown only. Chinese editions (any `*.zh-CN.md`) are
  for the human maintainer whose native language is Chinese; they have **no operational
  effect** and MUST be ignored for Spec Kit execution decisions.

### VII. Bilingual Constitution (NON-NEGOTIABLE)

- This constitution is maintained as a bilingual pair:
  - English (authoritative for agents): `.specify/memory/constitution.md`
  - Simplified Chinese (human-readable only): `.specify/memory/constitution.zh-CN.md`
- Every amendment MUST update **both** files in the same change, keep them
  information-equivalent, bump **Version**, and set **Last Amended** identically on both.
- Spec Kit skills and implement/converge flows MUST treat the English constitution as the
  only binding source. The Chinese constitution MUST NOT be used as an execution input.

## Platform & Product Constraints

- **Primary target**: Windows desktop. Design, test, and document against Windows first.
- **UI stack**: Python desktop GUI with a modern, tech-oriented visual design. Prefer Qt for
  Python (PySide6) unless a ratified amendment chooses another toolkit.
- **Distribution**: ship a Windows **executable** (packaged app) as a first-class deliverable.
- **Python**: `>=3.11` unless `pyproject.toml` raises the floor in the same change.
- **Packaging source of truth**: `pyproject.toml` (and documented packaging recipe for the exe).
- **Non-goals unless specified**: multi-OS parity, multi-script parallel runs, cloud/multi-user
  accounts, marketplace for third-party scripts, or replacing NGE2 itself.

## Quality Gates

- User-visible behavior changes: automated tests for orchestration/catalog/settings logic where
  practical; UI smoke paths documented in the feature plan’s Definition of Done.
- Lint/format tooling configured for the repo MUST pass when present in the plan’s Definition
  of Done.
- Complexity that is not forced by a requirement MUST be rejected or deferred; justify
  exceptions in the plan.
- Spec Kit flow for features: constitution compliance is checked during plan, tasks, and
  implement/converge—not only at the end.
- Bilingual pairs: a change that touches requirement Markdown or the constitution is
  incomplete if either language edition is missing or stale.

## Governance

- This constitution supersedes informal chat agreements and ad-hoc coding preferences when
  they conflict.
- Amendments update **both** `constitution.md` and `constitution.zh-CN.md`, bump the
  constitution **Version**, and set **Last Amended**. Material rule changes should be called
  out in the next feature plan that relies on them.
- `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`, and `/speckit-converge` MUST NOT
  introduce designs that violate these principles without an explicit, documented amendment.
- When unsure whether a rule applies, prefer a narrower product surface, single-runner safety,
  cooperative lifecycle, and stronger operator visibility (logs + controls).

**Version**: 1.0.0 | **Ratified**: 2026-09-28 | **Last Amended**: 2026-09-28
