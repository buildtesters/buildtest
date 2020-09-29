from buildtest.menu.build import discover_buildspecs

tagname = ["tutorials"]
print(f"Searching by tagname: {tagname}")
included_bp, excluded_bp = discover_buildspecs(tags=tagname)
print("\n Discovered buildspecs: \n")
[print(f) for f in included_bp]
