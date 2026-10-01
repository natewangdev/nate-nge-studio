# Data Model: 007 Param Form Sections

No persistence or domain model changes. UI presentation entities only:

| Entity | Role |
|--------|------|
| LaunchParamGroup | `QGroupBox` title **启动参数**; hosts NGE2 + Studio duration fields |
| ScriptParamGroup | `QGroupBox` title **脚本参数**; hosts dynamic `script_params`; hidden when empty |

LaunchParameters / ScriptParamField / settings overlays unchanged from 001/006.
