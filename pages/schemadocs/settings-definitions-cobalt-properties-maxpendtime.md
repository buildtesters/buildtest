# Untitled integer in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/cobalt/properties/maxpendtime
```

Cancel job if it is still pending in queue beyond maxpendtime

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## maxpendtime Type

`integer`

## maxpendtime Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## maxpendtime Default Value

The default value is:

```json
86400
```
