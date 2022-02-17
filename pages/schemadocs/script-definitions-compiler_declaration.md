# Untitled object in script schema version Schema

```txt
script.schema.json#/definitions/compiler_declaration
```

Specify compiler configuration at compiler level. The `config` section has highest precedence when searching compiler configuration. This overrides fields found in compiler group and `all` property

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [script.schema.json\*](../out/script.schema.json "open original schema") |

## compiler\_declaration Type

`object` ([Details](script-definitions-compiler_declaration.md))

# compiler\_declaration Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                              |
| :-------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/compiler_declaration/properties/cc")             |
| [fc](#fc)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/compiler_declaration/properties/fc")             |
| [cxx](#cxx)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/compiler_declaration/properties/cxx")           |
| [cflags](#cflags)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/compiler_declaration/properties/cflags")     |
| [fflags](#fflags)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/compiler_declaration/properties/fflags")     |
| [cxxflags](#cxxflags) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/compiler_declaration/properties/cxxflags") |
| [ldflags](#ldflags)   | `string` | Optional | cannot be null | [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/compiler_declaration/properties/ldflags")   |
| [cppflags](#cppflags) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/compiler_declaration/properties/cppflags") |
| [env](#env)           | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/env")           |
| [vars](#vars)         | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/vars")          |
| [status](#status)     | `object` | Optional | cannot be null | [script schema version](definitions-definitions-status.md "script.schema.json#/definitions/compiler_declaration/properties/status")     |
| [run](#run)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/compiler_declaration/properties/run")           |
| [module](#module)     | `object` | Optional | cannot be null | [script schema version](definitions-definitions-module.md "script.schema.json#/definitions/compiler_declaration/properties/module")     |

## cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/compiler_declaration/properties/cc")

### cc Type

`string`

## fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/compiler_declaration/properties/fc")

### fc Type

`string`

## cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/compiler_declaration/properties/cxx")

### cxx Type

`string`

## cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/compiler_declaration/properties/cflags")

### cflags Type

`string`

## fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/compiler_declaration/properties/fflags")

### fflags Type

`string`

## cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/compiler_declaration/properties/cxxflags")

### cxxflags Type

`string`

## ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/compiler_declaration/properties/ldflags")

### ldflags Type

`string`

## cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/compiler_declaration/properties/cppflags")

### cppflags Type

`string`

## env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/env")

### env Type

`object` ([Details](definitions-definitions-env.md))

### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## vars

One or more key value pairs for an environment (key=value)

`vars`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.

`status`

*   is optional

*   Type: `object` ([Details](definitions-definitions-status.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-status.md "script.schema.json#/definitions/compiler_declaration/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## run

Specify a series of commands to run.

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/compiler_declaration/properties/run")

### run Type

`string`

## module



`module`

*   is optional

*   Type: `object` ([Details](definitions-definitions-module.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-module.md "script.schema.json#/definitions/compiler_declaration/properties/module")

### module Type

`object` ([Details](definitions-definitions-module.md))
