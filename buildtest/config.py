import json
import os
import shutil
import sys
import yaml

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from buildtest import BUILDTEST_VERSION
from buildtest.utils.file import create_dir
from buildtest.defaults import (
    system    
    BUILDTEST_BUILD_LOGFILE,
    BUILDTEST_CONFIG_FILE,
    BUILDTEST_CONFIG_BACKUP_FILE,
    BUILDTEST_ROOT,
    DEFAULT_CONFIG_FILE,
    DEFAULT_CONFIG_SCHEMA,
    EDITOR_LIST,
    
)
from buildtest.buildsystem.schemas.utils import load_schema


def create_config_files():
    """If default config files don't exist, create them."""

    if not os.path.exists(BUILDTEST_CONFIG_FILE):
        shutil.copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_FILE)
        shutil.copy(DEFAULT_CONFIG_FILE, BUILDTEST_CONFIG_BACKUP_FILE)


def create_logfile():
    """Create a logfile to keep track of messages for the user, if doesn't exist."""

    if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
        build_dict = {"build": {}}
        with open(BUILDTEST_BUILD_LOGFILE, "w") as outfile:
            json.dump(build_dict, outfile, indent=2)


def init():
    """Buildtest init should check that the buildtest user root exists,
       and that dependency files are created. This is called by 
       load_configuration.
    """

    # check if $HOME/.buildtest exists, if not create directory
    if not os.path.exists(BUILDTEST_ROOT):
        print(
            f"Creating buildtest configuration directory: \
                 {BUILDTEST_ROOT}"
        )
        os.mkdir(BUILDTEST_ROOT)

    # Create subfolders for var and root
    create_dir(os.path.join(BUILDTEST_ROOT, "var"))
    create_dir(os.path.join(BUILDTEST_ROOT, "root"))
    create_dir(os.path.join(BUILDTEST_ROOT, "site"))

    # Create config files, module files, and log file
    create_config_files()
    create_logfile()


def check_configuration():
    """Checks all keys in configuration file (``settings.json``) are valid
       against schema ``config_schema.json``. If there are any errors during schema check
       an exception of type ``ValidationError`` will be raised.

       :raises ValidationError: ``jsonschema.validate`` will raise ValidationError if validation check fails against given schema.

       :return: returns gracefully if all checks passes otherwise terminate immediately
       :rtype: exit code 1 if checks failed
    """

    config_schema = load_schema(DEFAULT_CONFIG_SCHEMA)
    try:
        validate(instance=config_opts, schema=config_schema)
    except ValidationError:
        sys.exit(
            "Buildtest Configuration Check Failed! \n"
            + f"Configuration File: {BUILDTEST_CONFIG_FILE} failed to validate against schema: {DEFAULT_CONFIG_SCHEMA}"
        )
    
    validate_queues(config_opts["queues"],system)        

def load_configuration(config_path=None):
    """Load the default configuration file.
    
       Parameters:

       :param config_path: Path to buildtest configuration file (json)
       :type config_path: str, optional

    """
    init()

    config_path = config_path or BUILDTEST_CONFIG_FILE

    # load the configuration file
    config_opts = load_schema(config_path)

    return config_opts


# Run on init, so we only load once
config_opts = load_configuration()

supported_launcher_dict = {
    "local": ["local", "mpirun", "mpiexec"],
    "slurm": ["mpirun", "mpiexec", "srun"]
}

def validate_queues(config_queues)
    """This method will validate queues defined in buildtest configuration with queue semantic. 
       A queue type will be validated against the supported launcher type defined in configuration.          
    """
    
    for queue in config_queue:
        if queue["scheduler"] == "local":
            validate_local_scheduler(queue["launcher"])                        
            
        elif queue["scheduler"] == "slurm":
            system["slurm"]["partitions"]

def validate_local_scheduler(launcher):
    """This method will check launcher type for ``scheduler: local`` defined in configuration file.
       Valid launchers for local scheduler are ``local``, ```mpiexec``, ``mpirun``. If launcher 
       type is not of supported type we exit immediately. Furthermore we check that mpiexec and mpirun
       are in $PATH so we can use them. 


    
       :return: 
    """
    # if mpiexec is not found in $PATH we can't use mpiexec as a launcher type
    if launcher == "mpiexec" and system["mpiexec"] is None:
        sys.exit("Can't find binary 'mpiexec' in $PATH")

    # if mpirun is not found in $PATH we can't use mpirun as a launcher type
    if launcher == "mpirun" and system["mpirun"] is None:
        sys.exit("Can't find binary 'mpirun' in $PATH")

    if launcher is not in supported_launcher_dict["local"]:
        sys.exit(f"Invalid launcher type: {launcher} for scheduler: local \n" +
                 f"Supported Launchers for scheduler: local {supported_launcher_dict['local']}"
        )