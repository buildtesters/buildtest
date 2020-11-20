# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find
```

Find compilers based on module names


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## find Type

`object` ([Details](settings-properties-compilers-properties-find.md))

# undefined Properties

| Property        | Type    | Required | Nullable       | Defined by                                                                                                                                                                                                        |
| :-------------- | ------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [gcc](#gcc)     | `array` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/gcc")   |
| [intel](#intel) | `array` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/intel") |
| [cray](#cray)   | `array` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/cray")  |
| [clang](#clang) | `array` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/clang") |
| [cuda](#cuda)   | `array` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/cuda")  |
| [pgi](#pgi)     | `array` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/pgi")   |

## gcc




`gcc`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/gcc")

### gcc Type

`string[]`

### gcc Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## intel




`intel`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/intel")

### intel Type

`string[]`

### intel Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## cray




`cray`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/cray")

### cray Type

`string[]`

### cray Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## clang




`clang`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/clang")

### clang Type

`string[]`

### clang Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## cuda




`cuda`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/cuda")

### cuda Type

`string[]`

### cuda Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## pgi




`pgi`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/find/properties/pgi")

### pgi Type

`string[]`

### pgi Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.
