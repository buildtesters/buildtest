# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## config Type

`object` ([Details](settings-properties-config.md))

# undefined Properties

| Property          | Type     | Required | Nullable       | Defined by                                                                                                                                                                                          |
| :---------------- | -------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [editor](#editor) | `string` | Optional | cannot be null | [buildtest configuration schema](settings-properties-config-properties-editor.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/editor") |
| [paths](#paths)   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-properties-config-properties-paths.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths")   |

## editor

The editor field is used for opening buildspecs in an editor. The default editor is `vim`.


`editor`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-config-properties-editor.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/editor")

### editor Type

`string`

### editor Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | ----------- |
| `"vi"`    |             |
| `"vim"`   |             |
| `"nano"`  |             |
| `"emacs"` |             |

### editor Default Value

The default value is:

```json
"vim"
```

## paths




`paths`

-   is optional
-   Type: `object` ([Details](settings-properties-config-properties-paths.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-config-properties-paths.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths")

### paths Type

`object` ([Details](settings-properties-config-properties-paths.md))
