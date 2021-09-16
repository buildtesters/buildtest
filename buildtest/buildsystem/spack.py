"""This method defines the Spack buildsystem for the spack package manager (https://spack.readthedocs.io/en/latest/)
by generating scripts that will do various spack operation. The SpackBuilder class will generate a test script using the
schema definition 'spack-v1.0.schema.json' that defines how buildspecs are written.
"""

import os

from buildtest.buildsystem.base import BuilderBase
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import resolve_path
from buildtest.utils.tools import deep_get


class SpackBuilder(BuilderBase):
    """This is a subclass of BuilderBase used for building test that uses ``type: spack`` in the buildspec."""

    type = "spack"

    def __init__(
        self,
        name,
        recipe,
        buildspec,
        buildexecutor,
        executor,
        testdir=None,
    ):
        super().__init__(
            name=name,
            recipe=recipe,
            buildspec=buildspec,
            executor=executor,
            buildexecutor=buildexecutor,
            testdir=testdir,
        )
        self.status = deep_get(
            self.recipe, "executors", self.executor, "status"
        ) or self.recipe.get("status")
        self.metrics = deep_get(
            self.recipe, "executors", self.executor, "metrics"
        ) or self.recipe.get("metrics")
        self.generate_script()

    def generate_script(self):
        """Method responsible for generating the content of test script for spack buildsystem"""

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

        var_lines = self._get_variables(self.recipe.get("vars"))
        env_lines = self._get_environment(self.recipe.get("env"))

        if deep_get(self.recipe, "executors", self.executor, "env"):
            env_lines = self._get_environment(
                self.recipe["executors"][self.executor]["env"]
            )

        if deep_get(self.recipe, "executors", self.executor, "vars"):
            var_lines = self._get_variables(
                self.recipe["executors"][self.executor]["vars"]
            )

        if env_lines:
            lines += env_lines

        if var_lines:
            lines += var_lines

        if self.recipe.get("pre_cmds"):
            lines.append("\n")
            lines.append("######## START OF PRE COMMANDS ######## ")
            lines += [self.recipe["pre_cmds"]]
            lines.append("######## END OF PRE COMMANDS   ######## ")
            lines.append("\n")

        spack_configuration = self.recipe["spack"]
        if spack_configuration.get("root"):
            lines += [
                "source "
                + self._resolve_spack_root(
                    spack_configuration["root"], spack_configuration.get("verify_spack")
                )
            ]

        if spack_configuration.get("compiler_find"):
            lines.append("spack compiler find")

        # add spack mirror if mirror field is specified
        if spack_configuration.get("mirror"):
            for mirror_name, mirror_location in spack_configuration["mirror"].items():
                lines.append(f"spack mirror add {mirror_name} {mirror_location}")

        if spack_configuration.get("env"):
            lines += self._spack_environment(spack_configuration["env"])

        if spack_configuration.get("install"):
            opts = spack_configuration["install"].get("option") or ""

            if spack_configuration["install"].get("specs"):
                for spec in spack_configuration["install"]["specs"]:
                    lines.append(f"spack install {opts} {spec}")
            else:
                lines.append(f"spack install {opts}")

        if spack_configuration.get("test"):
            lines += self._spack_test(spack_configuration)

        if self.recipe.get("post_cmds"):
            lines.append("\n")
            lines.append("######## START OF POST COMMANDS ######## ")
            lines += [self.recipe["post_cmds"]]
            lines.append("######## END OF POST COMMANDS   ######## ")
            lines.append("\n")

        return lines

    def _spack_test(self, spack_configuration):
        """This method will return lines for generating ``spack test run`` and ``spack test results`` command for running tests via
        spack and getting results.
        """
        lines = []
        if spack_configuration["test"].get("remove_tests"):
            lines.append("spack test remove -y")

        spack_test_cmd = ["spack test run"]

        if spack_configuration["test"]["run"].get("option"):
            spack_test_cmd.append(spack_configuration["test"]["run"]["option"])

        run_specs = spack_configuration["test"]["run"]["specs"]

        spack_test_cmd.append(f"--alias {self.name}")

        for spec in run_specs:
            spack_test_cmd.append(spec)

        lines.append(" ".join(spack_test_cmd))

        opts = spack_configuration["test"]["results"].get("option") or ""
        # fetch results using 'spack test results <suite>'
        if spack_configuration["test"]["results"].get("suite"):
            for suite in spack_configuration["test"]["results"]["suite"]:
                lines.append(f"spack test results {opts} {suite}")

        # fetch results using 'spack test results -- <spec>'
        if spack_configuration["test"]["results"].get("specs"):
            for spec in spack_configuration["test"]["results"]["specs"]:
                lines.append(f"spack test results {opts} -- {spec}")

        return lines

    def _resolve_spack_root(self, path, verify_spack=True):
        """Given a path find the startup spack setup script to source.

        Args:
            path (str): Full path to root of spack directory
            verify_spack (bool, optional): Check for existence of spack setup script `$SPACK_ROOT/share/spack/setup-env.sh` before sourcing file. By default this check is enabled but can be disabled to allow test to run even if spack doesn't exist on filesystem.

        Raises:
            BuildTestError: Raise exception if root of spack doesn't exist or we are unable to resolve path to setup script `$SPACK_ROOT/share/spack/setup-env.sh`
        """

        spack_root = resolve_path(path, exist=verify_spack)

        if not spack_root:
            raise BuildTestError(
                f"Unable to find root of spack based on directory: {path}"
            )

        setup_script = os.path.join(spack_root, "share", "spack", "setup-env.sh")

        sourced_script = resolve_path(setup_script, exist=verify_spack)

        if not sourced_script:
            raise BuildTestError(
                f"Unable to find spack setup-env.sh script: {setup_script}"
            )
        return sourced_script

    def _spack_environment(self, spack_env):
        """This method is responsible for  creating a spack environment, activate an existing
        spack environment, create a spack environment from a directory and a manifest file (spack.yaml, spack.lock)

        Args:
            spack_env (dict): Contains property ``env`` from buildspec dictionary
        """

        # create spack environment ('spack env create')
        lines = []

        if spack_env.get("rm"):
            lines.append(f"spack env rm -y {spack_env['rm']['name']}")

        if spack_env.get("create"):

            opts = spack_env["create"].get("options") or ""
            cmd = ["spack env create", opts]

            # create spack environment from name
            if spack_env["create"].get("name"):

                # if remove_environment is defined we remove the environment before creating it
                if spack_env["create"].get("remove_environment"):
                    lines.append(f"spack env rm -y {spack_env['create']['name']}")

                cmd.append(spack_env["create"]["name"])

            # create spack envrionment from directory. Note we don't need to check if directory exist because spack will create the directory via `spack env create -d <dir>`
            elif spack_env["create"].get("dir"):
                env_dir = resolve_path(spack_env["create"]["dir"], exist=False)
                cmd += ["-d", env_dir]

            if spack_env["create"].get("manifest"):
                manifest = resolve_path(spack_env["create"]["manifest"], exist=False)
                cmd.append(manifest)

            spack_env_create_line = " ".join(cmd)
            lines += [spack_env_create_line]

        # activate environment ('spack env activate')
        if spack_env.get("activate"):
            opts = spack_env["activate"].get("options") or ""
            cmd = ["spack env activate", opts]
            # activate spack environment via name 'spack env activate <name>'
            if spack_env["activate"].get("name"):
                cmd.append(spack_env["activate"]["name"])

            # activate spack environment via directory 'spack env activate -d <dir>'
            elif spack_env["activate"].get("dir"):

                env_dir = resolve_path(spack_env["activate"]["dir"], exist=False)
                if not env_dir:
                    raise BuildTestError(
                        f"Unable to resolve directory: {spack_env['activate']['dir']} for activating spack environment via directory. Please specify a valid directory"
                    )
                cmd += ["-d", env_dir]

            spack_env_activate_line = " ".join(cmd)
            lines.append(spack_env_activate_line)

        # add spack mirror if mirror field is specified
        if spack_env.get("mirror"):
            for mirror_name, mirror_location in spack_env["mirror"].items():
                lines.append(f"spack mirror add {mirror_name} {mirror_location}")

        if spack_env.get("specs"):
            for spec in spack_env["specs"]:
                lines.append(f"spack add {spec}")

        if spack_env.get("concretize"):
            lines.append("spack concretize -f")
        return lines
