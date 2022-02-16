import os
import shlex
import shutil

from buildtest.builders.base import BuilderBase
from buildtest.tools.modules import get_module_commands
from buildtest.utils.file import write_file
from buildtest.utils.tools import deep_get


class ScriptBuilder(BuilderBase):
    """This is a subclass of BuilderBase used for building test that uses ``type: script`` in the buildspec."""

    type = "script"

    def __init__(
        self,
        name,
        recipe,
        buildspec,
        executor,
        buildexecutor,
        configuration,
        testdir=None,
        numprocs=None,
        numnodes=None,
        compiler=None,
    ):

        super().__init__(
            name=name,
            recipe=recipe,
            buildspec=buildspec,
            executor=executor,
            buildexecutor=buildexecutor,
            testdir=testdir,
            numprocs=numprocs,
            numnodes=numnodes,
            compiler=compiler,
        )
        self.compiler_settings = {"vars": None, "env": None, "modules": None}

        self.configuration = configuration
        self.compiler_section = self.recipe.get("compilers")

        # if 'compilers' property defined resolve compiler logic
        if self.compiler_section:
            self._process_compiler_config()
            self.resolve_compilers()

        self.status = deep_get(
            self.recipe, "executors", self.executor, "status"
        ) or self.recipe.get("status")
        self.metrics = deep_get(
            self.recipe, "executors", self.executor, "metrics"
        ) or self.recipe.get("metrics")

    def resolve_compilers(self):
        # get environment variables
        self.compiler_settings["env"] = deep_get(
            self.compiler_section, "config", self.compiler, "env"
        ) or deep_get(self.compiler_section, "default", self.compiler_group, "env")

        # get environment variables
        self.compiler_settings["vars"] = deep_get(
            self.compiler_section, "config", self.compiler, "vars"
        ) or deep_get(self.compiler_section, "default", self.compiler_group, "vars")

        # compiler set in compilers 'config' section, we try to get module lines using self._get_modules
        self.compiler_settings["modules"] = get_module_commands(
            deep_get(self.compiler_section, "config", self.compiler, "module")
        )

        if not self.compiler_settings["modules"]:
            self.compiler_settings["modules"] = get_module_commands(
                self.bc_compiler.get("module")
            )

    def write_python_script(self):
        """This method is used for writing python script when ``shell: python``
        is set. The content from ``run`` section is added into a python
        script. The file is written to run directory and we simply invoke
        python script by running ``python script.py``
        """

        python_content = self.recipe.get("run")
        script_path = "%s.py" % os.path.join(self.stage_dir, self.name)
        write_file(script_path, python_content)
        self.logger.debug(f"[{self.name}]: Writing python script to: {script_path}")
        shutil.copy2(
            script_path, os.path.join(self.test_root, os.path.basename(script_path))
        )
        self.logger.debug(
            f"[{self.name}]: Copying file: {script_path} to: {os.path.join(self.test_root, os.path.basename(script_path))}"
        )

        # lines = [f"python {script_path}"]
        # return lines

    def generate_script(self):
        """This method builds the content of the test script which will return a list
        of shell commands that will be written to file.

        A typical test will contain: shebang line, job directives, environment variables and variable declaration,
        and content of ``run`` property. For ``shell: python`` we write a python script and
        return immediately. The variables, environment section are not applicable
        for python scripts

        Returns:
            List of shell commands that will be written to file
        """

        # start of each test should have the shebang
        lines = [self.shebang]

        # if shell is python the generated testscript will be run via bash, we invoke
        # python script in bash script.
        if self.shell.name == "python":
            lines = ["#!/bin/bash"]

        sched_lines = self.get_job_directives()
        if sched_lines:
            lines += sched_lines

        if self.burstbuffer:

            burst_buffer_lines = self._get_burst_buffer(self.burstbuffer)
            if burst_buffer_lines:
                lines += burst_buffer_lines

        if self.datawarp:
            data_warp_lines = self._get_data_warp(self.datawarp)

            if data_warp_lines:
                lines += data_warp_lines

        # for python scripts we generate python script and return lines
        if self.shell.name == "python":
            self.logger.debug(f"[{self.name}]: Detected python shell")
            self.write_python_script()

            py_script = "%s.py" % format(os.path.join(self.stage_dir, self.name))

            python_wrapper = self.buildexecutor.executors[self.executor]._settings[
                "shell"
            ]
            python_wrapper_buildspec = shlex.split(self.recipe.get("shell"))[0]

            # if 'shell' property in buildspec specifies 'shell: python' or 'shell: python3' then we use this instead
            if python_wrapper_buildspec.endswith(
                "python"
            ) or python_wrapper_buildspec.endswith("python3"):
                python_wrapper = python_wrapper_buildspec

            lines.append(f"{python_wrapper} {py_script}")
            return lines

        # section below is for shell-scripts (bash, sh, csh, zsh, tcsh, zsh)

        if self.compiler:
            compiler_variables = {
                "BUILDTEST_CC": self.cc,
                "BUILDTEST_CXX": self.cxx,
                "BUILDTEST_FC": self.fc,
                "BUILDTEST_CFLAGS": self.cflags,
                "BUILDTEST_CXXFLAGS": self.cxxflags,
                "BUILDTEST_FFLAGS": self.fflags,
                "BUILDTEST_CPPFLAGS": self.cppflags,
                "BUILDTEST_LDFLAGS": self.ldflags,
            }
            lines += self._get_variables(compiler_variables)

            if self.compiler_settings["env"]:
                lines += self._get_environment(self.compiler_settings["env"])
            if self.compiler_settings["vars"]:
                lines += self._get_variables(self.compiler_settings["vars"])

        # Add environment variables
        env_section = deep_get(
            self.recipe, "executors", self.executor, "env"
        ) or self.recipe.get("env")
        var_section = deep_get(
            self.recipe, "executors", self.executor, "vars"
        ) or self.recipe.get("vars")

        env_lines = self._get_environment(env_section)
        if env_lines:
            lines += env_lines

        var_lines = self._get_variables(var_section)
        if var_lines:
            lines += var_lines

        if self.compiler_settings["modules"]:
            lines += self.compiler_settings["modules"]

        lines.append("# Content of run section")
        # Add run section
        lines += [self.recipe["run"]]

        return lines
