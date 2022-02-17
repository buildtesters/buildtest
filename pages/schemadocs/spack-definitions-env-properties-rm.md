# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/env/properties/rm
```

Remove an existing spack environment via `spack env rm`.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## rm Type

`object` ([Details](spack-definitions-env-properties-rm.md))

# rm Properties

| Property      | Type     | Required | Nullable       | Defined by                                                                                                                                        |
| :------------ | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| [name](#name) | `string` | Required | cannot be null | [spack schema version](spack-definitions-env-properties-rm-properties-name.md "spack.schema.json#/definitions/env/properties/rm/properties/name") |

## name

Remove spack environment by name. This will run `spack env rm -y <name>`.

`name`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-env-properties-rm-properties-name.md "spack.schema.json#/definitions/env/properties/rm/properties/name")

### name Type

`string`
