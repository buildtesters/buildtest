# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/build
```

The `build` section is used for compiling a single program, this section specifies fields for setting C, C++, Fortran compiler and flags including CPP flags and linker flags


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## build Type

`object` ([Details](compiler-v1-properties-build.md))

# undefined Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                           |
| :-------------------- | -------- | -------- | -------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| [name](#name)         | `string` | Required | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-name.md "compiler-v1.0.schema.json#/properties/build/properties/name")         |
| [cc](#cc)             | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-cc.md "compiler-v1.0.schema.json#/properties/build/properties/cc")             |
| [fc](#fc)             | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-fc.md "compiler-v1.0.schema.json#/properties/build/properties/fc")             |
| [cxx](#cxx)           | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-cxx.md "compiler-v1.0.schema.json#/properties/build/properties/cxx")           |
| [source](#source)     | `string` | Required | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-source.md "compiler-v1.0.schema.json#/properties/build/properties/source")     |
| [cflags](#cflags)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-cflags.md "compiler-v1.0.schema.json#/properties/build/properties/cflags")     |
| [cxxflags](#cxxflags) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-cxxflags.md "compiler-v1.0.schema.json#/properties/build/properties/cxxflags") |
| [fflags](#fflags)     | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-fflags.md "compiler-v1.0.schema.json#/properties/build/properties/fflags")     |
| [cppflags](#cppflags) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-cppflags.md "compiler-v1.0.schema.json#/properties/build/properties/cppflags") |
| [ldflags](#ldflags)   | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-build-properties-ldflags.md "compiler-v1.0.schema.json#/properties/build/properties/ldflags")   |

## name

Select the compiler class to use, buildtest will set cc, cxx, and fc compiler wrapper based on compiler name


`name`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-name.md "compiler-v1.0.schema.json#/properties/build/properties/name")

### name Type

`string`

### name Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | ----------- |
| `"gnu"`   |             |
| `"intel"` |             |
| `"pgi"`   |             |
| `"cray"`  |             |

## cc

Set C compiler. Use this field to override buildtest selection for **cc**


`cc`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-cc.md "compiler-v1.0.schema.json#/properties/build/properties/cc")

### cc Type

`string`

## fc

Set Fortran compiler. Use this field to override buildtest selection for **fc**


`fc`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-fc.md "compiler-v1.0.schema.json#/properties/build/properties/fc")

### fc Type

`string`

## cxx

Set C++ compiler. Use this field to override buildtest selection for **cxx**


`cxx`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-cxx.md "compiler-v1.0.schema.json#/properties/build/properties/cxx")

### cxx Type

`string`

## source

Specify a source file for compilation, the file can be relative path to buildspec or an absolute path


`source`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-source.md "compiler-v1.0.schema.json#/properties/build/properties/source")

### source Type

`string`

## cflags

Set C compiler flags (**cflags**)


`cflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-cflags.md "compiler-v1.0.schema.json#/properties/build/properties/cflags")

### cflags Type

`string`

## cxxflags

Set C++ compiler flags (**cxxflags**)


`cxxflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-cxxflags.md "compiler-v1.0.schema.json#/properties/build/properties/cxxflags")

### cxxflags Type

`string`

## fflags

Set Fortran compiler flags (**fflags**)


`fflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-fflags.md "compiler-v1.0.schema.json#/properties/build/properties/fflags")

### fflags Type

`string`

## cppflags

Set Pre Processor Flags (**cppflags**)


`cppflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-cppflags.md "compiler-v1.0.schema.json#/properties/build/properties/cppflags")

### cppflags Type

`string`

## ldflags

Set linker flags (**ldflags**)


`ldflags`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-build-properties-ldflags.md "compiler-v1.0.schema.json#/properties/build/properties/ldflags")

### ldflags Type

`string`
