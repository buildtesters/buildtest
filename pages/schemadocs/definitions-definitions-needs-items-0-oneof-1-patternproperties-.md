# Untitled undefined type in JSON Schema Definitions File.  Schema

```txt
definitions.schema.json#/definitions/needs/items/0/oneOf/1/patternProperties/^.*$
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                         |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [definitions.schema.json\*](../out/definitions.schema.json "open original schema") |

## ^.\*$ Type

unknown

# ^.\*$ Properties

| Property                  | Type     | Required | Nullable       | Defined by                                                                                                                                                                         |
| :------------------------ | :------- | :------- | :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [state](#state)           | `string` | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-state.md "definitions.schema.json#/definitions/needs/items/0/oneOf/1/patternProperties/^.*$/properties/state")            |
| [returncode](#returncode) | Merged   | Optional | cannot be null | [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/needs/items/0/oneOf/1/patternProperties/^.*$/properties/returncode") |

## state

explicitly mark state of test regardless of status calculation

`state`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-state.md "definitions.schema.json#/definitions/needs/items/0/oneOf/1/patternProperties/^.*$/properties/state")

### state Type

`string`

### state Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"PASS"` |             |
| `"FAIL"` |             |

## returncode

Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array

`returncode`

*   is optional

*   Type: merged type ([Details](definitions-definitions-int_or_list.md))

*   cannot be null

*   defined in: [JSON Schema Definitions File. ](definitions-definitions-int_or_list.md "definitions.schema.json#/definitions/needs/items/0/oneOf/1/patternProperties/^.*$/properties/returncode")

### returncode Type

merged type ([Details](definitions-definitions-int_or_list.md))

one (and only one) of

*   [Untitled integer in JSON Schema Definitions File. ](definitions-definitions-int_or_list-oneof-0.md "check type definition")

*   [Untitled array in JSON Schema Definitions File. ](definitions-definitions-list_of_ints.md "check type definition")
