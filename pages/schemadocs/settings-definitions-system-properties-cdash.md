# Untitled object in buildtest configuration schema Schema

```txt
settings.schema.json#/definitions/system/properties/cdash
```

Specify CDASH configuration used to upload tests via 'buildtest cdash' command

| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | :--------- | :------------- | :----------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Allowed               | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## cdash Type

`object` ([Details](settings-definitions-system-properties-cdash.md))

# cdash Properties

| Property            | Type     | Required | Nullable       | Defined by                                                                                                                                                                          |
| :------------------ | :------- | :------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [url](#url)         | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-cdash-properties-url.md "settings.schema.json#/definitions/system/properties/cdash/properties/url")         |
| [project](#project) | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-cdash-properties-project.md "settings.schema.json#/definitions/system/properties/cdash/properties/project") |
| [site](#site)       | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-system-properties-cdash-properties-site.md "settings.schema.json#/definitions/system/properties/cdash/properties/site")       |

## url

Url to CDASH server

`url`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-cdash-properties-url.md "settings.schema.json#/definitions/system/properties/cdash/properties/url")

### url Type

`string`

## project

Name of CDASH project

`project`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-cdash-properties-project.md "settings.schema.json#/definitions/system/properties/cdash/properties/project")

### project Type

`string`

## site

Site Name reported in CDASH

`site`

*   is required

*   Type: `string`

*   cannot be null

*   defined in: [buildtest configuration schema](settings-definitions-system-properties-cdash-properties-site.md "settings.schema.json#/definitions/system/properties/cdash/properties/site")

### site Type

`string`
