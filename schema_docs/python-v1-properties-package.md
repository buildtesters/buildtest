# Untitled object in python schema version 1.0 Schema

```txt
https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [python-v1.0.schema.json\*](../out/python-v1.0.schema.json "open original schema") |

## package Type

`object` ([Details](python-v1-properties-package.md))

# undefined Properties

| Property                      | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                     |
| :---------------------------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [requirements](#requirements) | `string` | Optional | cannot be null | [python schema version 1.0](python-v1-properties-package-properties-requirements.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package/properties/requirements") |
| [pypi](#pypi)                 | `array`  | Optional | cannot be null | [python schema version 1.0](python-v1-properties-package-properties-pypi.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package/properties/pypi")                 |

## requirements




`requirements`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-package-properties-requirements.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package/properties/requirements")

### requirements Type

`string`

## pypi




`pypi`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [python schema version 1.0](python-v1-properties-package-properties-pypi.md "https&#x3A;//buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package/properties/pypi")

### pypi Type

`string[]`

### pypi Constraints

**minimum number of items**: the minimum number of items for this array is: `1`
