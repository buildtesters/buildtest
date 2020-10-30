# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## compiler_section Type

`object` ([Details](settings-definitions-compiler_section.md))

# undefined Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                  |
| :------------------ | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)           | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cc")           |
| [cxx](#cxx)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-cxx.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cxx")         |
| [fc](#fc)           | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-fc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/fc")           |
| [modules](#modules) | `array`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-modules.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/modules") |

## cc




`cc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cc")

### cc Type

`string`

## cxx




`cxx`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-cxx.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cxx")

### cxx Type

`string`

## fc




`fc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-fc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/fc")

### fc Type

`string`

## modules




`modules`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-modules.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/modules")

### modules Type

`string[]`

### modules Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.
