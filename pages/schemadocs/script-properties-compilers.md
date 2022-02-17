# Untitled object in script schema version Schema

```txt
script.schema.json#/properties/compilers
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script.schema.json\*](../out/script.schema.json "open original schema") |

## compilers Type

`object` ([Details](script-properties-compilers.md))

# compilers Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                               |
| :------------------ | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)       | `array`  | Required | cannot be null | [script schema version](definitions-definitions-list_of_strings.md "script.schema.json#/properties/compilers/properties/name")           |
| [exclude](#exclude) | `array`  | Optional | cannot be null | [script schema version](definitions-definitions-list_of_strings.md "script.schema.json#/properties/compilers/properties/exclude")        |
| [default](#default) | `object` | Optional | cannot be null | [script schema version](script-properties-compilers-properties-default.md "script.schema.json#/properties/compilers/properties/default") |
| [config](#config)   | `object` | Optional | cannot be null | [script schema version](script-properties-compilers-properties-config.md "script.schema.json#/properties/compilers/properties/config")   |

## name

Specify a list of regular expression to search compiler instance from buildtest settings.

`name`

*   is required

*   Type: `string[]`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-list_of_strings.md "script.schema.json#/properties/compilers/properties/name")

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

*   defined in: [script schema version](definitions-definitions-list_of_strings.md "script.schema.json#/properties/compilers/properties/exclude")

### exclude Type

`string[]`

### exclude Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## default



`default`

*   is optional

*   Type: `object` ([Details](script-properties-compilers-properties-default.md))

*   cannot be null

*   defined in: [script schema version](script-properties-compilers-properties-default.md "script.schema.json#/properties/compilers/properties/default")

### default Type

`object` ([Details](script-properties-compilers-properties-default.md))

## config

Specify compiler configuration based on named compilers.

`config`

*   is optional

*   Type: `object` ([Details](script-properties-compilers-properties-config.md))

*   cannot be null

*   defined in: [script schema version](script-properties-compilers-properties-config.md "script.schema.json#/properties/compilers/properties/config")

### config Type

`object` ([Details](script-properties-compilers-properties-config.md))
