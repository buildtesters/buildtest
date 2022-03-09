# Untitled integer in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/pollinterval
```

Specify poll interval in seconds after job submission, where buildtest will sleep and poll all jobs for job states. This field can be configured based on your preference. Excessive polling every few seconds can result in system degradation.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## pollinterval Type

`integer`

## pollinterval Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## pollinterval Default Value

The default value is:

```json
30
```
