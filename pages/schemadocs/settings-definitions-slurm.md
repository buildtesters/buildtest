# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/slurm
```

An instance object of slurm executor

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## slurm Type

`object` ([Details](settings-definitions-slurm.md))

# slurm Properties

| Property                         | Type          | Required | Nullable       | Defined by                                                                                                                                                  |
| :------------------------------- | :------------ | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [description](#description)      | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-description.md "settings.schema.json#/definitions/slurm/properties/description")     |
| [launcher](#launcher)            | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-launcher.md "settings.schema.json#/definitions/slurm/properties/launcher")           |
| [options](#options)              | `array`       | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-options.md "settings.schema.json#/definitions/slurm/properties/options")             |
| [cluster](#cluster)              | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-cluster.md "settings.schema.json#/definitions/slurm/properties/cluster")             |
| [partition](#partition)          | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-partition.md "settings.schema.json#/definitions/slurm/properties/partition")         |
| [qos](#qos)                      | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-qos.md "settings.schema.json#/definitions/slurm/properties/qos")                     |
| [before\_script](#before_script) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-before_script.md "settings.schema.json#/definitions/slurm/properties/before_script") |
| [maxpendtime](#maxpendtime)      | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-maxpendtime.md "settings.schema.json#/definitions/slurm/properties/maxpendtime")                      |
| [account](#account)              | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-account.md "settings.schema.json#/definitions/slurm/properties/account")                              |
| [max\_jobs](#max_jobs)           | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-max_jobs.md "settings.schema.json#/definitions/slurm/properties/max_jobs")                            |
| [disable](#disable)              | `boolean`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-disable.md "settings.schema.json#/definitions/slurm/properties/disable")                              |
| [module](#module)                | `object`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/slurm/properties/module")                                |

## description

description field for documenting your executor

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-description.md "settings.schema.json#/definitions/slurm/properties/description")

### description Type

`string`

## launcher

Specify the slurm batch scheduler to use. This overrides the default `launcher` field. This must be `sbatch`.

`launcher`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-launcher.md "settings.schema.json#/definitions/slurm/properties/launcher")

### launcher Type

`string`

### launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | :---------- |
| `"sbatch"` |             |

## options

Specify any other options for `sbatch` used by this executor for running all jobs.

`options`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-options.md "settings.schema.json#/definitions/slurm/properties/options")

### options Type

`string[]`

## cluster

Specify the slurm cluster you want to use `-M <cluster>`

`cluster`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-cluster.md "settings.schema.json#/definitions/slurm/properties/cluster")

### cluster Type

`string`

## partition

Specify the slurm partition you want to use `-p <partition>`

`partition`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-partition.md "settings.schema.json#/definitions/slurm/properties/partition")

### partition Type

`string`

## qos

Specify the slurm qos you want to use `-q <qos>`

`qos`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-qos.md "settings.schema.json#/definitions/slurm/properties/qos")

### qos Type

`string`

## before\_script

The `before_script` section can be used to specify commands before start of test. The script will be sourced in active shell.

`before_script`

*   is optional

*   Type: unknown

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-before_script.md "settings.schema.json#/definitions/slurm/properties/before_script")

### before\_script Type

unknown

## maxpendtime

Cancel job if it is still pending in queue beyond maxpendtime

`maxpendtime`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-maxpendtime.md "settings.schema.json#/definitions/slurm/properties/maxpendtime")

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

*   defined in: [buildtest configuration schema](settings-definitions-account.md "settings.schema.json#/definitions/slurm/properties/account")

### account Type

`string`

## max\_jobs

Maximum number of jobs that can be run at a given time for a particular executor

`max_jobs`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-max_jobs.md "settings.schema.json#/definitions/slurm/properties/max_jobs")

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

*   defined in: [buildtest configuration schema](settings-definitions-disable.md "settings.schema.json#/definitions/slurm/properties/disable")

### disable Type

`boolean`

## module



`module`

*   is optional

*   Type: `object` ([Details](settings-definitions-module.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-module.md "settings.schema.json#/definitions/slurm/properties/module")

### module Type

`object` ([Details](settings-definitions-module.md))
