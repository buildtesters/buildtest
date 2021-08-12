# Untitled boolean in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/properties/skip
```

The `skip` is a boolean field that can be used to skip tests during builds. By default buildtest will build and run all tests in your buildspec file, if `skip: True` is set it will skip the buildspec.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## skip Type

`boolean`
