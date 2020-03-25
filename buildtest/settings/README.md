# Settings

The configuration file in this folder serves to validate a user configuration for
buildtest. This means that by default, the executor of choice is a local system (or
a local host) and this can be modified to use a specific launcher
or scheduler. Any build test test recipe should be easy to run on different
schedulers and/or launchers by way of editing the default configuration file,
or by customizing usage on the command line.

 - [default.yml](default.yml) is the default configuration with a local executor
 - [default-config.json](default-config.json) is validation for this file.

## Executors

Any executor can be defined (by name) and must include a type, launcher,
scheduler, and description. We use the key as a name and index in buildtest, and
we use the type to match to the correct Executor class (e.g., LocalExecutor)

```yaml
editor: vi
executors:
  local:
    type: local
    description: submit jobs locally
```

Notice that the first variable "local" is the key. This should be unique across definitions.
If you put two sections with the same name, only one will be read as it is loaded as a dictionary.

 - type: is the class of executor under BuildTest/executors/base.py (e.g., `LocalExecutor`)
 - description: is a description for the executor.

All other variables that are executor-specific (e.g., a launcher) should be defined under
vars. The vars that are required are checked by the matching executor class. For example,
let's say that I want to use a slurm executor and specify a launcher to be srun. Launcher
is a variable that is custom for a slurm executor, and defaults to sbatch. However I might
want to use this type, and specify a default of srun instead. I might do

```yaml
editor: vi
executors:
  slurm:
    type: slurm
    description: submit jobs with slurm using srun instead of sbatch
    vars:
      launcher: sbatch
``` 
