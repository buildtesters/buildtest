# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## system Type

`object` ([Details](settings-definitions-system.md))

# system Properties

| Property                             | Type      | Required | Nullable       | Defined by                                                                                                                                                        |
| :----------------------------------- | :-------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [hostnames](#hostnames)              | `array`   | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-hostnames.md "settings.schema.json#/definitions/system/properties/hostnames")             |
| [description](#description)          | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-description.md "settings.schema.json#/definitions/system/properties/description")         |
| [numprocs](#numprocs)                | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-numprocs.md "settings.schema.json#/definitions/system/properties/numprocs")               |
| [buildspec\_roots](#buildspec_roots) | `array`   | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-buildspec_roots.md "settings.schema.json#/definitions/system/properties/buildspec_roots") |
| [testdir](#testdir)                  | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-testdir.md "settings.schema.json#/definitions/system/properties/testdir")                 |
| [logdir](#logdir)                    | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-logdir.md "settings.schema.json#/definitions/system/properties/logdir")                   |
| [moduletool](#moduletool)            | `string`  | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-moduletool.md "settings.schema.json#/definitions/system/properties/moduletool")           |
| [timeout](#timeout)                  | `integer` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-timeout.md "settings.schema.json#/definitions/system/properties/timeout")                 |
| [processor](#processor)              | `object`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor.md "settings.schema.json#/definitions/system/properties/processor")             |
| [compilers](#compilers)              | `object`  | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers.md "settings.schema.json#/definitions/system/properties/compilers")             |
| [executors](#executors)              | `object`  | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-executors.md "settings.schema.json#/definitions/system/properties/executors")             |
| [cdash](#cdash)                      | `object`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-cdash.md "settings.schema.json#/definitions/system/properties/cdash")                     |

## hostnames

Specify a list of hostnames to check where buildtest can run for the given system record

`hostnames`

*   is required

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-hostnames.md "settings.schema.json#/definitions/system/properties/hostnames")

### hostnames Type

`string[]`

## description

system description field

`description`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-description.md "settings.schema.json#/definitions/system/properties/description")

### description Type

`string`

## numprocs

Specify size of Process Pool for parallel processing

`numprocs`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-numprocs.md "settings.schema.json#/definitions/system/properties/numprocs")

### numprocs Type

`integer`

### numprocs Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## buildspec\_roots

Specify a list of directory paths to search buildspecs. This field can be used with `buildtest buildspec find` to rebuild buildspec cache or build tests using `buildtest build` command

`buildspec_roots`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-buildspec_roots.md "settings.schema.json#/definitions/system/properties/buildspec_roots")

### buildspec\_roots Type

`string[]`

## testdir

Specify full path to test directory where buildtest will write tests.

`testdir`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-testdir.md "settings.schema.json#/definitions/system/properties/testdir")

### testdir Type

`string`

## logdir

Specify location where buildtest will write log files

`logdir`

*   is optional

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-logdir.md "settings.schema.json#/definitions/system/properties/logdir")

### logdir Type

`string`

## moduletool

Specify modules tool used for interacting with `module` command.

`moduletool`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-moduletool.md "settings.schema.json#/definitions/system/properties/moduletool")

### moduletool Type

`string`

### moduletool Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value                   | Explanation |
| :---------------------- | :---------- |
| `"environment-modules"` |             |
| `"lmod"`                |             |
| `"N/A"`                 |             |

## timeout

Specify timeout duration in number of seconds

`timeout`

*   is optional

*   Type: `integer`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-timeout.md "settings.schema.json#/definitions/system/properties/timeout")

### timeout Type

`integer`

### timeout Constraints

**minimum**: the value of this number must greater than or equal to: `1`

## processor

Specify processor information

`processor`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-processor.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-processor.md "settings.schema.json#/definitions/system/properties/processor")

### processor Type

`object` ([Details](settings-definitions-system-properties-processor.md))

## compilers

Declare compiler section for defining system compilers that can be referenced in buildspec.

`compilers`

*   is required

*   Type: `object` ([Details](settings-definitions-system-properties-compilers.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers.md "settings.schema.json#/definitions/system/properties/compilers")

### compilers Type

`object` ([Details](settings-definitions-system-properties-compilers.md))

## executors

The executor section is used for declaring your executors that are responsible for running jobs. The executor section can be `local`, `lsf`, `slurm`, `cobalt`. The executors are referenced in buildspec using `executor` field.

`executors`

*   is required

*   Type: `object` ([Details](settings-definitions-system-properties-executors.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-executors.md "settings.schema.json#/definitions/system/properties/executors")

### executors Type

`object` ([Details](settings-definitions-system-properties-executors.md))

## cdash

Specify CDASH configuration used to upload tests via 'buildtest cdash' command

`cdash`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-cdash.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-cdash.md "settings.schema.json#/definitions/system/properties/cdash")

### cdash Type

`object` ([Details](settings-definitions-system-properties-cdash.md))
