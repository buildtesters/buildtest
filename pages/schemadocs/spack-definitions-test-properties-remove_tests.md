# Untitled boolean in spack schema version Schema

```txt
spack.schema.json#/definitions/test/properties/remove_tests
```

Remove all test suites in spack before running test via `spack test run`. If set to `True` we will run `spack test remove -y` which will remove all test suites.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## remove\_tests Type

`boolean`
