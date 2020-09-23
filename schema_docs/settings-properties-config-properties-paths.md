# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## paths Type

`object` ([Details](settings-properties-config-properties-paths.md))

# undefined Properties

| Property                            | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                                                              |
| :---------------------------------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [buildspec_roots](#buildspec_roots) | `array`  | Optional | cannot be null | [buildtest configuration schema](settings-properties-config-properties-paths-properties-buildspec_roots.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/buildspec_roots") |
| [prefix](#prefix)                   | `string` | Optional | cannot be null | [buildtest configuration schema](settings-properties-config-properties-paths-properties-prefix.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/prefix")                   |
| [logdir](#logdir)                   | `string` | Optional | cannot be null | [buildtest configuration schema](settings-properties-config-properties-paths-properties-logdir.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/logdir")                   |
| [testdir](#testdir)                 | `string` | Optional | cannot be null | [buildtest configuration schema](settings-properties-config-properties-paths-properties-testdir.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/testdir")                 |

## buildspec_roots

Specify a list of directory paths to search buildspecs. This field can be used with `buildtest buildspec find` to rebuild buildspec cache or build tests using `buildtest build` command


`buildspec_roots`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-config-properties-paths-properties-buildspec_roots.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/buildspec_roots")

### buildspec_roots Type

`string[]`

## prefix




`prefix`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-config-properties-paths-properties-prefix.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/prefix")

### prefix Type

`string`

## logdir




`logdir`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-config-properties-paths-properties-logdir.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/logdir")

### logdir Type

`string`

## testdir




`testdir`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-config-properties-paths-properties-testdir.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/testdir")

### testdir Type

`string`
