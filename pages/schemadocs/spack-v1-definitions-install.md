# Untitled object in spack schema version 1.0 Schema

```txt
spack-v1.0.schema.json#/definitions/install
```

Install spack packages using `spack install` command

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                      |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :------------------------------------------------------------------------------ |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [spack-v1.0.schema.json*](../out/spack-v1.0.schema.json "open original schema") |

## install Type

`object` ([Details](spack-v1-definitions-install.md))

# install Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                      |
| :------------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| [options](#options) | `string` | Optional | cannot be null | [spack schema version 1.0](spack-v1-definitions-install-properties-options.md "spack-v1.0.schema.json#/definitions/install/properties/options") |
| [specs](#specs)     | `array`  | Optional | cannot be null | [spack schema version 1.0](definitions-definitions-list_of_strings.md "spack-v1.0.schema.json#/definitions/install/properties/specs")           |

## options

Pass options to `spack install` command

`options`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [spack schema version 1.0](spack-v1-definitions-install-properties-options.md "spack-v1.0.schema.json#/definitions/install/properties/options")

### options Type

`string`

## specs

List of specs to install using `spack install` command

`specs`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [spack schema version 1.0](definitions-definitions-list_of_strings.md "spack-v1.0.schema.json#/definitions/install/properties/specs")

### specs Type

`string[]`

### specs Constraints

**minimum number of items**: the minimum number of items for this array is: `1`

**unique items**: all items in this array must be unique. Duplicates are not allowed.
