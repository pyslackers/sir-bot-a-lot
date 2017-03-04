.. _configuration:

=============
Configuration
=============

Sir-bot-a-lot configuration is a Yaml file containing the core and all the plugins
configuration.

The environment variable and command line arguments take precedence over the
configuration file.

example
-------

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
