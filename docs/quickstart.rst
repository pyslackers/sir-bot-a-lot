===========
Quick Start
===========

.. note::

    The core Sir Bot-a-lot module does **NOTHING** without plugins.
    Check out the list of :ref:`available plugins`.

Installation
------------

Sir Bot-a-lot can be install with pip:

.. code-block:: console

    $ pip install sir-bot-a-lot

This is the preferred method as it will always install the most recent stable
release.

Configuration
-------------

To load a custom config file use the :code:`--config` argument or the
:code:`SIRBOT_CONFIG` environment variable with the configuration file path.

The default configuration file look like this:

.. code-block:: yaml

    sirbot:
        port: 8080
        plugins: []
    
Plugins can also be added with the :code:`--plugins` argument.

You can auto-generate a configuration file and a basic plugin with:

.. code-block:: console

    $ sirbot init

Start
-----

To start Sir Bot-a-lot use the command

.. code-block:: console

    $ sirbot --config path/to/config/file
