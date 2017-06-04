======
|icon|
======

|build| |doc|

A bot framework built for the people and by the people of the `python developers slack community`_.

The uses of bots are nearly endless and come in all shapes and sizes. They can handle Slack shenanigans, monitor the status of a crypto-currency, or become your personal assistant. sir-bot-a-lot can help you get started writing your own bot.

Want to join? `Get an invite`_ !

.. _Get an invite: http://pythondevelopers.herokuapp.com/
.. _python developers slack community: https://pythondev.slack.com/
.. |build| image:: https://travis-ci.org/pyslackers/sir-bot-a-lot.svg?branch=master
    :alt: Build status
    :target: https://travis-ci.org/pyslackers/sir-bot-a-lot
.. |doc| image:: https://readthedocs.org/projects/sir-bot-a-lot/badge/?version=latest
    :alt: Documentation status
    :target: http://sir-bot-a-lot.readthedocs.io/en/latest
.. |icon| image:: icon/icon-500.png
    :width: 10%
    :alt: Sir-bot-a-lot icon
    :target: http://sir-bot-a-lot.readthedocs.io/en/latest

Installation
------------

The sources for sir-bot-a-lot can be downloaded from the `github repo`_.

.. code-block:: console

    $ git clone https://github.com/pyslackers/sir-bot-a-lot.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install sir-bot-a-lot/

To install the development requirements do:

.. code-block:: console

    $ pip install sir-bot-a-lot/[dev]

Run
---

To start Sir-bot-a-lot use the command

.. code-block:: console

    $ sirbot

By default no plugins are installed so Sir-bot-a-lot will do nothing.
Check out the `available plugins`_.

.. _github repo: https://github.com/pyslackers/sir-bot-a-lot
.. _available plugins: http://sir-bot-a-lot.readthedocs.io/en/latest/plugins.html#available-plugins

Configuration
-------------

To load a custom file use the ``--config`` argument or the ``SIRBOT_CONFIG`` environment variable with the configuration file path.

The default configuration file look like this:

.. code-block:: yaml

    sirbot:
      port: 8080
      plugins: []

Plugins can also be added with the ``--plugins`` argument
