# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json*](../out/compiler-v1.0.schema.json "open original schema") |

## compilers Type

`object` ([Details](compiler-v1-properties-compilers.md))

# undefined Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                 |
| :------------------ | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)       | `array`  | Required | cannot be null | [compiler schema version 1.0](definitions-definitions-list_of_strings.md "compiler-v1.0.schema.json#/properties/compilers/properties/name")                |
| [exclude](#exclude) | `array`  | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-list_of_strings.md "compiler-v1.0.schema.json#/properties/compilers/properties/exclude")             |
| [default](#default) | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-compilers-properties-default.md "compiler-v1.0.schema.json#/properties/compilers/properties/default") |
| [config](#config)   | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-compilers-properties-config.md "compiler-v1.0.schema.json#/properties/compilers/properties/config")   |

## name

Specify a list of regular expression to search compiler instance from buildtest settings.

`name`

*   is required

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](definitions-definitions-list_of_strings.md "compiler-v1.0.schema.json#/properties/compilers/properties/name")

### name Type

`string[]`

### name Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## exclude

Specify a list of named compilers to exclude when building test based on regular expression specified in `name` property. The `exclude` property has no effect if named compiler not found based on regular expression.

`exclude`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [compiler schema version 1.0](definitions-definitions-list_of_strings.md "compiler-v1.0.schema.json#/properties/compilers/properties/exclude")

### exclude Type

`string[]`

### exclude Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## default



`default`

*   is optional

*   Type: `object` ([Details](compiler-v1-properties-compilers-properties-default.md))

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-properties-compilers-properties-default.md "compiler-v1.0.schema.json#/properties/compilers/properties/default")

### default Type

`object` ([Details](compiler-v1-properties-compilers-properties-default.md))

## config

Specify compiler configuration based on named compilers.

`config`

*   is optional

*   Type: `object` ([Details](compiler-v1-properties-compilers-properties-config.md))

*   cannot be null

*   defined in: [compiler schema version 1.0](compiler-v1-properties-compilers-properties-config.md "compiler-v1.0.schema.json#/properties/compilers/properties/config")

### config Type

`object` ([Details](compiler-v1-properties-compilers-properties-config.md))
