=======
Modules
=======

Available modules
-----------------

 * A Slack module is available in the `pythondev gitlab repo`_

.. _pythondev gitlab repo: https://gitlab.com/PythonDevCommunity/sirbot-plugin-slack

Writing a module
----------------

Sir-bot-a-lot is build onto the `pluggy`_ library for plugins management.

Two hooks are used. Ths first one to load the clients and the second one to load
the dispatchers.


Clients
^^^^^^^

The client is the part of a module receiving data from the outside world.

The hook is passed the loop and the incoming data queue and must return a tuple consisting of the plugin name and the client class.

.. code-block:: python

    from sirbot.hookimpl import hookimpl

    @hookimpl
    def clients(loop, queue):
        return METADATA['name'], Client(loop=loop, queue=queue)

The client class must have a connect method which will be called at startup with the configuration of the plugin.
This function keep running as an async tasks and should put a tuple consisting of the plugin name and the incoming data in the queue every times it's needed.

.. _pluggy: https://github.com/pytest-dev/pluggy


Dispatcher
^^^^^^^^^^

The dispatcher is the part of a module sending data to the outside world

The hook is passed the loop and must return a tuple consisting of the plugin name and the dispatcher class

.. code-block:: python

    from sirbot.hookimpl import hookimpl

    @hookimpl
    def dispatchers(loop):
        return METADATA['name'], Dispatcher(loop=loop)

A dispatcher need to have three method:

.. code-block:: python

    def configure(self, config):
        """
        Configure the plugin

        This method is called by the core after initialization
        :param config: configuration relevant to the plugin
        """

.. code-block:: python

    async def incoming(self, msg, plugin_facade, facades):
        """
        Handle the incoming message

        This method is called for every incoming messages
        """

.. code-block:: python

    def facade(self):
        """
        Initialize and return a new facade

        This is called by the core for each incoming message and when
        another plugin request this plugin facade
        """

Facade
^^^^^^

Each dispatcher should provide a facade which can be used to interact with itself and the outside service API