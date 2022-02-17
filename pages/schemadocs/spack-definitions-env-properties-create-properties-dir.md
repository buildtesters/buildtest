# Untitled string in spack schema version Schema

```txt
spack.schema.json#/definitions/env/properties/create/properties/dir
```

Create a spack environment in a specific directory. This will run `spack env create -d <dir>`. Directory path does not have to exist prior to execution however user must have appropriate ACL in-order to create directory.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## dir Type

`string`
