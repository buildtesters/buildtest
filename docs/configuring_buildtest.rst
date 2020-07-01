.. _configuring_buildtest:

Configuring buildtest
======================

Schema File
------------

The schema file used for configuring and validating buildtest is done
by `settings.script.json <https://raw.githubusercontent.com/buildtesters/buildtest/devel/buildtest/settings/settings.schema.json>`_

For more details on schema attributes see `Settings Schema Documentation <https://buildtesters.github.io/schemas/settings/>`_


Default Settings
-----------------------

The default buildtest settings is found in ``buildtest/settings/settings.yml``. At
start of buildtest this file is copied to ``$HOME/.buildtest/settings.yml`` to
help you get started. You are expected to customize this file to best suit your
site configuration.

.. program-output:: cat ../buildtest/settings/settings.yml

Settings Example
-----------------

To retrieve a list of settings example you can run ``buildtest schema -n settings.schema.json -e``
which will show a listing a valid buildtest settings.

.. program-output:: cat docgen/schemas/settings-examples.txt

Settings Schema
-----------------

Shown below is the json schema for buildtest settings that can be retrieved via
``buildtest schema -n settings.schema.json -j``

.. program-output:: cat docgen/schemas/settings-json.txt


