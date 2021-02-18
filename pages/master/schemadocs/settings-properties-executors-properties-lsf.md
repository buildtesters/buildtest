# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/properties/executors/properties/lsf
```

The `lsf` section is used for declaring LSF executors for running jobs using LSF scheduler

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## lsf Type

`object` ([Details](settings-properties-executors-properties-lsf.md))

# lsf Properties

| Property | Type     | Required | Nullable       | Defined by                                                                                                                                       |
| :------- | :------- | :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| `^.*$`   | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf.md "settings.schema.json#/properties/executors/properties/lsf/patternProperties/^.*$") |

## Pattern: `^.*$`

An instance object of lsf executor

`^.*$`

*   is optional

*   Type: `object` ([Details](settings-definitions-lsf.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-lsf.md "settings.schema.json#/properties/executors/properties/lsf/patternProperties/^.\*$")

### ^.\*$ Type

`object` ([Details](settings-definitions-lsf.md))
