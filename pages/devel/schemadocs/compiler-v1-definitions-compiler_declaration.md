# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers/properties/config/patternProperties/^.*$
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## ^.\*$ Type

`object` ([Details](compiler-v1-definitions-compiler_declaration.md))

# undefined Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                           |
| :-------------------- | -------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)             | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cc")             |
| [fc](#fc)             | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-fc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fc")             |
| [cxx](#cxx)           | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cxx.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxx")           |
| [cflags](#cflags)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cflags")     |
| [cxxflags](#cxxflags) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cxxflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxxflags") |
| [fflags](#fflags)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-fflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fflags")     |
| [ldflags](#ldflags)   | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-ldflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/ldflags")   |
| [cppflags](#cppflags) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cppflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cppflags") |
| [env](#env)           | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/env")                                           |
| [vars](#vars)         | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/vars")                                          |
| [status](#status)     | `object` | Optional | cannot be null | [compiler schema version 1.0](definitions-definitions-status.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/status")                                     |
| [run](#run)           | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/run")           |
| [module](#module)     | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-module.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/module")     |

## cc




`cc`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cc")

### cc Type

`string`

## fc




`fc`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-fc.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fc")

### fc Type

`string`

## cxx




`cxx`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cxx.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxx")

### cxx Type

`string`

## cflags




`cflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cflags")

### cflags Type

`string`

## cxxflags




`cxxflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cxxflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cxxflags")

### cxxflags Type

`string`

## fflags




`fflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-fflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/fflags")

### fflags Type

`string`

## ldflags




`ldflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-ldflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/ldflags")

### ldflags Type

`string`

## cppflags




`cppflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-cppflags.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/cppflags")

### cppflags Type

`string`

## env

One or more key value pairs for an environment (key=value)


`env`

-   is optional
-   Type: `object` ([Details](definitions-definitions-env.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/env")

### env Type

`object` ([Details](definitions-definitions-env.md))

### env Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## vars

One or more key value pairs for an environment (key=value)


`vars`

-   is optional
-   Type: `object` ([Details](definitions-definitions-env.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](definitions-definitions-env.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/vars")

### vars Type

`object` ([Details](definitions-definitions-env.md))

### vars Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## status

The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.


`status`

-   is optional
-   Type: `object` ([Details](definitions-definitions-status.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](definitions-definitions-status.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/status")

### status Type

`object` ([Details](definitions-definitions-status.md))

## run

Run command for launching compiled binary


`run`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-run.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/run")

### run Type

`string`

## module




`module`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-compiler_declaration-properties-module.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration-properties-module.md "compiler-v1.0.schema.json#/definitions/compiler_declaration/properties/module")

### module Type

`object` ([Details](compiler-v1-definitions-compiler_declaration-properties-module.md))
