from buildtest.tools.testconfigs import func_testconfigs_show, func_testconfigs_view

def test_testconfigs_show():
    dict = {}
    func_testconfigs_show(dict)

"""
def test_testconfigs_view():
    dict = {
        "name": "tutorial.compilers.args.c.yml"
    }
    func_testconfigs_view(dict)
"""