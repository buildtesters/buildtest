# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/env/properties/create
```

Create a spack environment via `spack env create`

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## create Type

`object` ([Details](spack-definitions-env-properties-create.md))

# create Properties

| Property                                   | Type      | Required | Nullable       | Defined by                                                                                                                                                                            |
| :----------------------------------------- | :-------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [remove\_environment](#remove_environment) | `boolean` | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create-properties-remove_environment.md "spack.schema.json#/definitions/env/properties/create/properties/remove_environment") |
| [name](#name)                              | `string`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create-properties-name.md "spack.schema.json#/definitions/env/properties/create/properties/name")                             |
| [manifest](#manifest)                      | `string`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create-properties-manifest.md "spack.schema.json#/definitions/env/properties/create/properties/manifest")                     |
| [options](#options)                        | `string`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create-properties-options.md "spack.schema.json#/definitions/env/properties/create/properties/options")                       |
| [dir](#dir)                                | `string`  | Optional | cannot be null | [spack schema version](spack-definitions-env-properties-create-properties-dir.md "spack.schema.json#/definitions/env/properties/create/properties/dir")                               |

## remove\_environment

Remove existing spack environment before creating new environment. If set to `True` we will run `spack env rm -y <name>`.

`remove_environment`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create-properties-remove_environment.md "spack.schema.json#/definitions/env/properties/create/properties/remove_environment")

### remove\_environment Type

`boolean`

## name

Name of spack environment to create

`name`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create-properties-name.md "spack.schema.json#/definitions/env/properties/create/properties/name")

### name Type

`string`

## manifest

Specify path to spack manifest file (`spack.yaml` or `spack.lock`) when creating environment

`manifest`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create-properties-manifest.md "spack.schema.json#/definitions/env/properties/create/properties/manifest")

### manifest Type

`string`

## options

Pass options to `spack env create` command

`options`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create-properties-options.md "spack.schema.json#/definitions/env/properties/create/properties/options")

### options Type

`string`

## dir

Create a spack environment in a specific directory. This will run `spack env create -d <dir>`. Directory path does not have to exist prior to execution however user must have appropriate ACL in-order to create directory.

`dir`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-create-properties-dir.md "spack.schema.json#/definitions/env/properties/create/properties/dir")

### dir Type

`string`
