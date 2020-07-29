from buildtest.buildsystem.schemas.utils import here, load_schema
import os
here = os.path.dirname(os.path.abspath(__file__))
global_schema_file = "global.schema.json"
global_schema = load_schema(os.path.join(here, global_schema_file))