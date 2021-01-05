import os
import shutil

from buildtest.buildsystem.base import BuilderBase
from buildtest.defaults import executor_root
from buildtest.utils.file import write_file


class ScriptBuilder(BuilderBase):
    type = "script"

    def write_python_script(self):
        """ This method is used for writing python script when ``shell: python``
            is set. The content from ``run`` section is added into a python
            script. The file is written to run directory and we simply invoke
            python script by running ``python script.py``
       """

        python_content = self.recipe.get("run")
        script_path = "%s.py" % os.path.join(self.stage_dir, self.name)
        write_file(script_path, python_content)
        shutil.copy2(
            script_path, os.path.join(self.run_dir, os.path.basename(script_path))
        )
        lines = [f"python {script_path}"]
        return lines

    def generate_script(self):
        """ This method builds the testscript content based on the builder type.
            For ScriptBuilder we need to add the shebang, environment variables
            and the run section. If shell is python we write a python script and
            return immediately. The variables, environment section are not applicable
            for python scripts

            :return: return content of test script
            :rtype: list
        """

        self.status = self.recipe.get("status")

        # start of each test should have the shebang
        lines = [self.shebang]

        # if shell is python the generated testscript will be run via bash, we invoke
        # python script in bash script.
        if self.shell.name == "python":
            lines = [self.default_shell.shebang]

        batch_directives_lines = self._get_scheduler_directives(
            bsub=self.recipe.get("bsub"),
            sbatch=self.recipe.get("sbatch"),
            cobalt=self.recipe.get("cobalt"),
            batch=self.recipe.get("cobalt"),
        )
        if batch_directives_lines:
            lines += batch_directives_lines

        burst_buffer_lines = self._get_burst_buffer(self.recipe.get("BB"))
        if burst_buffer_lines:
            lines += burst_buffer_lines

        data_warp_lines = self._get_data_warp(self.recipe.get("DW"))
        if data_warp_lines:
            lines += data_warp_lines

        lines += [
            f"source {os.path.join(executor_root, self.executor, 'before_script.sh')}"
        ]

        # for python scripts we generate python script and return lines
        if self.shell.name == "python":
            lines += self.write_python_script()
            lines += [
                f"source {os.path.join(executor_root, self.executor, 'after_script.sh')}"
            ]

            return lines

        # section below is for shell-scripts (bash, sh, csh, zsh, tcsh, zsh)

        # Add environment variables
        lines += self.get_environment(self.recipe.get("env"))

        # Add variables
        lines += self.get_variables(self.recipe.get("vars"))

        # Add run section
        lines += [self.recipe.get("run")]

        lines += [
            f"source {os.path.join(executor_root, self.executor, 'after_script.sh')}"
        ]

        return lines
