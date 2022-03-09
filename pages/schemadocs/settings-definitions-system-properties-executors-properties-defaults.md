# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/executors/properties/defaults
```

Specify default executor settings for all executors

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## defaults Type

`object` ([Details](settings-definitions-system-properties-executors-properties-defaults.md))

# defaults Properties

| Property                      | Type      | Required | Nullable       | Defined by                                                                                                                                                                                                                                    |
| :---------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [pollinterval](#pollinterval) | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-pollinterval.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/pollinterval") |
| [maxpendtime](#maxpendtime)   | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-maxpendtime.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/maxpendtime")   |
| [account](#account)           | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-account.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/account")           |
| [max\_jobs](#max_jobs)        | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-max_jobs.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/max_jobs")         |

## pollinterval

Specify poll interval in seconds after job submission, where buildtest will sleep and poll all jobs for job states. This field can be configured based on your preference. Excessive polling every few seconds can result in system degradation.

`pollinterval`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-pollinterval.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/pollinterval")

### pollinterval Type

`integer`

### pollinterval Constraints

**minimum**: the value of this number must greater than or equal to: `1`

### pollinterval Default Value

The default value is:

```json
30
```

## maxpendtime

Cancel job if it is still pending in queue beyond maxpendtime

`maxpendtime`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-maxpendtime.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/maxpendtime")

### maxpendtime Type

`integer`

### maxpendtime Constraints

**minimum**: the value of this number must greater than or equal to: `1`

### maxpendtime Default Value

The default value is:

```json
86400
```

## account

Specify Job Account for charging resources

`account`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-account.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/account")

### account Type

`string`

## max\_jobs

Maximum number of jobs that can be run at a given time for a particular executor

`max_jobs`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-executors-properties-defaults-properties-max_jobs.md "settings.schema.json#/definitions/system/properties/executors/properties/defaults/properties/max_jobs")

### max\_jobs Type

`integer`

### max\_jobs Constraints

**minimum**: the value of this number must greater than or equal to: `1`
