# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cuda
```

Declaration of one or more Cuda compilers where we define C compiler. The Cuda compiler wrapper is `nvcc`. 


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## cuda Type

`object` ([Details](settings-properties-compilers-properties-cuda.md))

# undefined Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                |
| :------- | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-cuda.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cuda/patternProperties/^.\*$") |

## Pattern: `^.*$`

The cuda compiler section consist of `cc`  where you generally specify path to `nvcc`


`^.*$`

-   is optional
-   Type: `object` ([Details](settings-definitions-cuda.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-cuda.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/cuda/patternProperties/^.\*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-cuda.md))
