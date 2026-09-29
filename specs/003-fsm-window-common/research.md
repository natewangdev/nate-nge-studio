# Research

## FSM
- **Decision**: `dataclasses.is_dataclass(instance)` and not a type; reject dict.
- **Rationale**: 002 clarification Option B.

## Title resolve
- **Decision**: `nge2.window.Window(None).find_by_title(query)[0].hwnd` before construct.
- **Rationale**: Same semantics as engine API; no new matching logic.

## Activate
- **Decision**: After `NGE2(...)` when hwnd bound, `engine.window.activate()`.
- **Rationale**: 001 FR-005g.

## Game path
- **Decision**: `sys.path.insert(0, game_dir)` then script_dir when loading main.
- **Rationale**: `import common` / `import rules` from game folder.
