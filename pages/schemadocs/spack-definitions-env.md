# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/env
```

Used for managing spack environment using `spack env` command.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## env Type

`object` ([Details](spack-definitions-env.md))

# env Properties

| Property                  | Type      | Required | Nullable       | Defined by                                                                                                                        |
| :------------------------ | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| [create](#create)         | `object`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create.md "spack.schema.json#/definitions/env/properties/create")         |
| [activate](#activate)     | `object`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-activate.md "spack.schema.json#/definitions/env/properties/activate")     |
| [rm](#rm)                 | `object`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-rm.md "spack.schema.json#/definitions/env/properties/rm")                 |
| [mirror](#mirror)         | `object`  | Optional | cannot be null | [spack schema version](definitions-definitions-env.md "spack.schema.json#/definitions/env/properties/mirror")                     |
| [specs](#specs)           | `array`   | Optional | cannot be null | [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/env/properties/specs")          |
| [concretize](#concretize) | `boolean` | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-concretize.md "spack.schema.json#/definitions/env/properties/concretize") |

## create

Create a spack environment via `spack env create`

`create`

*   is optional

*   Type: `object` ([Details](spack-definitions-env-properties-create.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create.md "spack.schema.json#/definitions/env/properties/create")

### create Type

`object` ([Details](spack-definitions-env-properties-create.md))

## activate

Activate a spack environment via `spack env activate`

`activate`

*   is optional

*   Type: `object` ([Details](spack-definitions-env-properties-activate.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-activate.md "spack.schema.json#/definitions/env/properties/activate")

### activate Type

`object` ([Details](spack-definitions-env-properties-activate.md))

## rm

Remove an existing spack environment via `spack env rm`.

`rm`

*   is optional

*   Type: `object` ([Details](spack-definitions-env-properties-rm.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-rm.md "spack.schema.json#/definitions/env/properties/rm")

### rm Type

`object` ([Details](spack-definitions-env-properties-rm.md))

## mirror

One or more key value pairs for an environment (key=value)

`mirror`

*   is optional

*   Type: `object` ([Details](definitions-definitions-env.md))

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-env.md "spack.schema.json#/definitions/env/properties/mirror")

### mirror Type

`object` ([Details](definitions-definitions-env.md))

### mirror Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

## specs

Add specs to environment by running `spack add <specs>`. The `specs` is a list of string which expect the argument to be name of spack package.

`specs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/env/properties/specs")

### specs Type

`string[]`

### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## concretize

If `concretize: true` is set, we will concretize spack environment by running `spack concretize -f` otherwise this line will be ignored.

`concretize`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-concretize.md "spack.schema.json#/definitions/env/properties/concretize")

### concretize Type

`boolean`
