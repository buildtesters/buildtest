# README

## Top-level Schemas

-   [JSON Schema Definitions File. ](./definitions.md "This file is used for declaring definitions that are referenced from other schemas") – `definitions.schema.json`
-   [buildtest configuration schema](./settings.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json`
-   [compiler schema version 1.0](./compiler-v1.md "The compiler schema is of type: compiler in sub-schema which is used for compiling and running programs") – `compiler-v1.0.schema.json`
-   [global schema](./global.md "buildtest global schema is validated for all buildspecs") – `global.schema.json`
-   [python schema version 1.0](./python-v1.md "The script schema is of type: python in sub-schema which is used for running python scripts") – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json`
-   [script schema version 1.0](./script-v1.md "The script schema is of type: script in sub-schema which is used for running shell scripts") – `script-v1.0.schema.json`

## Other Schemas

### Objects

-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-env-items.md) – `definitions.schema.json#/definitions/env/items`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-env-items.md) – `definitions.schema.json#/definitions/env/items`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-status-properties-regex.md "Perform regular expression search using re") – `definitions.schema.json#/definitions/status/properties/regex`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-env.md "One or more key value pairs for an environment (key=value)") – `definitions.schema.json#/definitions/env`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-env-items.md) – `definitions.schema.json#/definitions/env/items`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-status.md "The status section describes how buildtest detects PASS/FAIL on test") – `definitions.schema.json#/definitions/status`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-status-properties-regex.md "Perform regular expression search using re") – `definitions.schema.json#/definitions/status/properties/regex`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-status-properties-regex.md "Perform regular expression search using re") – `definitions.schema.json#/definitions/status/properties/regex`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-env-items.md) – `definitions.schema.json#/definitions/env/items`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-env-items.md) – `definitions.schema.json#/definitions/env/items`
-   [Untitled object in JSON Schema Definitions File. ](./definitions-definitions-status-properties-regex.md "Perform regular expression search using re") – `definitions.schema.json#/definitions/status/properties/regex`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors.md "The executor section is used for declaring your executors that are responsible for running jobs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-defaults.md "Specify default executor settings for all executors") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/defaults`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-local.md "The local section is used for declaring local executors for running jobs on local machine") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/local`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-local-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/local/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-lsf.md "The lsf section is used for declaring LSF executors for running jobs using LSF scheduler") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/lsf`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-lsf-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/lsf/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-slurm.md "The slurm section is used for declaring Slurm executors for running jobs using Slurm scheduler") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/slurm`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-slurm-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/slurm/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-config.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config`
-   [Untitled object in buildtest configuration schema](./settings-properties-config-properties-paths.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths`
-   [Untitled object in buildtest configuration schema](./settings-definitions-modules.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/modules`
-   [Untitled object in buildtest configuration schema](./settings-definitions-local.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local`
-   [Untitled object in buildtest configuration schema](./settings-definitions-slurm.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm`
-   [Untitled object in buildtest configuration schema](./settings-definitions-lsf.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-env.md "One or more key value pairs for an environment (key=value)") – `compiler-v1.0.schema.json#/properties/env`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-vars.md "One or more key value pairs for an environment (key=value)") – `compiler-v1.0.schema.json#/properties/vars`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-status.md "The status section describes how buildtest detects PASS/FAIL on test") – `compiler-v1.0.schema.json#/properties/status`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-build.md "The build section is used for compiling a single program, this section specifies fields for setting C, C++, Fortran compiler and flags including CPP flags and linker flags") – `compiler-v1.0.schema.json#/properties/build`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-run.md "The run section is used for specifying launch configuration of executable") – `compiler-v1.0.schema.json#/properties/run`
-   [Untitled object in global schema](./global-properties-buildspecs.md "This section is used to define one or more tests (buildspecs)") – `global.schema.json#/properties/buildspecs`
-   [Untitled object in python schema version 1.0](./python-v1-properties-package.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package`
-   [Untitled object in python schema version 1.0](./python-v1-properties-status.md "The status section describes how buildtest detects PASS/FAIL on test") – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/status`
-   [Untitled object in script schema version 1.0](./script-v1-properties-env.md "One or more key value pairs for an environment (key=value)") – `script-v1.0.schema.json#/properties/env`
-   [Untitled object in script schema version 1.0](./script-v1-properties-vars.md "One or more key value pairs for an environment (key=value)") – `script-v1.0.schema.json#/properties/vars`
-   [Untitled object in script schema version 1.0](./script-v1-properties-status.md "The status section describes how buildtest detects PASS/FAIL on test") – `script-v1.0.schema.json#/properties/status`

### Arrays

-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-int_or_list-oneof-1.md) – `definitions.schema.json#/definitions/int_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-string_or_list-oneof-1.md) – `definitions.schema.json#/definitions/string_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-list_of_strings.md) – `definitions.schema.json#/definitions/list_of_strings`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-string_or_list-oneof-1.md) – `definitions.schema.json#/definitions/string_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-list_of_ints.md) – `definitions.schema.json#/definitions/list_of_ints`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-int_or_list-oneof-1.md) – `definitions.schema.json#/definitions/int_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-string_or_list-oneof-1.md) – `definitions.schema.json#/definitions/string_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-sbatch.md "This field is used for specifying #SBATCH options in test script") – `definitions.schema.json#/definitions/sbatch`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-bsub.md "This field is used for specifying #BSUB options in test script") – `definitions.schema.json#/definitions/bsub`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-int_or_list-oneof-1.md) – `definitions.schema.json#/definitions/int_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-int_or_list-oneof-1.md) – `definitions.schema.json#/definitions/int_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-string_or_list-oneof-1.md) – `definitions.schema.json#/definitions/string_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-int_or_list-oneof-1.md) – `definitions.schema.json#/definitions/int_or_list/oneOf/1`
-   [Untitled array in JSON Schema Definitions File. ](./definitions-definitions-string_or_list-oneof-1.md) – `definitions.schema.json#/definitions/string_or_list/oneOf/1`
-   [Untitled array in buildtest configuration schema](./settings-definitions-lsf-properties-options.md "Specify any options for bsub for this executor when running all jobs associated to this executor") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options`
-   [Untitled array in buildtest configuration schema](./settings-definitions-slurm-properties-options.md "Specify any other options for sbatch used by this executor for running all jobs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/options`
-   [Untitled array in buildtest configuration schema](./settings-properties-config-properties-paths-properties-buildspec_roots.md "Specify a list of directory paths to search buildspecs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/buildspec_roots`
-   [Untitled array in buildtest configuration schema](./settings-definitions-modules-properties-load.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/modules/properties/load`
-   [Untitled array in buildtest configuration schema](./settings-definitions-script.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/script`
-   [Untitled array in buildtest configuration schema](./settings-definitions-slurm-properties-options.md "Specify any other options for sbatch used by this executor for running all jobs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/options`
-   [Untitled array in buildtest configuration schema](./settings-definitions-lsf-properties-options.md "Specify any options for bsub for this executor when running all jobs associated to this executor") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options`
-   [Untitled array in compiler schema version 1.0](./compiler-v1-properties-module.md "A list of modules to load into test script") – `compiler-v1.0.schema.json#/properties/module`
-   [Untitled array in compiler schema version 1.0](./compiler-v1-properties-sbatch.md "This field is used for specifying #SBATCH options in test script") – `compiler-v1.0.schema.json#/properties/sbatch`
-   [Untitled array in compiler schema version 1.0](./compiler-v1-properties-bsub.md "This field is used for specifying #BSUB options in test script") – `compiler-v1.0.schema.json#/properties/bsub`
-   [Untitled array in global schema](./global-properties-maintainers.md "One or more maintainers or aliases") – `global.schema.json#/properties/maintainers`
-   [Untitled array in python schema version 1.0](./python-v1-properties-pyver.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/pyver`
-   [Untitled array in python schema version 1.0](./python-v1-properties-package-properties-pypi.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package/properties/pypi`
-   [Untitled array in python schema version 1.0](./python-v1-properties-module.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/module`
-   [Untitled array in python schema version 1.0](./python-v1-properties-sbatch.md "This field is used for specifying #SBATCH options in test script") – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/sbatch`
-   [Untitled array in script schema version 1.0](./script-v1-properties-sbatch.md "This field is used for specifying #SBATCH options in test script") – `script-v1.0.schema.json#/properties/sbatch`
-   [Untitled array in script schema version 1.0](./script-v1-properties-bsub.md "This field is used for specifying #BSUB options in test script") – `script-v1.0.schema.json#/properties/bsub`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
