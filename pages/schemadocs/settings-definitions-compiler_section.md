# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/compiler_section
```

A compiler section is composed of `cc`, `cxx` and `fc` wrapper these are required when you need to specify compiler wrapper.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## compiler\_section Type

`object` ([Details](settings-definitions-compiler_section.md))

# compiler\_section Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                              |
| :---------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-cc.md "settings.schema.json#/definitions/compiler_section/properties/cc")         |
| [cxx](#cxx)       | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-cxx.md "settings.schema.json#/definitions/compiler_section/properties/cxx")       |
| [fc](#fc)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-fc.md "settings.schema.json#/definitions/compiler_section/properties/fc")         |
| [module](#module) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/compiler_section/properties/module") |

## cc

Specify path to C compiler wrapper. You may specify a compiler wrapper such as `gcc` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.

`cc`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-cc.md "settings.schema.json#/definitions/compiler_section/properties/cc")

### cc Type

`string`

## cxx

Specify path to C++ compiler wrapper. You may specify a compiler wrapper such as `g++` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.

`cxx`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-cxx.md "settings.schema.json#/definitions/compiler_section/properties/cxx")

### cxx Type

`string`

## fc

Specify path to Fortran compiler wrapper. You may specify a compiler wrapper such as `gfortran` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.

`fc`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-fc.md "settings.schema.json#/definitions/compiler_section/properties/fc")

### fc Type

`string`

## module



`module`

*   is optional

*   Type: `object` ([Details](settings-definitions-module.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/compiler_section/properties/module")

### module Type

`object` ([Details](settings-definitions-module.md))
