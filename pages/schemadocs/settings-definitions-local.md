# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/local
```

An instance object of local executor

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## local Type

`object` ([Details](settings-definitions-local.md))

# local Properties

| Property                        | Type          | Required | Nullable       | Defined by                                                                                                                                                  |
| :------------------------------ | :------------ | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [description](#description)     | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-description.md "settings.schema.json#/definitions/local/properties/description")     |
| [shell](#shell)                 | `string`      | Required | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-shell.md "settings.schema.json#/definitions/local/properties/shell")                 |
| [before_script](#before_script) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-before_script.md "settings.schema.json#/definitions/local/properties/before_script") |
| [max_jobs](#max_jobs)           | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-max_jobs.md "settings.schema.json#/definitions/local/properties/max_jobs")                            |

## description

description field for documenting your executor

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-local-properties-description.md "settings.schema.json#/definitions/local/properties/description")

### description Type

`string`

## shell

Specify the shell launcher you want to use when running tests locally

`shell`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-local-properties-shell.md "settings.schema.json#/definitions/local/properties/shell")

### shell Type

`string`

### shell Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|sh|bash|csh|tcsh|zsh|python).*
```

[try pattern](https://regexr.com/?expression=%5E\(%2Fbin%2Fbash%7C%2Fbin%2Fsh%7C%2Fbin%2Fcsh%7C%2Fbin%2Ftcsh%7C%2Fbin%2Fzsh%7Csh%7Cbash%7Ccsh%7Ctcsh%7Czsh%7Cpython\).\* "try regular expression with regexr.com")

## before_script



`before_script`

*   is optional

*   Type: unknown

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-local-properties-before_script.md "settings.schema.json#/definitions/local/properties/before_script")

### before_script Type

unknown

## max_jobs

Maximum number of jobs that can be run at a given time for a particular executor

`max_jobs`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-max_jobs.md "settings.schema.json#/definitions/local/properties/max_jobs")

### max_jobs Type

`integer`

### max_jobs Constraints

**minimum**: the value of this number must greater than or equal to: `1`
