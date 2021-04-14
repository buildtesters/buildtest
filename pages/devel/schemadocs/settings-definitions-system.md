# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system
```



| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## system Type

`object` ([Details](settings-definitions-system.md))

# system Properties

| Property                                            | Type      | Required | Nullable       | Defined by                                                                                                                                                                        |
| :-------------------------------------------------- | :-------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [hostnames](#hostnames)                             | `array`   | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-hostnames.md "settings.schema.json#/definitions/system/properties/hostnames")                             |
| [description](#description)                         | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-description.md "settings.schema.json#/definitions/system/properties/description")                         |
| [buildspec_roots](#buildspec_roots)                 | `array`   | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-buildspec_roots.md "settings.schema.json#/definitions/system/properties/buildspec_roots")                 |
| [load_default_buildspecs](#load_default_buildspecs) | `boolean` | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-load_default_buildspecs.md "settings.schema.json#/definitions/system/properties/load_default_buildspecs") |
| [testdir](#testdir)                                 | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-testdir.md "settings.schema.json#/definitions/system/properties/testdir")                                 |
| [logdir](#logdir)                                   | `string`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-logdir.md "settings.schema.json#/definitions/system/properties/logdir")                                   |
| [moduletool](#moduletool)                           | `string`  | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-moduletool.md "settings.schema.json#/definitions/system/properties/moduletool")                           |
| [processor](#processor)                             | `object`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-processor.md "settings.schema.json#/definitions/system/properties/processor")                             |
| [compilers](#compilers)                             | `object`  | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers.md "settings.schema.json#/definitions/system/properties/compilers")                             |
| [executors](#executors)                             | `object`  | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-executors.md "settings.schema.json#/definitions/system/properties/executors")                             |
| [cdash](#cdash)                                     | `object`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-cdash.md "settings.schema.json#/definitions/system/properties/cdash")                                     |

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

## buildspec_roots

Specify a list of directory paths to search buildspecs. This field can be used with `buildtest buildspec find` to rebuild buildspec cache or build tests using `buildtest build` command

`buildspec_roots`

*   is optional

*   Type: `string[]`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-buildspec_roots.md "settings.schema.json#/definitions/system/properties/buildspec_roots")

### buildspec_roots Type

`string[]`

## load_default_buildspecs

Specify whether buildtest should automatically load  buildspecs provided in buildtest repo into buildspec cache

`load_default_buildspecs`

*   is required

*   Type: `boolean`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-load_default_buildspecs.md "settings.schema.json#/definitions/system/properties/load_default_buildspecs")

### load_default_buildspecs Type

`boolean`

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
