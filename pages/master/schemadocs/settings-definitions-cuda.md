# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/cuda
```

The cuda compiler section consist of `cc`  where you generally specify path to `nvcc`


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## cuda Type

`object` ([Details](settings-definitions-cuda.md))

# undefined Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                  |
| :---------------- | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-cc.md "settings.schema.json#/definitions/cuda/properties/cc")         |
| [module](#module) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/cuda/properties/module") |

## cc

Specify path to C compiler wrapper. You may specify a compiler wrapper such as `gcc` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`cc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-cc.md "settings.schema.json#/definitions/cuda/properties/cc")

### cc Type

`string`

## module




`module`

-   is optional
-   Type: `object` ([Details](settings-definitions-module.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/cuda/properties/module")

### module Type

`object` ([Details](settings-definitions-module.md))
