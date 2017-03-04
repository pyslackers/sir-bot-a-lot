.. _configuration:

=============
Configuration
=============

Sir-bot-a-lot configuration is a Yaml file containing the core and all the plugins
configuration.

The environment variable and command line arguments take precedence over the
configuration file.

Environment variables
---------------------

The environment variable take precedence over the command line arguments and the
configuration file.

* :code:`SIRBOT_PORT`: Port where to run Sir-bot-a-lot
* :code:`SIRBOT_CONFIG`: Path to Sir-bot-a-lot Yaml config file

Command line arguments
----------------------

The command line arguments take precedence over the configuration file.

* :code:`-h --help`: Help message
* :code:`-p --port`: Port where to run Sir-bot-a-lot
* :code:`-c --config`: Path to Sir-bot-a-lot Yaml config file

Configuration file
------------------

example
^^^^^^^

A basic configuration will look like this:

.. code-block:: yaml

    loglevel: 10
    port: 8080

    core:
      loglevel: 10
      plugins:
      - plugin-1
      - plugin-2

    plugin-1:
      loglevel: 10

    plugin-2:
      loglevel: 10
