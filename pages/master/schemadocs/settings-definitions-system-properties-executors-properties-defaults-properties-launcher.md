# Untitled string in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/launcher
```

Specify batch launcher to use when submitting jobs, this is applicable for LSF and Slurm Executors.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## launcher Type

`string`

## launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"sbatch"` |             |
| `"bsub"`   |             |
| `"qsub"`   |             |
