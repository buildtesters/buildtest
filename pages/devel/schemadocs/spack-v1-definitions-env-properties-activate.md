# Untitled object in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/definitions/env/properties/activate
```

Activate a spack environment via `spack env activate`

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## activate Type

`object` ([Details](spack-v1-definitions-env-properties-activate.md))

# activate Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                                      |
| :------------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [name](#name)       | `string` | Optional | cannot be null | [spack schema version 1.0](spack-v1-definitions-env-properties-activate-properties-name.md "spack-v1.0.schema.json#/definitions/env/properties/activate/properties/name")       |
| [options](#options) | `string` | Optional | cannot be null | [spack schema version 1.0](spack-v1-definitions-env-properties-activate-properties-options.md "spack-v1.0.schema.json#/definitions/env/properties/activate/properties/options") |
| [dir](#dir)         | `string` | Optional | cannot be null | [spack schema version 1.0](spack-v1-definitions-env-properties-activate-properties-dir.md "spack-v1.0.schema.json#/definitions/env/properties/activate/properties/dir")         |

## name

Name of spack environment to activate.

`name`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version 1.0](spack-v1-definitions-env-properties-activate-properties-name.md "spack-v1.0.schema.json#/definitions/env/properties/activate/properties/name")

### name Type

`string`

## options

Options passed to `spack env activate`

`options`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version 1.0](spack-v1-definitions-env-properties-activate-properties-options.md "spack-v1.0.schema.json#/definitions/env/properties/activate/properties/options")

### options Type

`string`

## dir

Activate spack environment from directory.

`dir`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version 1.0](spack-v1-definitions-env-properties-activate-properties-dir.md "spack-v1.0.schema.json#/definitions/env/properties/activate/properties/dir")

### dir Type

`string`
