==========
Quickstart
==========

A slack bot built for the people and by the people of the python developers slack community. https://pythondev.slack.com/

Want to contribute?
Get an invite!
http://pythondevelopers.herokuapp.com/

Instalation
-----------

The sources for sir-bot-a-lot can be downloaded from the `gitlab repo`_.

.. code-block:: console

    $ git clone git://gitlab.com/PythonDevCommunity/sir-bot-a-lot


Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

More installation instruction can be found :ref:`here <installation>`.

.. _gitlab repo: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot

Start
-----

To start Sir-bot-a-lot use the command

.. code-block:: console

    $ python run.py -c <configuration-file>

By default no plugins are installed so Sir-bot-a-lot will not do anything.
Check out the :ref:`available module page <available_modules>`.

Configuration
-------------

The `configuration file`_ is where you tell which plugins to be load.

A basic configuration will look like this:

.. code-block:: yaml

    loglevel: 10
    core:
      loglevel: 10
      plugins:
        - sirbot-plugin-slack

.. _configuration file: https://gitlab.com/PythonDevCommunity/sir-bot-a-lot/blob/master/sirbot.yml
