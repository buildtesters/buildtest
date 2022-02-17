# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/executors/properties/pbs
```

The `pbs` section is used for declaring PBS executors for running jobs using PBS scheduler

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## pbs Type

`object` ([Details](settings-definitions-system-properties-executors-properties-pbs.md))

# pbs Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                                          |
| :------- | :------- | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-pbs.md "settings.schema.json#/definitions/system/properties/executors/properties/pbs/patternProperties/^.*$") |

## Pattern: `^.*$`

An instance object of cobalt executor

`^.*$`

*   is optional

*   Type: `object` ([Details](settings-definitions-pbs.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-pbs.md "settings.schema.json#/definitions/system/properties/executors/properties/pbs/patternProperties/^.*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-pbs.md))
