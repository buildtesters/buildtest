# Untitled object in compiler schema Schema

```txt
compiler.schema.json#/properties/compilers/properties/config
```

Specify compiler configuration based on named compilers.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [compiler.schema.json\*](../out/compiler.schema.json "open original schema") |

## config Type

`object` ([Details](compiler-properties-compilers-properties-config.md))

# config Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                            |
| :------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [compiler schema](compiler-definitions-compiler_declaration.md "compiler.schema.json#/properties/compilers/properties/config/patternProperties/^.*$") |

## Pattern: `^.*$`

Specify compiler configuration at compiler level. The `config` section has highest precedence when searching compiler configuration. This overrides fields found in compiler group and `all` property

`^.*$`

*   is optional

*   Type: `object` ([Details](compiler-definitions-compiler_declaration.md))

*   cannot be null

*   defined in: [compiler schema](compiler-definitions-compiler_declaration.md "compiler.schema.json#/properties/compilers/properties/config/patternProperties/^.*$")

### ^.\*$ Type

`object` ([Details](compiler-definitions-compiler_declaration.md))
