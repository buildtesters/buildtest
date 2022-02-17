# Untitled object in spack schema version Schema

```txt
spack.schema.json#/definitions/test/properties/run
```

Run tests using spack via `spack test run` command. This command requires specs are installed in your spack instance prior to running tests.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## run Type

`object` ([Details](spack-definitions-test-properties-run.md))

# run Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                                |
| :---------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [option](#option) | `string` | Optional | cannot be null | [spack schema version](spack-definitions-test-properties-run-properties-option.md "spack.schema.json#/definitions/test/properties/run/properties/option") |
| [specs](#specs)   | `array`  | Required | cannot be null | [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/test/properties/run/properties/specs")                  |

## option

Pass options to `spack test run`

`option`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version](spack-definitions-test-properties-run-properties-option.md "spack.schema.json#/definitions/test/properties/run/properties/option")

### option Type

`string`

## specs

List of specs to run tests by running `spack test run <specs>`.

`specs`

*   is required

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version](definitions-definitions-list_of_strings.md "spack.schema.json#/definitions/test/properties/run/properties/specs")

### specs Type

`string[]`

### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
