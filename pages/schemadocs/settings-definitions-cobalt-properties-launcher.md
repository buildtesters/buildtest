# Untitled string in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/cobalt/properties/launcher
```

Specify the cobalt batch scheduler to use. This overrides the default `launcher` field. It must be `qsub`.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## launcher Type

`string`

## launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"qsub"` |             |
