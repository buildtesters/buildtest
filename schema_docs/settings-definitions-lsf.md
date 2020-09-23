# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## lsf Type

`object` ([Details](settings-definitions-lsf.md))

# undefined Properties

| Property                        | Type          | Required | Nullable       | Defined by                                                                                                                                                                                                    |
| :------------------------------ | ------------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [description](#description)     | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/description")     |
| [launcher](#launcher)           | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-launcher.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/launcher")           |
| [options](#options)             | `array`       | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-options.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options")             |
| [queue](#queue)                 | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-queue.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/queue")                 |
| [before_script](#before_script) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/before_script") |
| [after_script](#after_script)   | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/after_script")   |

## description

description field for documenting your executor


`description`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/description")

### description Type

`string`

## launcher

Specify the lsf batch scheduler to use. This overrides the default `launcher` field. It must be `bsub`. 


`launcher`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-launcher.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/launcher")

### launcher Type

`string`

### launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | ----------- |
| `"bsub"` |             |

## options

Specify any options for `bsub` for this executor when running all jobs associated to this executor


`options`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-options.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options")

### options Type

`string[]`

## queue

Specify the lsf queue you want to use `-q <queue>`


`queue`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-queue.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/queue")

### queue Type

`string`

## before_script




`before_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/before_script")

### before_script Type

unknown

## after_script




`after_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/after_script")

### after_script Type

unknown
