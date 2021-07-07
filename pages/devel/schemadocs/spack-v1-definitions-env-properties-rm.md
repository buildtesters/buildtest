# Untitled object in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/definitions/env/properties/rm
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## rm Type

`object` ([Details](spack-v1-definitions-env-properties-rm.md))

# rm Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                                    |
| :------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [name](#name) | `string` | Required | cannot be null | [spack schema version 1.0](spack-v1-definitions-env-properties-rm-properties-name.md "spack-v1.0.schema.json#/definitions/env/properties/rm/properties/name") |

## name

Remove spack environment by name. This will run `spack env rm -y <name>`.

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version 1.0](spack-v1-definitions-env-properties-rm-properties-name.md "spack-v1.0.schema.json#/definitions/env/properties/rm/properties/name")

### name Type

`string`
