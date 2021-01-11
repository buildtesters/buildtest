# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers/properties/config
```

Specify compiler configuration based on named compilers.


| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## config Type

`object` ([Details](compiler-v1-properties-compilers-properties-config.md))

# undefined Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                                 |
| :------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration.md "compiler-v1.0.schema.json#/properties/compilers/properties/config/patternProperties/^.\*$") |

## Pattern: `^.*$`

Specify compiler configuration at compiler level. The `config` section has highest precedence when searching compiler configuration. This overrides fields found in compiler group and `all` property


`^.*$`

-   is optional
-   Type: `object` ([Details](compiler-v1-definitions-compiler_declaration.md))
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-definitions-compiler_declaration.md "compiler-v1.0.schema.json#/properties/compilers/properties/config/patternProperties/^.\*$")

### ^.\*$ Type

`object` ([Details](compiler-v1-definitions-compiler_declaration.md))
