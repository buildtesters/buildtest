# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/pbs
```

An instance object of cobalt executor

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## pbs Type

`object` ([Details](settings-definitions-pbs.md))

# pbs Properties

| Property                         | Type          | Required | Nullable       | Defined by                                                                                                                                              |
| :------------------------------- | :------------ | :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [description](#description)      | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-pbs-properties-description.md "settings.schema.json#/definitions/pbs/properties/description")     |
| [launcher](#launcher)            | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-pbs-properties-launcher.md "settings.schema.json#/definitions/pbs/properties/launcher")           |
| [options](#options)              | `array`       | Optional | cannot be null | [buildtest configuration schema](settings-definitions-pbs-properties-options.md "settings.schema.json#/definitions/pbs/properties/options")             |
| [queue](#queue)                  | `string`      | Required | cannot be null | [buildtest configuration schema](settings-definitions-pbs-properties-queue.md "settings.schema.json#/definitions/pbs/properties/queue")                 |
| [before\_script](#before_script) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-pbs-properties-before_script.md "settings.schema.json#/definitions/pbs/properties/before_script") |
| [maxpendtime](#maxpendtime)      | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-maxpendtime.md "settings.schema.json#/definitions/pbs/properties/maxpendtime")                    |
| [account](#account)              | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-account.md "settings.schema.json#/definitions/pbs/properties/account")                            |
| [max\_jobs](#max_jobs)           | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-max_jobs.md "settings.schema.json#/definitions/pbs/properties/max_jobs")                          |
| [disable](#disable)              | `boolean`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-disable.md "settings.schema.json#/definitions/pbs/properties/disable")                            |
| [module](#module)                | `object`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/pbs/properties/module")                              |

## description

description field for documenting your executor

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-pbs-properties-description.md "settings.schema.json#/definitions/pbs/properties/description")

### description Type

`string`

## launcher

Specify the pbs batch scheduler to use. This overrides the default `launcher` field. It must be `qsub`.

`launcher`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-pbs-properties-launcher.md "settings.schema.json#/definitions/pbs/properties/launcher")

### launcher Type

`string`

### launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | :---------- |
| `"qsub"` |             |

## options

Specify any options for `qsub` for this executor when running all jobs associated to this executor

`options`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-pbs-properties-options.md "settings.schema.json#/definitions/pbs/properties/options")

### options Type

`string[]`

## queue

Specify the lsf queue you want to use `-q <queue>`

`queue`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-pbs-properties-queue.md "settings.schema.json#/definitions/pbs/properties/queue")

### queue Type

`string`

## before\_script

The `before_script` section can be used to specify commands before start of test. The script will be sourced in active shell.

`before_script`

*   is optional

*   Type: unknown

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-pbs-properties-before_script.md "settings.schema.json#/definitions/pbs/properties/before_script")

### before\_script Type

unknown

## maxpendtime

Cancel job if it is still pending in queue beyond maxpendtime

`maxpendtime`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-maxpendtime.md "settings.schema.json#/definitions/pbs/properties/maxpendtime")

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

*   defined in: [buildtest configuration schema](settings-definitions-account.md "settings.schema.json#/definitions/pbs/properties/account")

### account Type

`string`

## max\_jobs

Maximum number of jobs that can be run at a given time for a particular executor

`max_jobs`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-max_jobs.md "settings.schema.json#/definitions/pbs/properties/max_jobs")

### max\_jobs Type

`integer`

### max\_jobs Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## disable

Disable executor

`disable`

*   is optional

*   Type: `boolean`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-disable.md "settings.schema.json#/definitions/pbs/properties/disable")

### disable Type

`boolean`

## module



`module`

*   is optional

*   Type: `object` ([Details](settings-definitions-module.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/pbs/properties/module")

### module Type

`object` ([Details](settings-definitions-module.md))
