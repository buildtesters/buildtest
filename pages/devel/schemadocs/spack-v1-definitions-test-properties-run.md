# Untitled object in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/definitions/test/properties/run
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## run Type

`object` ([Details](spack-v1-definitions-test-properties-run.md))

# run Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                                            |
| :---------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [option](#option) | `string` | Optional | cannot be null | [spack schema version 1.0](spack-v1-definitions-test-properties-run-properties-option.md "spack-v1.0.schema.json#/definitions/test/properties/run/properties/option") |
| [specs](#specs)   | `array`  | Required | cannot be null | [spack schema version 1.0](definitions-definitions-list_of_strings.md "spack-v1.0.schema.json#/definitions/test/properties/run/properties/specs")                     |

## option

Options passed to `spack test run`

`option`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version 1.0](spack-v1-definitions-test-properties-run-properties-option.md "spack-v1.0.schema.json#/definitions/test/properties/run/properties/option")

### option Type

`string`

## specs

List of specs to run tests by running `spack test run <specs>`.

`specs`

*   is required

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version 1.0](definitions-definitions-list_of_strings.md "spack-v1.0.schema.json#/definitions/test/properties/run/properties/specs")

### specs Type

`string[]`

### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
