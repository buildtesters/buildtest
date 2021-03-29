# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/compilers
```

Declare compiler section for defining system compilers that can be referenced in buildspec.

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                  |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :-------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json*](../out/settings.schema.json "open original schema") |

## compilers Type

`object` ([Details](settings-definitions-system-properties-compilers.md))

# compilers Properties

| Property              | Type     | Required | Nullable       | Defined by                                                                                                                                                                                    |
| :-------------------- | :------- | :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [find](#find)         | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find.md "settings.schema.json#/definitions/system/properties/compilers/properties/find")         |
| [compiler](#compiler) | `object` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler") |

## find

Find compilers by specifying regular expression that is applied to modulefile names

`find`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-find.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-find.md "settings.schema.json#/definitions/system/properties/compilers/properties/find")

### find Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-find.md))

## compiler

Start of compiler declaration

`compiler`

*   is optional

*   Type: `object` ([Details](settings-definitions-system-properties-compilers-properties-compiler.md))

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-compilers-properties-compiler.md "settings.schema.json#/definitions/system/properties/compilers/properties/compiler")

### compiler Type

`object` ([Details](settings-definitions-system-properties-compilers-properties-compiler.md))
