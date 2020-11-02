# buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                 |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------- |
| Can be instantiated | Yes        | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json](../out/settings.schema.json "open original schema") |

## buildtest configuration schema Type

`object` ([buildtest configuration schema](settings.md))

# buildtest configuration schema Properties

| Property                                      | Type          | Required | Nullable       | Defined by                                                                                                                                                                        |
| :-------------------------------------------- | ------------- | -------- | -------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [editor](#editor)                             | `string`      | Required | cannot be null | [buildtest configuration schema](settings-properties-editor.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/editor")                   |
| [buildspec_roots](#buildspec_roots)           | `array`       | Optional | cannot be null | [buildtest configuration schema](settings-properties-buildspec_roots.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/buildspec_roots") |
| [testdir](#testdir)                           | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-properties-testdir.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/testdir")                 |
| [modules_tool](#modules_tool)                 | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-properties-modules_tool.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/modules_tool")       |
| [compilers](#compilers)                       | `object`      | Optional | cannot be null | [buildtest configuration schema](settings-properties-compilers.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers")             |
| [executors](#executors)                       | `object`      | Required | cannot be null | [buildtest configuration schema](settings-properties-executors.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors")             |
| [additionalProperties](#additionalproperties) | Not specified | Optional | cannot be null | [Untitled schema](undefined.md "undefined#undefined")                                                                                                                             |

## editor

The editor field is used for opening buildspecs in an editor. The default editor is `vim`.


`editor`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-editor.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/editor")

### editor Type

`string`

### editor Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value     | Explanation |
| :-------- | ----------- |
| `"vi"`    |             |
| `"vim"`   |             |
| `"nano"`  |             |
| `"emacs"` |             |

### editor Default Value

The default value is:

```json
"vim"
```

## buildspec_roots

Specify a list of directory paths to search buildspecs. This field can be used with `buildtest buildspec find` to rebuild buildspec cache or build tests using `buildtest build` command


`buildspec_roots`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-buildspec_roots.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/buildspec_roots")

### buildspec_roots Type

`string[]`

## testdir

Specify full path to test directory where buildtest will write tests.


`testdir`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-testdir.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/testdir")

### testdir Type

`string`

## modules_tool

Specify modules tool used for interacting with `module` command. 


`modules_tool`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-modules_tool.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/modules_tool")

### modules_tool Type

`string`

### modules_tool Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value                   | Explanation |
| :---------------------- | ----------- |
| `"environment-modules"` |             |
| `"lmod"`                |             |

## compilers

Declare compiler section for defining system compilers that can be referenced in buildspec.


`compilers`

-   is optional
-   Type: `object` ([Details](settings-properties-compilers.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-compilers.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/compilers")

### compilers Type

`object` ([Details](settings-properties-compilers.md))

## executors

The executor section is used for declaring your executors that are responsible for running jobs. The executor section can be `local`, `lsf`, `slurm`, `ssh`. The executors are referenced in buildspec using `executor` field.


`executors`

-   is required
-   Type: `object` ([Details](settings-properties-executors.md))
-   cannot be null
-   defined in: [buildtest configuration schema](settings-properties-executors.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors")

### executors Type

`object` ([Details](settings-properties-executors.md))

## additionalProperties

no description

`additionalProperties`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [Untitled schema](undefined.md "undefined#undefined")

### Untitled schema Type

unknown

# buildtest configuration schema Definitions

## Definitions group cc

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cc"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group cxx

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cxx"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group fc

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/fc"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group clang

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang"}
```

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                                                       |
| :------------------ | -------- | -------- | -------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc)           | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-clang-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang/properties/cc")      |
| [cxx](#cxx)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-clang-properties-cxx.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang/properties/cxx")    |
| [modules](#modules) | `array`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang/properties/modules") |

### cc

Specify path to C compiler wrapper. You may specify a compiler wrapper such as `gcc` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`cc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-clang-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang/properties/cc")

#### cc Type

`string`

### cxx

Specify path to C++ compiler wrapper. You may specify a compiler wrapper such as `g++` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`cxx`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-clang-properties-cxx.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang/properties/cxx")

#### cxx Type

`string`

### modules

Specify list of modules to load when resolving compiler. The modules will be inserted into test script when using the compiler


`modules`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/clang/properties/modules")

#### modules Type

`string[]`

#### modules Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## Definitions group cuda

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cuda"}
```

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                                      |
| :-------------------- | -------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [cc](#cc-1)           | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-cuda-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cuda/properties/cc")       |
| [modules](#modules-1) | `array`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cuda/properties/modules") |

### cc

Specify path to C compiler wrapper. You may specify a compiler wrapper such as `gcc` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`cc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-cuda-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cuda/properties/cc")

#### cc Type

`string`

### modules

Specify list of modules to load when resolving compiler. The modules will be inserted into test script when using the compiler


`modules`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/cuda/properties/modules")

#### modules Type

`string[]`

#### modules Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## Definitions group compiler_section

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section"}
```

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                          |
| :-------------------- | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [cc](#cc-2)           | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cc")   |
| [cxx](#cxx-1)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-cxx.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cxx") |
| [fc](#fc)             | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-compiler_section-properties-fc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/fc")   |
| [modules](#modules-2) | `array`  | Optional | cannot be null | [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/modules")         |

### cc

Specify path to C compiler wrapper. You may specify a compiler wrapper such as `gcc` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`cc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-cc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cc")

#### cc Type

`string`

### cxx

Specify path to C++ compiler wrapper. You may specify a compiler wrapper such as `g++` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`cxx`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-cxx.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/cxx")

#### cxx Type

`string`

### fc

Specify path to Fortran compiler wrapper. You may specify a compiler wrapper such as `gfortran` assuming its in $PATH or you can use `modules` property to resolve path to compiler wrapper.


`fc`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-compiler_section-properties-fc.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/fc")

#### fc Type

`string`

### modules

Specify list of modules to load when resolving compiler. The modules will be inserted into test script when using the compiler


`modules`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-unique_string_array.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/compiler_section/properties/modules")

#### modules Type

`string[]`

#### modules Constraints

**unique items**: all items in this array must be unique. Duplicates are not allowed.

## Definitions group unique_string_array

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/unique_string_array"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group modules

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/modules"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group script

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/script"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group max_pend_time

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/max_pend_time"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group account

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/account"}
```

| Property | Type | Required | Nullable | Defined by |
| :------- | ---- | -------- | -------- | :--------- |

## Definitions group local

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local"}
```

| Property                        | Type          | Required | Nullable       | Defined by                                                                                                                                                                                                        |
| :------------------------------ | ------------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [description](#description)     | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/description")     |
| [shell](#shell)                 | `string`      | Required | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-shell.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/shell")                 |
| [before_script](#before_script) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/before_script") |
| [after_script](#after_script)   | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-local-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/after_script")   |

### description

description field for documenting your executor


`description`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/description")

#### description Type

`string`

### shell

Specify the shell launcher you want to use when running tests locally


`shell`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-shell.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/shell")

#### shell Type

`string`

#### shell Constraints

**pattern**: the string must match the following regular expression: 

```regexp
^(/bin/bash|/bin/sh|/bin/csh|/bin/tcsh|/bin/zsh|sh|bash|csh|tcsh|zsh|python).*
```

[try pattern](https://regexr.com/?expression=%5E(%2Fbin%2Fbash%7C%2Fbin%2Fsh%7C%2Fbin%2Fcsh%7C%2Fbin%2Ftcsh%7C%2Fbin%2Fzsh%7Csh%7Cbash%7Ccsh%7Ctcsh%7Czsh%7Cpython).* "try regular expression with regexr.com")

### before_script




`before_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/before_script")

#### before_script Type

unknown

### after_script




`after_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-local-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local/properties/after_script")

#### after_script Type

unknown

## Definitions group slurm

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm"}
```

| Property                          | Type          | Required | Nullable       | Defined by                                                                                                                                                                                                        |
| :-------------------------------- | ------------- | -------- | -------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [description](#description-1)     | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/description")     |
| [launcher](#launcher)             | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-launcher.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/launcher")           |
| [options](#options)               | `array`       | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-options.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/options")             |
| [cluster](#cluster)               | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-cluster.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/cluster")             |
| [partition](#partition)           | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-partition.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/partition")         |
| [qos](#qos)                       | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-qos.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/qos")                     |
| [before_script](#before_script-1) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/before_script") |
| [after_script](#after_script-1)   | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/after_script")   |
| [max_pend_time](#max_pend_time)   | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-max_pend_time.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/max_pend_time") |
| [account](#account)               | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-slurm-properties-account.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/account")             |

### description

description field for documenting your executor


`description`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/description")

#### description Type

`string`

### launcher

Specify the slurm batch scheduler to use. This overrides the default `launcher` field. This must be `sbatch`. 


`launcher`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-launcher.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/launcher")

#### launcher Type

`string`

#### launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value      | Explanation |
| :--------- | ----------- |
| `"sbatch"` |             |

### options

Specify any other options for `sbatch` used by this executor for running all jobs.


`options`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-options.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/options")

#### options Type

`string[]`

### cluster

Specify the slurm cluster you want to use `-M <cluster>`


`cluster`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-cluster.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/cluster")

#### cluster Type

`string`

### partition

Specify the slurm partition you want to use `-p <partition>`


`partition`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-partition.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/partition")

#### partition Type

`string`

### qos

Specify the slurm qos you want to use `-q <qos>`


`qos`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-qos.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/qos")

#### qos Type

`string`

### before_script




`before_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/before_script")

#### before_script Type

unknown

### after_script




`after_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/after_script")

#### after_script Type

unknown

### max_pend_time

Cancel job if it is still pending in queue beyond max_pend_time


`max_pend_time`

-   is optional
-   Type: `integer`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-max_pend_time.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/max_pend_time")

#### max_pend_time Type

`integer`

#### max_pend_time Constraints

**minimum**: the value of this number must greater than or equal to: `10`

#### max_pend_time Default Value

The default value is:

```json
90
```

### account

Specify Job Account for charging resources


`account`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-slurm-properties-account.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/account")

#### account Type

`string`

## Definitions group lsf

Reference this group by using

```json
{"$ref":"https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf"}
```

| Property                          | Type          | Required | Nullable       | Defined by                                                                                                                                                                                                    |
| :-------------------------------- | ------------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [description](#description-2)     | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/description")     |
| [launcher](#launcher-1)           | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-launcher.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/launcher")           |
| [options](#options-1)             | `array`       | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-options.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options")             |
| [queue](#queue)                   | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-queue.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/queue")                 |
| [before_script](#before_script-2) | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/before_script") |
| [after_script](#after_script-2)   | Not specified | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/after_script")   |
| [max_pend_time](#max_pend_time-1) | `integer`     | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-max_pend_time.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/max_pend_time") |
| [account](#account-1)             | `string`      | Optional | cannot be null | [buildtest configuration schema](settings-definitions-lsf-properties-account.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/account")             |

### description

description field for documenting your executor


`description`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/description")

#### description Type

`string`

### launcher

Specify the lsf batch scheduler to use. This overrides the default `launcher` field. It must be `bsub`. 


`launcher`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-launcher.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/launcher")

#### launcher Type

`string`

#### launcher Constraints

**enum**: the value of this property must be equal to one of the following values:

| Value    | Explanation |
| :------- | ----------- |
| `"bsub"` |             |

### options

Specify any options for `bsub` for this executor when running all jobs associated to this executor


`options`

-   is optional
-   Type: `string[]`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-options.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options")

#### options Type

`string[]`

### queue

Specify the lsf queue you want to use `-q <queue>`


`queue`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-queue.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/queue")

#### queue Type

`string`

### before_script




`before_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-before_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/before_script")

#### before_script Type

unknown

### after_script




`after_script`

-   is optional
-   Type: unknown
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-after_script.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/after_script")

#### after_script Type

unknown

### max_pend_time

Cancel job if it is still pending in queue beyond max_pend_time


`max_pend_time`

-   is optional
-   Type: `integer`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-max_pend_time.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/max_pend_time")

#### max_pend_time Type

`integer`

#### max_pend_time Constraints

**minimum**: the value of this number must greater than or equal to: `10`

#### max_pend_time Default Value

The default value is:

```json
90
```

### account

Specify Job Account for charging resources


`account`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-lsf-properties-account.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/account")

#### account Type

`string`
