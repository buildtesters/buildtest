# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/test
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json*](../out/spack.schema.json "open original schema") |

## test Type

`object` ([Details](spack-definitions-test.md))

# test Properties

| Property                      | Type      | Required | Nullable       | Defined by                                                                                                                              |
| :---------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| [remove_tests](#remove_tests) | `boolean` | Optional | cannot be null | [spack schema version](spack-definitions-test-properties-remove_tests.md "spack.schema.json#/definitions/test/properties/remove_tests") |
| [run](#run)                   | `object`  | Required | cannot be null | [spack schema version](spack-definitions-test-properties-run.md "spack.schema.json#/definitions/test/properties/run")                   |
| [results](#results)           | Merged    | Required | cannot be null | [spack schema version](spack-definitions-test-properties-results.md "spack.schema.json#/definitions/test/properties/results")           |

## remove_tests

Remove all test suites in spack before running test via `spack test run`. If set to `True` we will run `spack test remove -y` which will remove all test suites.

`remove_tests`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-remove_tests.md "spack.schema.json#/definitions/test/properties/remove_tests")

### remove_tests Type

`boolean`

## run

Run tests using spack via `spack test run` command. This command requires specs are installed in your spack instance prior to running tests.

`run`

*   is required

*   Type: `object` ([Details](spack-definitions-test-properties-run.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-run.md "spack.schema.json#/definitions/test/properties/run")

### run Type

`object` ([Details](spack-definitions-test-properties-run.md))

## results

View test results via `spack test results` after running tests via `spack test run`. Results can be viewed using suitename or installed specs or both.

`results`

*   is required

*   Type: `object` ([Details](spack-definitions-test-properties-results.md))

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-results.md "spack.schema.json#/definitions/test/properties/results")

### results Type

`object` ([Details](spack-definitions-test-properties-results.md))

any of

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-0.md "check type definition")

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-1.md "check type definition")

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-2.md "check type definition")
