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
    "gcc": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "properties": {
        "cc": {
          "type": "string"
        },
        "fc": {
          "type": "string"
        },
        "cxx": {
          "type": "string"
        },
        "cflags": {
          "type": "string"
        },
        "fflags": {
          "type": "string"
        },
        "ldflags": {
          "type": "string"
        },
        "cppflags": {
          "type": "string"
        }
      }
    },
    "intel": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "properties": {
        "cc": {
          "type": "string"
        },
        "fc": {
          "type": "string"
        },
        "cxx": {
          "type": "string"
        },
        "cflags": {
          "type": "string"
        },
        "fflags": {
          "type": "string"
        },
        "ldflags": {
          "type": "string"
        },
        "cppflags": {
          "type": "string"
        }
      }
    },
    "pgi": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "properties": {
        "cc": {
          "type": "string"
        },
        "fc": {
          "type": "string"
        },
        "cxx": {
          "type": "string"
        },
        "cflags": {
          "type": "string"
        },
        "fflags": {
          "type": "string"
        },
        "ldflags": {
          "type": "string"
        },
        "cppflags": {
          "type": "string"
        }
      }
    },
    "cray": {
      "$ref": "#definitions/default_compiler_config",
      "type": "object",
      "properties": {
        "cc": {
          "type": "string"
        },
        "fc": {
          "type": "string"
        },
        "cxx": {
          "type": "string"
        },
        "cflags": {
          "type": "string"
        },
        "fflags": {
          "type": "string"
        },
        "ldflags": {
          "type": "string"
        },
        "cppflags": {
          "type": "string"
        }
      }
    }
  }
}
```
