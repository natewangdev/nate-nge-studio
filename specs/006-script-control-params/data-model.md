# Data Model: 006

## RunContext

+ `request_stop()` (existing)
+ `script_params: Mapping[str, Any]` (set at Start)

## ScriptParamField

id, type (`string`|`int`|`number`|`bool`|`choice`), label?, default?, choices?

## Manifest

+ `script_params: list[ScriptParamField]`

## LaunchParameters

+ `duration_end_action: "none"|"shutdown"` (default `none`)

## Settings launch_configs entry

```json
{ "parameters": { "...": "..." }, "script_params": { "friend_name": "..." } }
```
