=============
Configuration
=============

.. note::

    A configuration file and an empty plugin can be auto-generated using:

    .. code-block:: console

        $ sirbot init

Start
-----

To start Sir Bot-a-lot you can use one of:

.. code-block:: console

    $ sirbot

.. code-block:: console

    $ python run.py


Command line arguments
----------------------

The command line arguments take precedence over the environment variables.

* :code:`-h --help`: Help message
* :code:`-P --port`: Port where to run Sir Bot-a-lot
* :code:`-c --config`: Path to Sir Bot-a-lot Yaml config file
* :code:`-u --update`: Perform update migration if necessary (i.e. database)
* :code:`-p --plugins`: Plugins to start


Environment variables
---------------------

The environment variable take precedence over the configuration file.

* :code:`SIRBOT_PORT`: Port where to run Sir Bot-a-lot
* :code:`SIRBOT_CONFIG`: Path to Sir Bot-a-lot Yaml config file


Configuration file
------------------

Sir Bot-a-lot configuration is a Yaml file containing the core and all the
additional plugins configuration.

A basic configuration will look like this:

.. code-block:: yaml

    sirbot:
        port: 8080
        plugins: []
    plugin1:
        ...
    plugin2:
        ...

Plugins must be importable python modules. See :ref:`writing_plugins` for more
information.

.. _conf_starting_priority:

Starting priority
^^^^^^^^^^^^^^^^^

Plugins can depend on other plugins. You can ensure a startup order by setting
a startup priority. By default all plugins have a priority of 50. Plugins with
a higher priority will start before the one with a lower priority.

If multiple plugins have the same priority they will start simultaneously. A
priority of 0 or false will disable the plugin.

.. code-block:: yaml

    plugin1:
        priority: 80
    plugin2:
        priority: false

Logging
^^^^^^^

Logging can be configured in the :code:`logging` key of the configuration file.
It use the logging module `dictionnary configuration`_. By default the log
level is set to :code:`INFO`.

Each plugin should define his own logger. The core logger is :code:`sirbot.core`.

.. _dictionnary configuration: https://docs.python.org/3.5/library/logging.config.html#configuration-dictionary-schema

Import
------

To use Sir Bot-a-lot in a project:

.. code-block:: python

    from sirbot import SirBot
    bot = SirBot(config=config)
    bot.run(port=port)

