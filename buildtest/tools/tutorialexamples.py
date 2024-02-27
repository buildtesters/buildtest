import getpass
import os
import shutil
import sys

from buildtest.cli.clean import clean
from buildtest.config import SiteConfiguration
from buildtest.defaults import BUILDTEST_ROOT, TUTORIALS_SETTINGS_FILE
from buildtest.tools.docs import build_aws_examples, build_spack_examples
from buildtest.utils.file import create_dir, is_dir, is_file


def generate_tutorial_examples():
    """This method is the entry point for "buildtest tutorial-examples" command which generates
    documentation examples for Buildtest Tutorial.
    """

    if getpass.getuser() != "spack" or os.getenv("HOME") != "/home/spack":
        sys.exit(
            "This script can only be run inside container: ghcr.io/buildtesters/buildtest_spack:latest"
        )

    autogen_examples_dir = os.path.join(
        BUILDTEST_ROOT, "docs", "buildtest_tutorial_examples"
    )

    config = SiteConfiguration(settings_file=TUTORIALS_SETTINGS_FILE)
    config.detect_system()
    config.validate()

    if is_file(autogen_examples_dir):
        os.remove(autogen_examples_dir)

    if is_dir(autogen_examples_dir):
        shutil.rmtree(autogen_examples_dir)

    create_dir(autogen_examples_dir)

    clean(config, yes=True)
    build_spack_examples(autogen_examples_dir)


def generate_aws_examples():
    if getpass.getuser() != "ubuntu" or os.getenv("HOME") != "/home/ubuntu":
        sys.exit(
            "This script can only be run in AWS instance using E4SPro image. Please check the AWS Market Place: https://aws.amazon.com/marketplace for the image "
        )

    autogen_examples_dir = os.path.join(BUILDTEST_ROOT, "docs", "aws_examples")

    config = SiteConfiguration(
        settings_file=os.path.join(BUILDTEST_ROOT, "buildtest", "settings", "aws.yml")
    )
    config.detect_system(moduletool="environment-modules")
    config.validate()

    build_aws_examples(autogen_examples_dir)
