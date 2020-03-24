import json
import sys

from buildtest.defaults import supported_schemas
from buildtest.menu.config import show_configuration
from buildtest.buildsystem.schemas.utils import (
    load_schema,
    get_schemas_available,
    get_schema_fullpath,
)


def show_schema_layout(args):
    """Implements method ``buildtest show schema``"""

    # buildtest show schema --name script
    if args.name is None:
        sys.exit("Please provide the name of a schema (e.g., script) to show.")

    # Must be supported
    if args.name not in supported_schemas:
        sys.exit(
            "%s is not a supported schema. Options include %s"
            % (args.name, "\n".join(supported_schemas))
        )

    schema = get_schemas_available()[args.name]
    version = args.version or "latest"

    if version not in schema:
        print("Warning, %s is not a known version, showing latest." % version)

    schema = get_schema_fullpath(schema.get(version, schema.get("latest")))
    schema = load_schema(schema)
    print(json.dumps(schema, indent=4))
