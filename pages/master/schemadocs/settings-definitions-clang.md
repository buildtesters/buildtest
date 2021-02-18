# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/clang
```

The clang compiler section consist of `cc` and `cxx` wrapper to specify C and C++ wrapper which are generally `clang` and `clang++`

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## clang Type

`object` ([Details](settings-definitions-clang.md))

# clang Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                   |
| :---------------- | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-cc.md "settings.schema.json#/definitions/clang/properties/cc")         |
| [cxx](#cxx)       | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-cxx.md "settings.schema.json#/definitions/clang/properties/cxx")       |
| [module](#module) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/clang/properties/module") |

## cc

Specify path to C compiler wrapper. You may specify a compiler wrapper such as `gcc` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.

`cc`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-cc.md "settings.schema.json#/definitions/clang/properties/cc")

### cc Type

`string`

## cxx

Specify path to C++ compiler wrapper. You may specify a compiler wrapper such as `g++` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.

`cxx`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-cxx.md "settings.schema.json#/definitions/clang/properties/cxx")

### cxx Type

`string`

## module



`module`

*   is optional

*   Type: `object` ([Details](settings-definitions-module.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/clang/properties/module")

### module Type

`object` ([Details](settings-definitions-module.md))
