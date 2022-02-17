# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/executors/properties/local
```

The `local` section is used for declaring local executors for running jobs on local machine

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## local Type

`object` ([Details](settings-definitions-system-properties-executors-properties-local.md))

# local Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                              |
| :------- | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local.md "settings.schema.json#/definitions/system/properties/executors/properties/local/patternProperties/^.*$") |

## Pattern: `^.*$`

An instance object of local executor

`^.*$`

*   is optional

*   Type: `object` ([Details](settings-definitions-local.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-local.md "settings.schema.json#/definitions/system/properties/executors/properties/local/patternProperties/^.*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-local.md))
