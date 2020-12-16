import os
import shutil

from buildtest.buildsystem.base import BuilderBase
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

        # for python scripts we generate python script and return lines
        if self.shell.name == "python":
            lines = self.write_python_script()
            return lines

        # section below is for shell script content (bash, sh, csh, tcsh, zsh)
        lines = []

        # Add environment variables
        lines += self.get_environment()

        # Add variables
        lines += self.get_variables()

        # Add run section
        lines += [self.recipe.get("run")]

        return lines
