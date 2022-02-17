# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/env/properties/activate
```

Activate a spack environment via `spack env activate`

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## activate Type

`object` ([Details](spack-definitions-env-properties-activate.md))

# activate Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                          |
| :------------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [name](#name)       | `string` | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-activate-properties-name.md "spack.schema.json#/definitions/env/properties/activate/properties/name")       |
| [options](#options) | `string` | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-activate-properties-options.md "spack.schema.json#/definitions/env/properties/activate/properties/options") |
| [dir](#dir)         | `string` | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-activate-properties-dir.md "spack.schema.json#/definitions/env/properties/activate/properties/dir")         |

## name

Name of spack environment to activate. In order to activate spack environment `my-project` you need to run `spack env activate my-project` which is specified by `name: my-project`.

`name`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-activate-properties-name.md "spack.schema.json#/definitions/env/properties/activate/properties/name")

### name Type

`string`

## options

Pass options to `spack env activate` command

`options`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-activate-properties-options.md "spack.schema.json#/definitions/env/properties/activate/properties/options")

### options Type

`string`

## dir

Activate spack environment from directory.

`dir`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-activate-properties-dir.md "spack.schema.json#/definitions/env/properties/activate/properties/dir")

### dir Type

`string`
