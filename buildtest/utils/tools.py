from functools import reduce


def deep_get(dictionary, *keys):
    return reduce(
        lambda d, key: d.get(key, None) if isinstance(d, dict) else None,
        keys,
        dictionary,
    )


class Hasher(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    def get(self, path, sep=".", default=None):
        keys = path.split(sep)
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val

    def __str__(self):
        return str(dict(self))
