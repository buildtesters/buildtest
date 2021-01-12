# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/local
```

An instance object of local executor


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## local Type

`object` ([Details](settings-definitions-local.md))

# undefined Properties

| Property                        | Type          | Required | Nullable       | Defined by                                                                                                                                                  |
| :------------------------------ | ------------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [description](#description)     | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-description.md "settings.schema.json#/definitions/local/properties/description")     |
| [shell](#shell)                 | `string`      | Required | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-shell.md "settings.schema.json#/definitions/local/properties/shell")                 |
| [before_script](#before_script) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-before_script.md "settings.schema.json#/definitions/local/properties/before_script") |
| [after_script](#after_script)   | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-after_script.md "settings.schema.json#/definitions/local/properties/after_script")   |

## description

description field for documenting your executor


`description`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-description.md "settings.schema.json#/definitions/local/properties/description")

### description Type

`string`

## shell

Specify the shell launcher you want to use when running tests locally


`shell`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-shell.md "settings.schema.json#/definitions/local/properties/shell")

### shell Type

`string`

### shell Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|sh|bash|csh|tcsh|zsh|python).*
```

[try pattern](https://regexr.com/?expression=%5E(%2Fbin%2Fbash%7C%2Fbin%2Fsh%7C%2Fbin%2Fcsh%7C%2Fbin%2Ftcsh%7C%2Fbin%2Fzsh%7Csh%7Cbash%7Ccsh%7Ctcsh%7Czsh%7Cpython).* "try regular expression with regexr.com")

## before_script




`before_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-before_script.md "settings.schema.json#/definitions/local/properties/before_script")

### before_script Type

unknown

## after_script




`after_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-after_script.md "settings.schema.json#/definitions/local/properties/after_script")

### after_script Type

unknown
