# Untitled boolean in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/definitions/test/properties/remove_tests
```

Remove all test suites in spack before running test via `spack test run`. If set to `True` we will run `spack test remove -y` which will remove all test suites.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## remove_tests Type

`boolean`
