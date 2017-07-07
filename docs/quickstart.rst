===========
Quick Start
===========

.. note::

    The core sir-bot-a-lot module does **NOTHING** without plugins.
    Check out the list of :ref:`available plugins`.

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

Configuration
-------------

To load a custom config file use the :code:`--config` argument or the :code:`SIRBOT_CONFIG` environment variable with the configuration file path.

The default configuration file look like this:

.. code-block:: yaml

    sirbot:
        port: 8080
        plugins: []
    
Plugins can also be added with the :code:`--plugins` argument


Start
-----

To start Sir Bot-a-lot use the command

.. code-block:: console

    $ sirbot --config path/to/config/file
