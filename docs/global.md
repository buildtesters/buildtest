# global schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/global.schema.json
```

buildtest global schema is validated for all buildspecs. The global schema defines top-level structure of buildspec and defintions that are inherited for sub-schemas


| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [global.schema.json](../out/global.schema.json "open original schema") |

## global schema Type

`object` ([global schema](global.md))

# global schema Properties

| Property                    | Type     | Required | Nullable       | Defined by                                                                                                                                           |
| :-------------------------- | -------- | -------- | -------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| [version](#version)         | `string` | Required | cannot be null | [global schema](global-properties-version.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/version")         |
| [maintainers](#maintainers) | `array`  | Optional | cannot be null | [global schema](global-properties-maintainers.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/maintainers") |
| [buildspecs](#buildspecs)   | `object` | Required | cannot be null | [global schema](global-properties-buildspecs.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/buildspecs")   |

## version

The semver version of the schema to use (x.x).


`version`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [global schema](global-properties-version.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/version")

### version Type

`string`

## maintainers

One or more maintainers or aliases


`maintainers`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [global schema](global-properties-maintainers.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/maintainers")

### maintainers Type

`string[]`

### maintainers Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## buildspecs

This section is used to define one or more tests (buildspecs). Each test must be unique name


`buildspecs`

-   is required
-   Type: `object` ([Details](global-properties-buildspecs.md))
-   cannot be null
-   defined in: [global schema](global-properties-buildspecs.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/buildspecs")

### buildspecs Type

`object` ([Details](global-properties-buildspecs.md))
