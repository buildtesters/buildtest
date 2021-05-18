import json
import os
import shutil

from buildtest.buildsystem.base import BuilderBase
from buildtest.exceptions import BuildTestError
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.utils.file import resolve_path
from buildtest.utils.tools import deep_get


class CompilerBuilder(BuilderBase):
    type = "compiler"

    # Fortran Extensions Links:
    # https://software.intel.com/content/www/us/en/develop/documentation/fortran-compiler-developer-guide-and-reference/top/compiler-setup/using-the-command-line/understanding-file-extensions.html
    # Fortran Extensions: http://fortranwiki.org/fortran/show/File+extensions
    lang_ext_table = {
        ".c": "C",
        ".cc": "C++",
        ".cxx": "C++",
        ".cpp": "C++",
        ".c++": "C++",
        ".f90": "Fortran",
        ".F90": "Fortran",
        ".f95": "Fortran",
        ".f03": "Fortran",
        ".f": "Fortran",
        ".F": "Fortran",
        ".FOR": "Fortran",
        ".for": "Fortran",
        ".FTN": "Fortran",
        ".ftn": "Fortran",
    }

    cc = None
    cxx = None
    fc = None
    ldflags = None
    cflags = None
    cxxflags = None
    fflags = None
    cppflags = None

    def __init__(
        self,
        name,
        recipe,
        buildspec,
        buildexecutor,
        executor,
        configuration,
        compiler=None,
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
        self.compiler = compiler
        self.configuration = configuration
        self.metadata["compiler"] = compiler

        self.compiler_section = self.recipe["compilers"]

        self.sourcefile = self.recipe["source"]

    def setup(self):
        """The setup method is responsible for process compiler section, getting modules
        pre_build, post_build, pre_run, post_run section and generate compilation
        and run command. This method invokes other methods and set values in class
        variables. This method is called by self.generate_script method.
        """

        self._resolve_source()
        self.lang = self._detect_lang(self.sourcefile)
        # set executable name and assign to self.executable
        self.executable = "%s.exe" % os.path.basename(self.sourcefile)
        self.exec_variable = f"_EXEC={self.executable}"

        self._process_compiler_config()

        # get environment variables
        self.envvars = (
            deep_get(self.compiler_section, "config", self.compiler, "env")
            or deep_get(self.compiler_section, "default", self.compiler_group, "env")
            or deep_get(self.compiler_section, "default", "all", "env")
        )

        # get environment variables
        self.vars = (
            deep_get(self.compiler_section, "config", self.compiler, "vars")
            or deep_get(self.compiler_section, "default", self.compiler_group, "vars")
            or deep_get(self.compiler_section, "default", "all", "vars")
        )

        # get status
        self.status = (
            deep_get(self.compiler_section, "config", self.compiler, "status")
            or deep_get(self.compiler_section, "default", self.compiler_group, "status")
            or deep_get(self.compiler_section, "default", "all", "status")
        )

        # compiler set in compilers 'config' section, we try to get module lines using self._get_modules
        self.modules = self._get_modules(
            deep_get(self.compiler_section, "config", self.compiler, "module")
        )

        if not self.modules:
            self.modules = self._get_modules(self.bc_compiler.get("module"))

        self.pre_build = (
            deep_get(self.compiler_section, "config", self.compiler, "pre_build")
            or deep_get(
                self.compiler_section, "default", self.compiler_group, "pre_build"
            )
            or deep_get(self.compiler_section, "default", "all", "pre_build")
        )

        self.post_build = (
            deep_get(self.compiler_section, "config", self.compiler, "post_build")
            or deep_get(
                self.compiler_section, "default", self.compiler_group, "post_build"
            )
            or deep_get(self.compiler_section, "default", "all", "post_build")
        )

        self.pre_run = (
            deep_get(self.compiler_section, "config", self.compiler, "pre_run")
            or deep_get(
                self.compiler_section, "default", self.compiler_group, "pre_run"
            )
            or deep_get(self.compiler_section, "default", "all", "pre_run")
        )

        self.post_run = (
            deep_get(self.compiler_section, "config", self.compiler, "post_run")
            or deep_get(
                self.compiler_section, "default", self.compiler_group, "post_run"
            )
            or deep_get(self.compiler_section, "default", "all", "post_run")
        )

        self.compile_cmd = self._compile_cmd()

        self.run_cmd = self._run_cmd()

    def generate_script(self):
        """This method is responsible for generating test script for compiler schema.
        The method ``generate_script`` is implemented in each subclass because
        implementation on test generation differs across schema types.

        This method will add the lines into list which comprise content
        of test. The method will return a list containing lines of test script.
        """

        self.setup()

        # every test starts with shebang line
        lines = [self.shebang]

        batch_dict = {}
        cray_dict = {}

        # get sbatch, bsub, cobalt, pbs, batch property and store in batch dictionary.
        # The order of lookup is in order of precedence
        for batch in ["sbatch", "bsub", "cobalt", "pbs", "batch"]:
            batch_dict[batch] = (
                deep_get(self.compiler_section, "config", self.compiler, batch)
                or deep_get(
                    self.compiler_section, "default", self.compiler_group, batch
                )
                or deep_get(self.compiler_section, "default", "all", batch)
            )

        batch_directives_lines = self._get_scheduler_directives(
            bsub=batch_dict["bsub"],
            sbatch=batch_dict["sbatch"],
            cobalt=batch_dict["cobalt"],
            pbs=batch_dict["pbs"],
            batch=batch_dict["batch"],
        )

        if batch_directives_lines:
            lines += batch_directives_lines

        # get cray burst buffer (BB) and datawarp (DW) fields in order of precedence.
        for name in ["BB", "DW"]:
            cray_dict[name] = (
                deep_get(self.compiler_section, "config", self.compiler, name)
                or deep_get(self.compiler_section, "default", self.compiler_group, name)
                or deep_get(self.compiler_section, "default", "all", name)
            )

        burst_buffer_lines = self._get_burst_buffer(cray_dict["BB"])

        if burst_buffer_lines:
            lines += burst_buffer_lines

        data_warp_lines = self._get_data_warp(cray_dict["DW"])

        if data_warp_lines:
            lines += data_warp_lines

        lines += [self.exec_variable]

        lines += self._get_environment(self.envvars)
        # get variables
        lines += self._get_variables(self.vars)

        # if 'module' defined in Buildspec add modules to test
        if self.modules:
            lines += self.modules

        if self.pre_build:
            lines.append(self.pre_build)

        lines.append(self.compile_cmd)

        if self.post_build:
            lines.append(self.post_build)

        if self.pre_run:
            lines.append(self.pre_run)

        # add run command
        lines.append(self.run_cmd)

        if self.post_run:
            lines.append(self.post_run)

        return lines

    def _resolve_source(self):
        """This method resolves full path to source file, it checks for absolute
        path first before checking relative path that is relative to
        Buildspec recipe.
        """

        # attempt to resolve path based on 'source' field.
        # 1. The source file can be absolute path and if exists we use this
        # 2. The source file can be relative path to where buildspec is located

        self.abspath_sourcefile = resolve_path(self.sourcefile) or resolve_path(
            os.path.join(os.path.dirname(self.buildspec), self.sourcefile)
        )

        # raise error if we can't find source file to compile
        if not self.abspath_sourcefile:
            raise BuildTestError(
                f"Failed to resolve path specified in field 'source': {self.sourcefile}"
            )

    def _detect_lang(self, sourcefile):
        """This method will return the Programming Language based by looking up
        file extension of source file.
        """
        self.logger.debug(
            f"[{self.name}]: Detecting programming language for source file: {sourcefile}"
        )

        ext = os.path.splitext(sourcefile)[1]

        self.logger.debug(
            f"Found file extension: {ext}, now we will attempt to lookup programming language based on extension"
        )

        # if ext not in self.lang_ext_table then raise an error. This table consist of all file extensions that map to a Programming Language
        if ext not in self.lang_ext_table:
            raise BuildTestError(
                f"[{self.name}]: Unable to detect Program Language based on extension: {ext} in source: {sourcefile}"
            )
        # Set Programming Language based on ext. Programming Language could be (C, C++, Fortran)
        lang = self.lang_ext_table[ext]
        self.logger.debug(
            f"[{self.name}]: Based on extension: {ext} the programming language is: {lang}"
        )

        return lang

    def _get_modules(self, modules):
        """Return a list of module command as a list of instructions based on
        ``module`` property.

         :param modules: 'module' property specified in buildspec used for loading/swapping modules
         :type modules: object

        """

        if not modules:
            return

        module_cmd = []

        assert isinstance(modules, dict)

        # if purge is True and defined add module purge
        if modules.get("purge"):
            module_cmd += ["module purge"]
        #
        if modules.get("load"):
            for name in modules.get("load"):
                module_cmd += [f"module load {name}"]

        if modules.get("swap"):
            module_cmd += [f"module swap {' '.join(modules.get('swap'))}"]

        if modules.get("restore"):
            module_cmd += [f"module restore {modules.get('restore')}"]
        return module_cmd

    def _compile_cmd(self):
        """This method generates the compilation line and returns the output as
        a list. The compilation line depends on the the language detected
        that is stored in variable ``self.lang``.
        """

        cmd = []
        # Generate C compilation line
        if self.lang == "C":
            cmd = [
                self.cc,
                self.cppflags,
                self.cflags,
                "-o $_EXEC",
                self.abspath_sourcefile,
                self.ldflags,
            ]

        # Generate C++ compilation line
        elif self.lang == "C++":
            cmd = [
                self.cxx,
                self.cppflags,
                self.cxxflags,
                "-o $_EXEC",
                self.abspath_sourcefile,
                self.ldflags,
            ]

        # Generate Fortran compilation line
        elif self.lang == "Fortran":
            cmd = [
                self.fc,
                self.cppflags,
                self.fflags,
                "-o $_EXEC",
                self.abspath_sourcefile,
                self.ldflags,
            ]

        # remove any None from list
        cmd = list(filter(None, cmd))
        cmd = " ".join(cmd)

        return cmd

    def _run_cmd(self):
        """This method builds the run command which refers to how to run the
        generated binary after compilation.
        """

        # order of precedence on how to generate run line when executing binary.
        # 1. Check in 'config' section within compiler
        # 2. Check in 'default' section within compiler group
        # 3. Check in 'default' section within 'all' section
        # 4. Last resort run binary standalone
        run_line = (
            deep_get(self.compiler_section, "config", self.compiler, "run")
            or deep_get(self.compiler_section, "default", self.compiler_group, "run")
            or deep_get(self.compiler_section, "default", "all", "run")
            or "./$_EXEC"
        )
        return run_line

    def _process_compiler_config(self):
        """This method is responsible for setting cc, fc, cxx class variables based
        on compiler selection. The order of precedence is ``config``, ``default``,
        then buildtest setting. Compiler settings in 'config' takes highest precedence,
        this overrides any configuration in 'default'. Finally we resort to compiler
        configuration in buildtest setting if none defined. This method is responsible
        for setting cc, fc, cxx, cflags, cxxflags, fflags, ldflags, and cppflags.
        """
        bc = BuildtestCompilers(configuration=self.configuration)

        self.compiler_group = bc.compiler_name_to_group[self.compiler]
        self.logger.debug(
            f"[{self.name}]: compiler: {self.compiler} belongs to compiler group: {self.compiler_group}"
        )

        # compiler from buildtest settings
        self.bc_compiler = self.configuration.target_config["compilers"]["compiler"][
            self.compiler_group
        ][self.compiler]

        self.logger.debug(self.bc_compiler)
        # set compiler values based on 'default' property in buildspec. This can override
        # compiler setting defined in configuration file. If default is not set we load from buildtest settings for appropriate compiler.

        # set compiler variables to ones defined in buildtest configuration
        self.cc = self.bc_compiler["cc"]
        self.cxx = self.bc_compiler["cxx"]
        self.fc = self.bc_compiler["fc"]

        self.logger.debug(
            f"[{self.name}]: Compiler setting for {self.compiler} from configuration file"
        )
        self.logger.debug(
            f"[{self.name}]: {self.compiler}: {json.dumps(self.bc_compiler, indent=2)}"
        )

        # if default compiler setting provided in buildspec let's assign it.
        if deep_get(self.compiler_section, "default", self.compiler_group):

            self.cc = (
                self.compiler_section["default"][self.compiler_group].get("cc")
                or self.cc
            )

            self.fc = (
                self.compiler_section["default"][self.compiler_group].get("fc")
                or self.fc
            )

            self.cxx = (
                self.compiler_section["default"][self.compiler_group].get("cxx")
                or self.fc
            )

            self.cflags = self.compiler_section["default"][self.compiler_group].get(
                "cflags"
            )
            self.cxxflags = self.compiler_section["default"][self.compiler_group].get(
                "cxxflags"
            )
            self.fflags = self.compiler_section["default"][self.compiler_group].get(
                "fflags"
            )
            self.ldflags = self.compiler_section["default"][self.compiler_group].get(
                "ldflags"
            )
            self.cppflags = self.compiler_section["default"][self.compiler_group].get(
                "cppflags"
            )
        # if compiler instance defined in config section read from buildspec. This overrides default section if specified
        if deep_get(self.compiler_section, "config", self.compiler):

            self.logger.debug(
                f"[{self.name}]: Detected compiler: {self.compiler} in 'config' scope overriding default compiler group setting for: {self.compiler_group}"
            )

            self.cc = (
                self.compiler_section["config"][self.compiler].get("cc") or self.cc
            )
            self.fc = (
                self.compiler_section["config"][self.compiler].get("fc") or self.fc
            )
            self.cxx = (
                self.compiler_section["config"][self.compiler].get("cxx") or self.cxx
            )
            self.cflags = (
                self.compiler_section["config"][self.compiler].get("cflags")
                or self.cflags
            )
            self.cxxflags = (
                self.compiler_section["config"][self.compiler].get("cxxflags")
                or self.cxxflags
            )
            self.fflags = (
                self.compiler_section["config"][self.compiler].get("fflags")
                or self.fflags
            )
            self.cppflags = (
                self.compiler_section["config"][self.compiler].get("cppflags")
                or self.cppflags
            )
            self.ldflags = (
                self.compiler_section["config"][self.compiler].get("ldflags")
                or self.ldflags
            )

        self.logger.debug(
            f"cc: {self.cc}, cxx: {self.cxx} fc: {self.fc} cppflags: {self.cppflags} cflags: {self.cflags} fflags: {self.fflags} ldflags: {self.ldflags}"
        )
        # this condition is a safety check before compiling code to ensure if all C, C++, Fortran compiler not set we raise error
        if not self.cc and not self.cxx and not self.fc:
            raise BuildTestError(
                "Unable to set C, C++, and Fortran compiler wrapper, please specify 'cc', 'cxx','fc' in your compiler settings in buildtest configuration or specify in buildspec file. "
            )

    def set_cc(self, cc):
        self.cc = cc

    def set_cxx(self, cxx):
        self.cxx = cxx

    def set_fc(self, fc):
        self.fc = fc

    def set_cflags(self, cflags):
        self.cflags = cflags

    def set_fflags(self, fflags):
        self.fflags = fflags

    def set_cxxflags(self, cxxflags):
        self.cxxflags = cxxflags

    def set_cppflags(self, cppflags):
        self.cppflags = cppflags

    def set_ldflags(self, ldflags):
        self.ldflags = ldflags

    def get_cc(self):
        return self.cc

    def get_cxx(self):
        return self.cxx

    def get_fc(self):
        return self.fc

    def get_cflags(self):
        return self.cflags

    def get_cxxflags(self):
        return self.cxxflags

    def get_fflags(self):
        return self.fflags

    def get_cppfilags(self):
        return self.cppflags

    def get_ldflags(self):
        return self.ldflags

    def get_path(self):
        """This method returns the full path for C, C++, Fortran compilers"""

        path = {
            self.cc: shutil.which(self.cc),
            self.cxx: shutil.which(self.cxx),
            self.fc: shutil.which(self.fc),
        }
        return path
