# Untitled string in script schema version 1.0 Schema

```txt
script-v1.0.schema.json#/properties/shell
```

Specify a shell launcher to use when running jobs. This sets the shebang line in your test script. The `shell` key can be used with `run` section to describe content of script and how its executed


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [script-v1.0.schema.json\*](../out/script-v1.0.schema.json "open original schema") |

## shell Type

`string`

## shell Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|bash|sh|csh|tcsh|zsh|python).*
```

[try pattern](https://regexr.com/?expression=%5E(%2Fbin%2Fbash%7C%2Fbin%2Fsh%7C%2Fbin%2Fcsh%7C%2Fbin%2Ftcsh%7C%2Fbin%2Fzsh%7Cbash%7Csh%7Ccsh%7Ctcsh%7Czsh%7Cpython).* "try regular expression with regexr.com")
