from buildtest.executors.local import LocalExecutor


class ContainerExecutor(LocalExecutor):
    type = "container"
