# Untitled integer in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/slurm/properties/max_pend_time
```

Cancel job if it is still pending in queue beyond max_pend_time

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## max_pend_time Type

`integer`

## max_pend_time Constraints

**minimum**: the value of this number must greater than or equal to: `10`

## max_pend_time Default Value

The default value is:

```json
90
```
