=====================
Usage & Configuration
=====================

Command Line
------------

To start Sir-bot-a-lot you can use:

.. code-block:: console

    $ sirbot

or:

.. code-block:: console

    $ python run.py



Arguments
^^^^^^^^^

The command line arguments take precedence over the configuration file.

* :code:`-h --help`: Help message
* :code:`-p --port`: Port where to run Sir-bot-a-lot
* :code:`-c --config`: Path to Sir-bot-a-lot Yaml config file


Environment variables
---------------------
The environment variable take precedence over the command line arguments and the
configuration file.

* :code:`SIRBOT_PORT`: Port where to run Sir-bot-a-lot
* :code:`SIRBOT_CONFIG`: Path to Sir-bot-a-lot Yaml config file


Configuration file
------------------

Sir-bot-a-lot configuration is a Yaml file containing the core and all the
plugins configuration.

The environment variable and command line arguments take precedence over the
configuration file.

A basic configuration will look like this:

.. code-block:: yaml

    port: 8080

    core:
      plugins:
      - plugin-1
      - plugin-2

    plugin-1:
        ...

    plugin-2:
        ...

Logging
^^^^^^^

Logging can be configured in the :code:`logging` key of the configuration file.
It use the logging module `dictionnary configuration`_.

Each plugin should define his own logger. The core logger is :code:`sirbot.core`.

.. _dictionnary configuration: https://docs.python.org/3.5/library/logging.config.html#configuration-dictionary-schema

Import
------

To use Sir-bot-a-lot in a project:

.. code-block:: python

    from sirbot import SirBot
    bot = SirBot(config=config)
    bot.run(port=port)

