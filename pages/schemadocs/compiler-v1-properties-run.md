# Untitled object in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/run
```

The `run` section is used for specifying launch configuration of executable


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## run Type

`object` ([Details](compiler-v1-properties-run.md))

# undefined Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                       |
| :-------------------- | -------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| [launcher](#launcher) | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-run-properties-launcher.md "compiler-v1.0.schema.json#/properties/run/properties/launcher") |
| [args](#args)         | `string` | Optional | cannot be null | [compiler schema version 1.0](compiler-v1-properties-run-properties-args.md "compiler-v1.0.schema.json#/properties/run/properties/args")         |

## launcher

The `launcher` field is inserted before the executable. This can be used when running programs with `mpirun`, `mpiexec`, `srun`, etc... You may specify launcher options with this field


`launcher`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-run-properties-launcher.md "compiler-v1.0.schema.json#/properties/run/properties/launcher")

### launcher Type

`string`

## args

The `args` field is used to specify arguments to executable.


`args`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [compiler schema version 1.0](compiler-v1-properties-run-properties-args.md "compiler-v1.0.schema.json#/properties/run/properties/args")

### args Type

`string`
