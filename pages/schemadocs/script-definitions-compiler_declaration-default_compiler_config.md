# Untitled object in script schema version Schema

```txt
script.schema.json#/definitions/compiler_declaration/default_compiler_config
```

Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides `all` property.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                               |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :----------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [script.schema.json\*](../out/script.schema.json "open original schema") |

## default\_compiler\_config Type

`object` ([Details](script-definitions-compiler_declaration-default_compiler_config.md))

# default\_compiler\_config Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                      |
| :-------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cc")             |
| [fc](#fc)             | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/fc")             |
| [cxx](#cxx)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cxx")           |
| [cflags](#cflags)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cflags")     |
| [fflags](#fflags)     | `string` | Optional | cannot be null | [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/fflags")     |
| [cxxflags](#cxxflags) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cxxflags") |
| [ldflags](#ldflags)   | `string` | Optional | cannot be null | [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/ldflags")   |
| [cppflags](#cppflags) | `string` | Optional | cannot be null | [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cppflags") |
| [env](#env)           | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/env")           |
| [vars](#vars)         | `object` | Optional | cannot be null | [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/vars")          |
| [run](#run)           | `string` | Optional | cannot be null | [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/run")           |

## cc

Set C compiler wrapper

`cc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cc.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cc")

### cc Type

`string`

## fc

Set Fortran compiler wrapper

`fc`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fc.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/fc")

### fc Type

`string`

## cxx

Set C++ compiler wrapper

`cxx`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxx.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cxx")

### cxx Type

`string`

## cflags

Set C compiler flags.

`cflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cflags")

### cflags Type

`string`

## fflags

Set Fortran compiler flags.

`fflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-fflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/fflags")

### fflags Type

`string`

## cxxflags

Set C++ compiler flags.

`cxxflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cxxflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cxxflags")

### cxxflags Type

`string`

## ldflags

Set linker flags

`ldflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-ldflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/ldflags")

### ldflags Type

`string`

## cppflags

Set C or C++ preprocessor flags

`cppflags`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-cppflags.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/cppflags")

### cppflags Type

`string`

## env

One or more key value pairs for an environment (key=value)

`env`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/env")

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

*   defined in: [script schema version](definitions-definitions-env.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## run

Specify a series of commands to run.

`run`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [script schema version](definitions-definitions-run.md "script.schema.json#/definitions/compiler_declaration/default_compiler_config/properties/run")

### run Type

`string`
