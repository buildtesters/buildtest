# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/upcxx
```

Declaration of one or more UPCXX compilers.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## upcxx Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler-properties-upcxx.md))

# upcxx Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                                                             |
| :------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/upcxx/patternProperties/^.*$") |

## Pattern: `^.*$`

A compiler section is composed of `cc`, `cxx` and `fc` wrapper these are required when you need to specify compiler wrapper.

`^.*$`

*   is optional

*   Type: `object` ([Details](settings-definitions-compiler_section.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-compiler_section.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler/properties/upcxx/patternProperties/^.*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-compiler_section.md))
