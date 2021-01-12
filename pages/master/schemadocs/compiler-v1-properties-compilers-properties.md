# Untitled undefined type in compiler schema version 1.0 Schema

```txt
compiler-v1.0.schema.json#/properties/compilers/properties
```




| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                             |
| :------------------ | ---------- | -------------- | ----------------------- | :---------------- | --------------------- | ------------------- | -------------------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [compiler-v1.0.schema.json\*](../out/compiler-v1.0.schema.json "open original schema") |

## properties Type

unknown

## properties Default Value

The default value is:

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "all": {
      "$ref": "#definitions/default_compiler_all",
      "type": "object",
      "description": "Specify compiler configuration for all compiler groups. Use the ``all`` property if configuration is shared across compiler groups. This property can be overridden in compiler group or named compiler in ``config`` section.",
      "additionalProperties": false,
      "properties": {
        "sbatch": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "bsub": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "cobalt": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #COBALT options in test script. buildtest will insert #COBALT in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "batch": {
          "$ref": "definitions.schema.json#/definitions/batch",
          "type": "object",
          "description": "The ``batch`` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.",
          "additionalProperties": false,
          "properties": {
            "account": {
              "type": "string",
              "description": "Specify Account to charge job"
            },
            "begintime": {
              "type": "string",
              "description": "Specify begin time when job will start allocation"
            },
            "cpucount": {
              "type": "string",
              "description": "Specify number of CPU to allocate"
            },
            "email-address": {
              "type": "string",
              "description": "Email Address to notify on Job State Changes"
            },
            "exclusive": {
              "type": "boolean",
              "description": "Specify if job needs to run in exclusive mode"
            },
            "memory": {
              "type": "string",
              "description": "Specify Memory Size for Job"
            },
            "network": {
              "type": "string",
              "description": "Specify network resource requirement for job"
            },
            "nodecount": {
              "type": "string",
              "description": "Specify number of Nodes to allocate"
            },
            "qos": {
              "type": "string",
              "description": "Specify Quality of Service (QOS)"
            },
            "queue": {
              "type": "string",
              "description": "Specify Job Queue"
            },
            "tasks-per-core": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each core. "
            },
            "tasks-per-node": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each node. "
            },
            "tasks-per-socket": {
              "type": "string",
              "description": "Request the maximum tasks to be invoked on each socket. "
            },
            "timelimit": {
              "type": "string",
              "description": "Specify Job timelimit"
            }
          }
        },
        "BB": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Create burst buffer space, this specifies #BB options in your test.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "DW": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Specify Data Warp option (#DW) when using burst buffer.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "env": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "vars": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "status": {
          "$ref": "definitions.schema.json#/definitions/status",
          "type": "object",
          "description": "The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.",
          "additionalProperties": false,
          "properties": {
            "slurm_job_state": {
              "type": "string",
              "enum": [
                "COMPLETED",
                "FAILED",
                "OUT_OF_MEMORY",
                "TIMEOUT"
              ],
              "description": "This field can be used for checking Slurm Job State, if there is a match buildtest will report as ``PASS`` "
            },
            "returncode": {
              "description": "Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array",
              "$ref": "#/definitions/int_or_list",
              "oneOf": [
                {
                  "type": "integer"
                },
                {
                  "$ref": "#/definitions/list_of_ints",
                  "type": "array",
                  "uniqueItems": true,
                  "minItems": 1,
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "regex": {
              "type": "object",
              "description": "Perform regular expression search using ``re.search`` python module on stdout/stderr stream for reporting if test ``PASS``. ",
              "properties": {
                "stream": {
                  "type": "string",
                  "enum": [
                    "stdout",
                    "stderr"
                  ],
                  "description": "The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream"
                },
                "exp": {
                  "type": "string",
                  "description": "Specify a regular expression to run with input stream specified by ``stream`` field. buildtest uses re.search when performing regex"
                }
              },
              "required": [
                "stream",
                "exp"
              ]
            }
          }
        },
        "pre_build": {
          "$ref": "#definitions/pre_build",
          "type": "string",
          "description": "Run commands before building program"
        },
        "post_build": {
          "$ref": "#definitions/post_build",
          "type": "string",
          "description": "Run commands after building program"
        },
        "pre_run": {
          "$ref": "#definitions/pre_run",
          "type": "string",
          "description": "Run commands before running program"
        },
        "post_run": {
          "$ref": "#definitions/post_run",
          "type": "string",
          "description": "Run commands after running program"
        },
        "run": {
          "$ref": "#definitions/run",
          "type": "string",
          "description": "Run command for launching compiled binary"
        }
      }
    },
    "gcc": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "description": "Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides ``all`` property. ",
      "properties": {
        "cc": {
          "$ref": "#definitions/cc",
          "type": "string",
          "description": "Set C compiler wrapper"
        },
        "fc": {
          "$ref": "#definitions/fc",
          "type": "string",
          "description": "Set Fortran compiler wrapper"
        },
        "cxx": {
          "$ref": "#definitions/cxx",
          "type": "string",
          "description": "Set C++ compiler wrapper"
        },
        "cflags": {
          "$ref": "#definitions/cflags",
          "type": "string",
          "description": "Set C compiler flags."
        },
        "fflags": {
          "$ref": "#definitions/fflags",
          "type": "string",
          "description": "Set Fortran compiler flags."
        },
        "cxxflags": {
          "$ref": "#definitions/cxxflags",
          "type": "string",
          "description": "Set C++ compiler flags."
        },
        "ldflags": {
          "$ref": "#definitions/ldflags",
          "type": "string",
          "description": "Set linker flags"
        },
        "cppflags": {
          "$ref": "#definitions/cppflags",
          "type": "string",
          "description": "Set C or C++ preprocessor flags"
        },
        "sbatch": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "bsub": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "cobalt": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #COBALT options in test script. buildtest will insert #COBALT in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "batch": {
          "$ref": "definitions.schema.json#/definitions/batch",
          "type": "object",
          "description": "The ``batch`` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.",
          "additionalProperties": false,
          "properties": {
            "account": {
              "type": "string",
              "description": "Specify Account to charge job"
            },
            "begintime": {
              "type": "string",
              "description": "Specify begin time when job will start allocation"
            },
            "cpucount": {
              "type": "string",
              "description": "Specify number of CPU to allocate"
            },
            "email-address": {
              "type": "string",
              "description": "Email Address to notify on Job State Changes"
            },
            "exclusive": {
              "type": "boolean",
              "description": "Specify if job needs to run in exclusive mode"
            },
            "memory": {
              "type": "string",
              "description": "Specify Memory Size for Job"
            },
            "network": {
              "type": "string",
              "description": "Specify network resource requirement for job"
            },
            "nodecount": {
              "type": "string",
              "description": "Specify number of Nodes to allocate"
            },
            "qos": {
              "type": "string",
              "description": "Specify Quality of Service (QOS)"
            },
            "queue": {
              "type": "string",
              "description": "Specify Job Queue"
            },
            "tasks-per-core": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each core. "
            },
            "tasks-per-node": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each node. "
            },
            "tasks-per-socket": {
              "type": "string",
              "description": "Request the maximum tasks to be invoked on each socket. "
            },
            "timelimit": {
              "type": "string",
              "description": "Specify Job timelimit"
            }
          }
        },
        "BB": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Create burst buffer space, this specifies #BB options in your test.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "DW": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Specify Data Warp option (#DW) when using burst buffer.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "env": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "vars": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "status": {
          "$ref": "definitions.schema.json#/definitions/status",
          "type": "object",
          "description": "The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.",
          "additionalProperties": false,
          "properties": {
            "slurm_job_state": {
              "type": "string",
              "enum": [
                "COMPLETED",
                "FAILED",
                "OUT_OF_MEMORY",
                "TIMEOUT"
              ],
              "description": "This field can be used for checking Slurm Job State, if there is a match buildtest will report as ``PASS`` "
            },
            "returncode": {
              "description": "Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array",
              "$ref": "#/definitions/int_or_list",
              "oneOf": [
                {
                  "type": "integer"
                },
                {
                  "$ref": "#/definitions/list_of_ints",
                  "type": "array",
                  "uniqueItems": true,
                  "minItems": 1,
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "regex": {
              "type": "object",
              "description": "Perform regular expression search using ``re.search`` python module on stdout/stderr stream for reporting if test ``PASS``. ",
              "properties": {
                "stream": {
                  "type": "string",
                  "enum": [
                    "stdout",
                    "stderr"
                  ],
                  "description": "The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream"
                },
                "exp": {
                  "type": "string",
                  "description": "Specify a regular expression to run with input stream specified by ``stream`` field. buildtest uses re.search when performing regex"
                }
              },
              "required": [
                "stream",
                "exp"
              ]
            }
          }
        },
        "pre_build": {
          "$ref": "#definitions/pre_build",
          "type": "string",
          "description": "Run commands before building program"
        },
        "post_build": {
          "$ref": "#definitions/post_build",
          "type": "string",
          "description": "Run commands after building program"
        },
        "pre_run": {
          "$ref": "#definitions/pre_run",
          "type": "string",
          "description": "Run commands before running program"
        },
        "post_run": {
          "$ref": "#definitions/post_run",
          "type": "string",
          "description": "Run commands after running program"
        },
        "run": {
          "$ref": "#definitions/run",
          "type": "string",
          "description": "Run command for launching compiled binary"
        }
      }
    },
    "intel": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "description": "Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides ``all`` property. ",
      "properties": {
        "cc": {
          "$ref": "#definitions/cc",
          "type": "string",
          "description": "Set C compiler wrapper"
        },
        "fc": {
          "$ref": "#definitions/fc",
          "type": "string",
          "description": "Set Fortran compiler wrapper"
        },
        "cxx": {
          "$ref": "#definitions/cxx",
          "type": "string",
          "description": "Set C++ compiler wrapper"
        },
        "cflags": {
          "$ref": "#definitions/cflags",
          "type": "string",
          "description": "Set C compiler flags."
        },
        "fflags": {
          "$ref": "#definitions/fflags",
          "type": "string",
          "description": "Set Fortran compiler flags."
        },
        "cxxflags": {
          "$ref": "#definitions/cxxflags",
          "type": "string",
          "description": "Set C++ compiler flags."
        },
        "ldflags": {
          "$ref": "#definitions/ldflags",
          "type": "string",
          "description": "Set linker flags"
        },
        "cppflags": {
          "$ref": "#definitions/cppflags",
          "type": "string",
          "description": "Set C or C++ preprocessor flags"
        },
        "sbatch": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "bsub": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "cobalt": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #COBALT options in test script. buildtest will insert #COBALT in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "batch": {
          "$ref": "definitions.schema.json#/definitions/batch",
          "type": "object",
          "description": "The ``batch`` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.",
          "additionalProperties": false,
          "properties": {
            "account": {
              "type": "string",
              "description": "Specify Account to charge job"
            },
            "begintime": {
              "type": "string",
              "description": "Specify begin time when job will start allocation"
            },
            "cpucount": {
              "type": "string",
              "description": "Specify number of CPU to allocate"
            },
            "email-address": {
              "type": "string",
              "description": "Email Address to notify on Job State Changes"
            },
            "exclusive": {
              "type": "boolean",
              "description": "Specify if job needs to run in exclusive mode"
            },
            "memory": {
              "type": "string",
              "description": "Specify Memory Size for Job"
            },
            "network": {
              "type": "string",
              "description": "Specify network resource requirement for job"
            },
            "nodecount": {
              "type": "string",
              "description": "Specify number of Nodes to allocate"
            },
            "qos": {
              "type": "string",
              "description": "Specify Quality of Service (QOS)"
            },
            "queue": {
              "type": "string",
              "description": "Specify Job Queue"
            },
            "tasks-per-core": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each core. "
            },
            "tasks-per-node": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each node. "
            },
            "tasks-per-socket": {
              "type": "string",
              "description": "Request the maximum tasks to be invoked on each socket. "
            },
            "timelimit": {
              "type": "string",
              "description": "Specify Job timelimit"
            }
          }
        },
        "BB": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Create burst buffer space, this specifies #BB options in your test.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "DW": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Specify Data Warp option (#DW) when using burst buffer.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "env": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "vars": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "status": {
          "$ref": "definitions.schema.json#/definitions/status",
          "type": "object",
          "description": "The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.",
          "additionalProperties": false,
          "properties": {
            "slurm_job_state": {
              "type": "string",
              "enum": [
                "COMPLETED",
                "FAILED",
                "OUT_OF_MEMORY",
                "TIMEOUT"
              ],
              "description": "This field can be used for checking Slurm Job State, if there is a match buildtest will report as ``PASS`` "
            },
            "returncode": {
              "description": "Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array",
              "$ref": "#/definitions/int_or_list",
              "oneOf": [
                {
                  "type": "integer"
                },
                {
                  "$ref": "#/definitions/list_of_ints",
                  "type": "array",
                  "uniqueItems": true,
                  "minItems": 1,
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "regex": {
              "type": "object",
              "description": "Perform regular expression search using ``re.search`` python module on stdout/stderr stream for reporting if test ``PASS``. ",
              "properties": {
                "stream": {
                  "type": "string",
                  "enum": [
                    "stdout",
                    "stderr"
                  ],
                  "description": "The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream"
                },
                "exp": {
                  "type": "string",
                  "description": "Specify a regular expression to run with input stream specified by ``stream`` field. buildtest uses re.search when performing regex"
                }
              },
              "required": [
                "stream",
                "exp"
              ]
            }
          }
        },
        "pre_build": {
          "$ref": "#definitions/pre_build",
          "type": "string",
          "description": "Run commands before building program"
        },
        "post_build": {
          "$ref": "#definitions/post_build",
          "type": "string",
          "description": "Run commands after building program"
        },
        "pre_run": {
          "$ref": "#definitions/pre_run",
          "type": "string",
          "description": "Run commands before running program"
        },
        "post_run": {
          "$ref": "#definitions/post_run",
          "type": "string",
          "description": "Run commands after running program"
        },
        "run": {
          "$ref": "#definitions/run",
          "type": "string",
          "description": "Run command for launching compiled binary"
        }
      }
    },
    "pgi": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "description": "Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides ``all`` property. ",
      "properties": {
        "cc": {
          "$ref": "#definitions/cc",
          "type": "string",
          "description": "Set C compiler wrapper"
        },
        "fc": {
          "$ref": "#definitions/fc",
          "type": "string",
          "description": "Set Fortran compiler wrapper"
        },
        "cxx": {
          "$ref": "#definitions/cxx",
          "type": "string",
          "description": "Set C++ compiler wrapper"
        },
        "cflags": {
          "$ref": "#definitions/cflags",
          "type": "string",
          "description": "Set C compiler flags."
        },
        "fflags": {
          "$ref": "#definitions/fflags",
          "type": "string",
          "description": "Set Fortran compiler flags."
        },
        "cxxflags": {
          "$ref": "#definitions/cxxflags",
          "type": "string",
          "description": "Set C++ compiler flags."
        },
        "ldflags": {
          "$ref": "#definitions/ldflags",
          "type": "string",
          "description": "Set linker flags"
        },
        "cppflags": {
          "$ref": "#definitions/cppflags",
          "type": "string",
          "description": "Set C or C++ preprocessor flags"
        },
        "sbatch": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "bsub": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "cobalt": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #COBALT options in test script. buildtest will insert #COBALT in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "batch": {
          "$ref": "definitions.schema.json#/definitions/batch",
          "type": "object",
          "description": "The ``batch`` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.",
          "additionalProperties": false,
          "properties": {
            "account": {
              "type": "string",
              "description": "Specify Account to charge job"
            },
            "begintime": {
              "type": "string",
              "description": "Specify begin time when job will start allocation"
            },
            "cpucount": {
              "type": "string",
              "description": "Specify number of CPU to allocate"
            },
            "email-address": {
              "type": "string",
              "description": "Email Address to notify on Job State Changes"
            },
            "exclusive": {
              "type": "boolean",
              "description": "Specify if job needs to run in exclusive mode"
            },
            "memory": {
              "type": "string",
              "description": "Specify Memory Size for Job"
            },
            "network": {
              "type": "string",
              "description": "Specify network resource requirement for job"
            },
            "nodecount": {
              "type": "string",
              "description": "Specify number of Nodes to allocate"
            },
            "qos": {
              "type": "string",
              "description": "Specify Quality of Service (QOS)"
            },
            "queue": {
              "type": "string",
              "description": "Specify Job Queue"
            },
            "tasks-per-core": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each core. "
            },
            "tasks-per-node": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each node. "
            },
            "tasks-per-socket": {
              "type": "string",
              "description": "Request the maximum tasks to be invoked on each socket. "
            },
            "timelimit": {
              "type": "string",
              "description": "Specify Job timelimit"
            }
          }
        },
        "BB": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Create burst buffer space, this specifies #BB options in your test.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "DW": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Specify Data Warp option (#DW) when using burst buffer.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "env": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "vars": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "status": {
          "$ref": "definitions.schema.json#/definitions/status",
          "type": "object",
          "description": "The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.",
          "additionalProperties": false,
          "properties": {
            "slurm_job_state": {
              "type": "string",
              "enum": [
                "COMPLETED",
                "FAILED",
                "OUT_OF_MEMORY",
                "TIMEOUT"
              ],
              "description": "This field can be used for checking Slurm Job State, if there is a match buildtest will report as ``PASS`` "
            },
            "returncode": {
              "description": "Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array",
              "$ref": "#/definitions/int_or_list",
              "oneOf": [
                {
                  "type": "integer"
                },
                {
                  "$ref": "#/definitions/list_of_ints",
                  "type": "array",
                  "uniqueItems": true,
                  "minItems": 1,
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "regex": {
              "type": "object",
              "description": "Perform regular expression search using ``re.search`` python module on stdout/stderr stream for reporting if test ``PASS``. ",
              "properties": {
                "stream": {
                  "type": "string",
                  "enum": [
                    "stdout",
                    "stderr"
                  ],
                  "description": "The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream"
                },
                "exp": {
                  "type": "string",
                  "description": "Specify a regular expression to run with input stream specified by ``stream`` field. buildtest uses re.search when performing regex"
                }
              },
              "required": [
                "stream",
                "exp"
              ]
            }
          }
        },
        "pre_build": {
          "$ref": "#definitions/pre_build",
          "type": "string",
          "description": "Run commands before building program"
        },
        "post_build": {
          "$ref": "#definitions/post_build",
          "type": "string",
          "description": "Run commands after building program"
        },
        "pre_run": {
          "$ref": "#definitions/pre_run",
          "type": "string",
          "description": "Run commands before running program"
        },
        "post_run": {
          "$ref": "#definitions/post_run",
          "type": "string",
          "description": "Run commands after running program"
        },
        "run": {
          "$ref": "#definitions/run",
          "type": "string",
          "description": "Run command for launching compiled binary"
        }
      }
    },
    "cray": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "description": "Specify compiler configuration for group of compilers. Use this property if you want to define common configuration for all compilers of same group. This property overrides ``all`` property. ",
      "properties": {
        "cc": {
          "$ref": "#definitions/cc",
          "type": "string",
          "description": "Set C compiler wrapper"
        },
        "fc": {
          "$ref": "#definitions/fc",
          "type": "string",
          "description": "Set Fortran compiler wrapper"
        },
        "cxx": {
          "$ref": "#definitions/cxx",
          "type": "string",
          "description": "Set C++ compiler wrapper"
        },
        "cflags": {
          "$ref": "#definitions/cflags",
          "type": "string",
          "description": "Set C compiler flags."
        },
        "fflags": {
          "$ref": "#definitions/fflags",
          "type": "string",
          "description": "Set Fortran compiler flags."
        },
        "cxxflags": {
          "$ref": "#definitions/cxxflags",
          "type": "string",
          "description": "Set C++ compiler flags."
        },
        "ldflags": {
          "$ref": "#definitions/ldflags",
          "type": "string",
          "description": "Set linker flags"
        },
        "cppflags": {
          "$ref": "#definitions/cppflags",
          "type": "string",
          "description": "Set C or C++ preprocessor flags"
        },
        "sbatch": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #SBATCH options in test script. buildtest will insert #SBATCH in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "bsub": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #BSUB options in test script. buildtest will insert #BSUB in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "cobalt": {
          "$ref": "#/definitions/list_of_strings",
          "description": "This field is used for specifying #COBALT options in test script. buildtest will insert #COBALT in front of each value",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "batch": {
          "$ref": "definitions.schema.json#/definitions/batch",
          "type": "object",
          "description": "The ``batch`` field is used to specify scheduler agnostic directives that are translated to #SBATCH or #BSUB based on your scheduler. This is an experimental feature that supports a subset of scheduler parameters.",
          "additionalProperties": false,
          "properties": {
            "account": {
              "type": "string",
              "description": "Specify Account to charge job"
            },
            "begintime": {
              "type": "string",
              "description": "Specify begin time when job will start allocation"
            },
            "cpucount": {
              "type": "string",
              "description": "Specify number of CPU to allocate"
            },
            "email-address": {
              "type": "string",
              "description": "Email Address to notify on Job State Changes"
            },
            "exclusive": {
              "type": "boolean",
              "description": "Specify if job needs to run in exclusive mode"
            },
            "memory": {
              "type": "string",
              "description": "Specify Memory Size for Job"
            },
            "network": {
              "type": "string",
              "description": "Specify network resource requirement for job"
            },
            "nodecount": {
              "type": "string",
              "description": "Specify number of Nodes to allocate"
            },
            "qos": {
              "type": "string",
              "description": "Specify Quality of Service (QOS)"
            },
            "queue": {
              "type": "string",
              "description": "Specify Job Queue"
            },
            "tasks-per-core": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each core. "
            },
            "tasks-per-node": {
              "type": "string",
              "description": "Request number of tasks to be invoked on each node. "
            },
            "tasks-per-socket": {
              "type": "string",
              "description": "Request the maximum tasks to be invoked on each socket. "
            },
            "timelimit": {
              "type": "string",
              "description": "Specify Job timelimit"
            }
          }
        },
        "BB": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Create burst buffer space, this specifies #BB options in your test.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "DW": {
          "$ref": "#/definitions/list_of_strings",
          "description": "Specify Data Warp option (#DW) when using burst buffer.",
          "type": "array",
          "uniqueItems": true,
          "minItems": 1,
          "items": {
            "type": "string"
          }
        },
        "env": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "vars": {
          "$ref": "definitions.schema.json#/definitions/env",
          "type": "object",
          "description": "One or more key value pairs for an environment (key=value)",
          "minItems": 1,
          "items": {
            "type": "object",
            "minItems": 1,
            "propertyNames": {
              "pattern": "^[A-Za-z_][A-Za-z0-9_]*$"
            }
          }
        },
        "status": {
          "$ref": "definitions.schema.json#/definitions/status",
          "type": "object",
          "description": "The status section describes how buildtest detects PASS/FAIL on test. By default returncode 0 is a PASS and anything else is a FAIL, however buildtest can support other types of PASS/FAIL conditions.",
          "additionalProperties": false,
          "properties": {
            "slurm_job_state": {
              "type": "string",
              "enum": [
                "COMPLETED",
                "FAILED",
                "OUT_OF_MEMORY",
                "TIMEOUT"
              ],
              "description": "This field can be used for checking Slurm Job State, if there is a match buildtest will report as ``PASS`` "
            },
            "returncode": {
              "description": "Specify a list of returncodes to match with script's exit code. buildtest will PASS test if script's exit code is found in list of returncodes. You must specify unique numbers as list and a minimum of 1 item in array",
              "$ref": "#/definitions/int_or_list",
              "oneOf": [
                {
                  "type": "integer"
                },
                {
                  "$ref": "#/definitions/list_of_ints",
                  "type": "array",
                  "uniqueItems": true,
                  "minItems": 1,
                  "items": {
                    "type": "integer"
                  }
                }
              ]
            },
            "regex": {
              "type": "object",
              "description": "Perform regular expression search using ``re.search`` python module on stdout/stderr stream for reporting if test ``PASS``. ",
              "properties": {
                "stream": {
                  "type": "string",
                  "enum": [
                    "stdout",
                    "stderr"
                  ],
                  "description": "The stream field can be stdout or stderr. buildtest will read the output or error stream after completion of test and check if regex matches in stream"
                },
                "exp": {
                  "type": "string",
                  "description": "Specify a regular expression to run with input stream specified by ``stream`` field. buildtest uses re.search when performing regex"
                }
              },
              "required": [
                "stream",
                "exp"
              ]
            }
          }
        },
        "pre_build": {
          "$ref": "#definitions/pre_build",
          "type": "string",
          "description": "Run commands before building program"
        },
        "post_build": {
          "$ref": "#definitions/post_build",
          "type": "string",
          "description": "Run commands after building program"
        },
        "pre_run": {
          "$ref": "#definitions/pre_run",
          "type": "string",
          "description": "Run commands before running program"
        },
        "post_run": {
          "$ref": "#definitions/post_run",
          "type": "string",
          "description": "Run commands after running program"
        },
        "run": {
          "$ref": "#definitions/run",
          "type": "string",
          "description": "Run command for launching compiled binary"
        }
      }
    }
  }
}
```
