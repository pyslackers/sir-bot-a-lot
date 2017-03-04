=====
Usage
=====

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
^^^^^^^^^^^^^^^^^^^^^

The environment variable take precedence over the command line arguments and the
configuration file.

* :code:`SIRBOT_PORT`: Port where to run Sir-bot-a-lot
* :code:`SIRBOT_CONFIG`: Path to Sir-bot-a-lot Yaml config file

Import
------

To use Sir-bot-a-lot in a project:

.. code-block:: python

    from sirbot import SirBot
    bot = SirBot(config=config)
    bot.run(port=port)
