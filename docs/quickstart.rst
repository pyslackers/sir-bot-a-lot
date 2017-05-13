===========
Quick Start
===========

Installation
------------

The sources for Sir Bot-a-lot can be downloaded from the `github repo`_.

.. code-block:: console

    $ git clone https://github.com/pyslackers/sir-bot-a-lot.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install sir-bot-a-lot/

More installation instruction can be found :ref:`here <installation>`.

.. _github repo: https://github.com/pyslackers/sir-bot-a-lot

Run
---

To start Sir Bot-a-lot use the command

.. code-block:: console

    $ sirbot

By default no plugins are installed so Sir Bot-a-lot will not do anything.
Check out the :ref:`available plugins page <available_plugins>`.

Configuration
-------------

To load a custom config file use the :code:`--config` argument or the :code:`SIRBOT_CONFIG` environment variable with the configuration file path.

The default configuration file look like this:

.. code-block:: yaml

    sirbot:
    port: 8080
    plugins: []
    
Plugins can also be added with the `--plugins` argument
