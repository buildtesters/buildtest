# Untitled object in script schema version Schema

```txt
script.schema.json#/definitions/compiler_declaration/properties/module
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                              |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :---------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script.schema.json*](../out/script.schema.json "open original schema") |

## module Type

`object` ([Details](script-definitions-compiler_declaration-properties-module.md))

# module Properties

| Property            | Type      | Required | Nullable       | Defined by                                                                                                                                                                                           |
| :------------------ | :-------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [purge](#purge)     | `boolean` | Optional | cannot be null | [script schema version](script-definitions-compiler_declaration-properties-module-properties-purge.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/purge")     |
| [load](#load)       | `array`   | Optional | cannot be null | [script schema version](definitions-definitions-list_of_strings.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/load")                                         |
| [restore](#restore) | `string`  | Optional | cannot be null | [script schema version](script-definitions-compiler_declaration-properties-module-properties-restore.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/restore") |
| [swap](#swap)       | `array`   | Optional | cannot be null | [script schema version](script-definitions-compiler_declaration-properties-module-properties-swap.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/swap")       |

## purge

Run `module purge` if purge is set

`purge`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [script schema version](script-definitions-compiler_declaration-properties-module-properties-purge.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/purge")

### purge Type

`boolean`

## load

Load one or more modules via `module load`

`load`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-list_of_strings.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/load")

### load Type

`string[]`

### load Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## restore

Load a collection name via `module restore`

`restore`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](script-definitions-compiler_declaration-properties-module-properties-restore.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/restore")

### restore Type

`string`

## swap

Swap modules using `module swap`. The swap property expects 2 unique modules.

`swap`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version](script-definitions-compiler_declaration-properties-module-properties-swap.md "script.schema.json#/definitions/compiler_declaration/properties/module/properties/swap")

### swap Type

`string[]`

### swap Constraints

**maximum number of items**: the maximum number of items for this array is: `2`

**minimum number of items**: the minimum number of items for this array is: `2`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
