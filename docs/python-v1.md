# python schema version 1.0 Schema

```txt
https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json
```

The script schema is of `type: python` in sub-schema which is used for running python scripts


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                       |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [python-v1.0.schema.json](../out/python-v1.0.schema.json "open original schema") |

## python schema version 1.0 Type

`object` ([python schema version 1.0](python-v1.md))

# python schema version 1.0 Properties

| Property                    | Type          | Required | Nullable       | Defined by                                                                                                                                                             |
| :-------------------------- | ------------- | -------- | -------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [type](#type)               | `string`      | Required | cannot be null | [python schema version 1.0](python-v1-properties-type.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/type")               |
| [description](#description) | Not specified | Optional | cannot be null | [python schema version 1.0](python-v1-properties-description.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/description") |
| [executor](#executor)       | Not specified | Required | cannot be null | [python schema version 1.0](python-v1-properties-executor.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/executor")       |
| [pyver](#pyver)             | `array`       | Required | cannot be null | [python schema version 1.0](python-v1-properties-pyver.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/pyver")             |
| [package](#package)         | `object`      | Optional | cannot be null | [python schema version 1.0](python-v1-properties-package.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package")         |
| [module](#module)           | `array`       | Optional | cannot be null | [python schema version 1.0](python-v1-properties-module.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/module")           |
| [sbatch](#sbatch)           | Not specified | Optional | cannot be null | [python schema version 1.0](python-v1-properties-sbatch.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/sbatch")           |
| [python](#python)           | `string`      | Required | cannot be null | [python schema version 1.0](python-v1-properties-python.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/python")           |
| [script](#script)           | `string`      | Optional | cannot be null | [python schema version 1.0](python-v1-properties-script.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/script")           |
| [status](#status)           | Not specified | Optional | cannot be null | [python schema version 1.0](python-v1-properties-status.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/status")           |
| [skip](#skip)               | Not specified | Optional | cannot be null | [python schema version 1.0](python-v1-properties-skip.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/skip")               |
| [tags](#tags)               | Not specified | Optional | cannot be null | [python schema version 1.0](python-v1-properties-tags.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/tags")               |

## type




`type`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-type.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/type")

### type Type

`string`

### type Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^python$
```

[try pattern](https://regexr.com/?expression=%5Epython%24 "try regular expression with regexr.com")

## description




`description`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-description.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/description")

### description Type

unknown

## executor




`executor`

-   is required
-   Type: unknown
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-executor.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/executor")

### executor Type

unknown

## pyver




`pyver`

-   is required
-   Type: `number[]`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-pyver.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/pyver")

### pyver Type

`number[]`

## package




`package`

-   is optional
-   Type: `object` ([Details](python-v1-properties-package.md))
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-package.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package")

### package Type

`object` ([Details](python-v1-properties-package.md))

## module




`module`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-module.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/module")

### module Type

`string[]`

## sbatch




`sbatch`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-sbatch.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/sbatch")

### sbatch Type

unknown

## python

A python script to run


`python`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-python.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/python")

### python Type

`string`

## script




`script`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-script.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/script")

### script Type

`string`

## status




`status`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-status.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/status")

### status Type

unknown

## skip




`skip`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-skip.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/skip")

### skip Type

unknown

## tags




`tags`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-tags.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/tags")

### tags Type

unknown
