# Untitled object in buildtest configuration schema Schema

```txt
https://buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh
```




| Abstract            | Extensible | Status         | Identifiable | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                                   |
| :------------------ | ---------- | -------------- | ------------ | :---------------- | --------------------- | ------------------- | ---------------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | No           | Forbidden         | Forbidden             | none                | [settings.schema.json\*](../out/settings.schema.json "open original schema") |

## ssh Type

`object` ([Details](settings-definitions-ssh.md))

# undefined Properties

| Property                        | Type     | Required | Nullable       | Defined by                                                                                                                                                                                                    |
| :------------------------------ | -------- | -------- | -------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [description](#description)     | `string` | Optional | cannot be null | [buildtest configuration schema](settings-definitions-ssh-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/description")     |
| [host](#host)                   | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-ssh-properties-host.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/host")                   |
| [user](#user)                   | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-ssh-properties-user.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/user")                   |
| [identity_file](#identity_file) | `string` | Required | cannot be null | [buildtest configuration schema](settings-definitions-ssh-properties-identity_file.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/identity_file") |

## description




`description`

-   is optional
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-ssh-properties-description.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/description")

### description Type

`string`

## host




`host`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-ssh-properties-host.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/host")

### host Type

`string`

## user




`user`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-ssh-properties-user.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/user")

### user Type

`string`

## identity_file




`identity_file`

-   is required
-   Type: `string`
-   cannot be null
-   defined in: [buildtest configuration schema](settings-definitions-ssh-properties-identity_file.md "https&#x3A;//buildtesters.github.io/buildtest/schemas/settings.schema.json#/definitions/ssh/properties/identity_file")

### identity_file Type

`string`
