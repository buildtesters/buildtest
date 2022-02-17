# Untitled boolean in spack schema version Schema

```txt
spack.schema.json#/properties/spack/properties/verify_spack
```

This boolean will determine if we need to check for file existence where spack is cloned via `root` property and file **$SPACK\_ROOT/share/spack/setup-env.sh** exists. These checks can be disabled by setting this to `False` which can be useful if you dont want buildtest to raise exception during test generation process and test is skipped.

| Abstract            | Extensible | Status         | Identifiable            | Custom Properties | Additional Properties | Access Restrictions | Defined In                                                             |
| :------------------ | :--------- | :------------- | :---------------------- | :---------------- | :-------------------- | :------------------ | :--------------------------------------------------------------------- |
| Can be instantiated | No         | Unknown status | Unknown identifiability | Forbidden         | Allowed               | none                | [spack.schema.json\*](../out/spack.schema.json "open original schema") |

## verify\_spack Type

`boolean`

## verify\_spack Default Value

The default value is:

```json
true
```
