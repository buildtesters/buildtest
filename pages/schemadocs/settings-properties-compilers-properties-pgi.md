# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/pgi
```

Declaration of one or more PGI compilers where we define C, C++ and Fortran compiler. The PGI compiler wrapper are `pgcc`, `pgc++` and `pgfortran`.


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## pgi Type

`object` ([Details](settings-properties-compilers-properties-pgi.md))

# undefined Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                           |
| :------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/pgi/patternProperties/^.\*$") |

## Pattern: `^.*$`

A compiler section is composed of `cc`, `cxx` and `fc` wrapper these are required when you need to specify compiler wrapper.


`^.*$`

-   is optional
-   Type: `object` ([Details](settings-definitions-compiler_section.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers/properties/pgi/patternProperties/^.\*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-compiler_section.md))
