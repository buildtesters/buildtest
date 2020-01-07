from buildtest.tools.testconfigs import func_testconfigs_show, func_testconfigs_view

def test_testconfigs_show():
    dict = {}
    func_testconfigs_show(dict)

"""
def test_testconfigs_view():
    parser = argparse.ArgumentParser()
    parser.add_argument("name",type=str)
    args = parser.parse_args(['name'="tutorial.compilers.args.c.yml"])
    print(args,args.name)
    func_testconfigs_view(args)
"""