# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/properties/compilers/properties/compiler/properties/clang
```

Declaration of one or more Clang compilers where we define C, C++ compiler. The Clang compiler wrapper are `clang`, `clang++`.


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## clang Type

`object` ([Details](settings-properties-compilers-properties-compiler-properties-clang.md))

# undefined Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                                |
| :------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-clang.md "settings.schema.json#/properties/compilers/properties/compiler/properties/clang/patternProperties/^.\*$") |

## Pattern: `^.*$`

The clang compiler section consist of `cc` and `cxx` wrapper to specify C and C++ wrapper which are generally `clang` and `clang++`


`^.*$`

-   is optional
-   Type: `object` ([Details](settings-definitions-clang.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-clang.md "settings.schema.json#/properties/compilers/properties/compiler/properties/clang/patternProperties/^.\*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-clang.md))
