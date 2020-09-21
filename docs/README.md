# README

## Top-level Schemas

-   [buildtest configuration schema](./settings.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json`
-   [compiler schema version 1.0](./compiler-v1.md "The compiler schema is of type: compiler in sub-schema which is used for compiling and running programs") – `https://buildtesters.github.io/buildtest/schemas/compiler-v1.0.schema.json`
-   [global schema](./global.md "buildtest global schema is validated for all buildspecs") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json`
-   [python schema version 1.0](./python-v1.md "The script schema is of type: python in sub-schema which is used for running python scripts") – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json`
-   [script schema version 1.0](./script-v1.md "The script schema is of type: script in sub-schema which is used for running shell scripts") – `https://buildtesters.github.io/buildtest/schemas/script-v1.0.schema.json`

## Other Schemas

### Objects

-   [Untitled object in buildtest configuration schema](./settings-properties-executors.md "The executor section is used for declaring your executors that are responsible for running jobs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-defaults.md "Specify default executor settings for all executors") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/defaults`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-local.md "The local section is used for declaring local executors for running jobs on local machine") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/local`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-local-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/local/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-lsf.md "The lsf section is used for declaring LSF executors for running jobs using LSF scheduler") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/lsf`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-lsf-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/lsf/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-slurm.md "The slurm section is used for declaring Slurm executors for running jobs using Slurm scheduler") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/slurm`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-slurm-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/slurm/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-ssh.md "The ssh section is used for declaring SSH executors for running jobs on remote node using ssh") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/ssh`
-   [Untitled object in buildtest configuration schema](./settings-properties-executors-properties-ssh-patternproperties-.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/executors/properties/ssh/patternProperties/^.*$`
-   [Untitled object in buildtest configuration schema](./settings-properties-config.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config`
-   [Untitled object in buildtest configuration schema](./settings-properties-config-properties-paths.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths`
-   [Untitled object in buildtest configuration schema](./settings-definitions-modules.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/modules`
-   [Untitled object in buildtest configuration schema](./settings-definitions-local.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/local`
-   [Untitled object in buildtest configuration schema](./settings-definitions-slurm.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm`
-   [Untitled object in buildtest configuration schema](./settings-definitions-lsf.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf`
-   [Untitled object in buildtest configuration schema](./settings-definitions-ssh.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-build.md "The build section is used for compiling a single program, this section specifies fields for setting C, C++, Fortran compiler and flags including CPP flags and linker flags") – `https://buildtesters.github.io/buildtest/schemas/compiler-v1.0.schema.json#/properties/build`
-   [Untitled object in compiler schema version 1.0](./compiler-v1-properties-run.md "The run section is used for specifying launch configuration of executable") – `https://buildtesters.github.io/buildtest/schemas/compiler-v1.0.schema.json#/properties/run`
-   [Untitled object in global schema](./global-properties-buildspecs.md "This section is used to define one or more tests (buildspecs)") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/buildspecs`
-   [Untitled object in global schema](./global-definitions-env.md "One or more key value pairs for an environment (key=value)") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/env`
-   [Untitled object in global schema](./global-definitions-env-items.md) – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/env/items`
-   [Untitled object in global schema](./global-definitions-status.md "The status section describes how buildtest detects PASS/FAIL on test") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/status`
-   [Untitled object in global schema](./global-definitions-status-properties-regex.md "Perform regular expression search using re") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/status/properties/regex`
-   [Untitled object in python schema version 1.0](./python-v1-properties-package.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package`

### Arrays

-   [Untitled array in buildtest configuration schema](./settings-definitions-lsf-properties-options.md "Specify any options for bsub for this executor when running all jobs associated to this executor") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options`
-   [Untitled array in buildtest configuration schema](./settings-definitions-slurm-properties-options.md "Specify any other options for sbatch used by this executor for running all jobs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/options`
-   [Untitled array in buildtest configuration schema](./settings-properties-config-properties-paths-properties-buildspec_roots.md "Specify a list of directory paths to search buildspecs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/properties/config/properties/paths/properties/buildspec_roots`
-   [Untitled array in buildtest configuration schema](./settings-definitions-modules-properties-load.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/modules/properties/load`
-   [Untitled array in buildtest configuration schema](./settings-definitions-script.md) – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/script`
-   [Untitled array in buildtest configuration schema](./settings-definitions-slurm-properties-options.md "Specify any other options for sbatch used by this executor for running all jobs") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/slurm/properties/options`
-   [Untitled array in buildtest configuration schema](./settings-definitions-lsf-properties-options.md "Specify any options for bsub for this executor when running all jobs associated to this executor") – `https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/lsf/properties/options`
-   [Untitled array in compiler schema version 1.0](./compiler-v1-properties-module.md "A list of modules to load into test script") – `https://buildtesters.github.io/buildtest/schemas/compiler-v1.0.schema.json#/properties/module`
-   [Untitled array in global schema](./global-properties-maintainers.md "One or more maintainers or aliases") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/properties/maintainers`
-   [Untitled array in global schema](./global-definitions-tags.md "Classify tests using a tag name, this can be used for categorizing test and building tests using --tags option") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/tags`
-   [Untitled array in global schema](./global-definitions-sbatch.md "This field is used for specifying #SBATCH options in test script") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/sbatch`
-   [Untitled array in global schema](./global-definitions-bsub.md "This field is used for specifying #BSUB options in test script") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/bsub`
-   [Untitled array in global schema](./global-definitions-status-properties-returncode.md "Specify a list of returncodes to match with script's exit code") – `https://buildtesters.github.io/buildtest/schemas/global.schema.json#/definitions/status/properties/returncode`
-   [Untitled array in python schema version 1.0](./python-v1-properties-pyver.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/pyver`
-   [Untitled array in python schema version 1.0](./python-v1-properties-package-properties-pypi.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/package/properties/pypi`
-   [Untitled array in python schema version 1.0](./python-v1-properties-module.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/module`
-   [Untitled array in python schema version 1.0](./python-v1-properties-sbatch.md) – `https://buildtesters.github.io/schemas/schemas/python-v1.0.schema.json#/properties/sbatch`

## Version Note

The schemas linked above follow the JSON Schema Spec version: `http://json-schema.org/draft-07/schema#`
