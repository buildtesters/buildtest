# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/test/properties/results
```

View test results via `spack test results` after running tests via `spack test run`. Results can be viewed using suitename or installed specs or both.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                            |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json*](../out/spack.schema.json "open original schema") |

## results Type

`object` ([Details](spack-definitions-test-properties-results.md))

any of

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-0.md "check type definition")

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-1.md "check type definition")

*   [Untitled undefined type in spack schema version](spack-definitions-test-properties-results-anyof-2.md "check type definition")

# results Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                                        |
| :---------------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [option](#option) | `string` | Optional | cannot be null | [spack schema version](spack-definitions-test-properties-results-properties-option.md "spack.schema.json#/definitions/test/properties/results/properties/option") |
| [suite](#suite)   | `array`  | Optional | cannot be null | [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/test/properties/results/properties/suite")                      |
| [specs](#specs)   | `array`  | Optional | cannot be null | [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/test/properties/results/properties/specs")                      |

## option

Pass options to `spack test results`

`option`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-results-properties-option.md "spack.schema.json#/definitions/test/properties/results/properties/option")

### option Type

`string`

## suite

Report results by  suite name by running `spack test results <suite>`.

`suite`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/test/properties/results/properties/suite")

### suite Type

`string[]`

### suite Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## specs

Report result by spec name by running `spack test run -- <specs>`.

`specs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/test/properties/results/properties/specs")

### specs Type

`string[]`

### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
