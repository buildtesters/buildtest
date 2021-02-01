# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/module
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## module Type

`object` ([Details](settings-definitions-module.md))

# module Properties

| Property        | Type      | Required | Nullable       | Defined by                                                                                                                                    |
| :-------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| [purge](#purge) | `boolean` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module-properties-purge.md "settings.schema.json#/definitions/module/properties/purge") |
| [load](#load)   | `array`   | Optional | cannot be null | [buildtest configuration schema](definitions-definitions-list_of_strings.md "settings.schema.json#/definitions/module/properties/load")       |
| [swap](#swap)   | `array`   | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module-properties-swap.md "settings.schema.json#/definitions/module/properties/swap")   |

## purge

Run `module purge` if purge is set

`purge`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-module-properties-purge.md "settings.schema.json#/definitions/module/properties/purge")

### purge Type

`boolean`

## load

Load one or more modules via `module load`

`load`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](definitions-definitions-list_of_strings.md "settings.schema.json#/definitions/module/properties/load")

### load Type

`string[]`

### load Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## swap

Swap modules using `module swap`. The swap property expects 2 unique modules.

`swap`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-module-properties-swap.md "settings.schema.json#/definitions/module/properties/swap")

### swap Type

`string[]`

### swap Constraints

**maximum number of items**: the maximum number of items for this array is: `2`

**minimum number of items**: the minimum number of items for this array is: `2`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
