=============
Sir-bot-a-lot
=============

|build| |coverage| |doc|

A slack bot built for the people and by the people of the `python developers slack community`_.

Want to join? `Get an invite`_ !

.. _Get an invite: http://pythondevelopers.herokuapp.com/
.. _python developers slack community: https://pythondev.slack.com/
.. |build| image:: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/badges/master/build.svg
    :alt: Build status
    :scale: 100%
    :target: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/commits/master
.. |coverage| image:: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/badges/master/coverage.svg
    :alt: Coverage status
    :scale: 100%
    :target: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/commits/master
.. |doc| image:: https://readthedocs.org/projects/sir-bot-a-lot/badge/?version=latest
    :alt: Documentation status
    :target: http://sir-bot-a-lot.readthedocs.io/en/latest/?badge=latest

Instalation
-----------

The sources for sir-bot-a-lot can be downloaded from the `gitlab repo`_.

.. code-block:: console

    $ git clone git://gitlab.com/PythonDevCommunity/sir-bot-a-lot

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install sir-bot-a-lot/

Run
---

To start Sir-bot-a-lot use the command

.. code-block:: console

    $ sirbot

By default no plugins are installed so Sir-bot-a-lot will not do anything.
Check out the `available plugins`_.

.. _gitlab repo: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot
.. _available plugins: http://sir-bot-a-lot.readthedocs.io/en/latest/plugins.html#available-plugins

Configuration
-------------

A basic configuration file will look like this:

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
