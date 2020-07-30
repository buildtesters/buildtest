from buildtest.schemas.utils import load_schema
import os

here = os.path.dirname(os.path.abspath(__file__))

global_schema_file = "global.schema.json"
global_schema = load_schema(os.path.join(here, global_schema_file))

script_schema_file = "script-v1.0.schema.json"
script_schema = load_schema(os.path.join(here, "script", script_schema_file))

compiler_schema_file = "compiler-v1.0.schema.json"
compiler_schema = load_schema(os.path.join(here, "compiler", compiler_schema_file))


schema_table = {}
schema_table["types"] = ["script", "compiler"]
schema_table["global"] = {}
schema_table["global"]["path"] = os.path.join(here, global_schema_file)
schema_table["global"]["recipe"] = global_schema
schema_table["script"] = {}
schema_table["script"]["versions"] = ["1.0"]
schema_table["script"]["path"] = os.path.join(here, "script", script_schema_file)
schema_table["script"]["recipe"] = script_schema
schema_table["compiler"] = {}
schema_table["compiler"]["versions"] = ["1.0"]
schema_table["compiler"]["path"] = os.path.join(here, "compiler", compiler_schema_file)
schema_table["compiler"]["recipe"] = compiler_schema
