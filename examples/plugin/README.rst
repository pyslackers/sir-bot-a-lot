===============
Example plugins
===============

Collection of examples plugins for Sir-bot-a-lot.

To run the example use:

.. code-block:: console

    $ sirbot --example plugin

and then point your browser to http://localhost:8080/sir-bot-a-lot

ExampleConfigPlugin (:code:`config.py`)
=======================================

Example plugin for customizing the behaviors of Sir-bot-a-lot.

This plugin represent your configuration to customize Sir-bot-a-lot. The most
interesting method for this plugin is :code:`start`. It's in this method that you
register your endpoints for the others plugins.

This plugin should have the lowest priority in your configuration file as it
should start after all the other plugins to be sure they are started when you
register your endpoints.

In this example we add a :code:`sir-bot-a-lot` endpoint
(:code:`self.hello_sirbot`) to the :code:`ExampleListenerPlugin`. This endpoint
will query the :code:`ExampleSenderPlugin` facade and use it to make a request
to github.

For an in use example see the `python developers slack community`_
configuration.

.. _python developers slack community: https://github.com/ovv/sirbot-pythondev/blob/master/sirbot/pythondev/__init__.py

ExampleListenerPlugin (:code:`listener.py`)
===========================================

Example plugin listening to incoming event and dispatching them to coroutines
registered by the user in the configuration plugin.

In this example the plugin register a route for :code:`/{name}` in the aiohttp
app and if an endpoint was register for a specific name it will call the
registered coroutine.

For an in use example see the `github plugin`_

.. _github plugin: https://github.com/pyslackers/sirbot-plugins/tree/master/sirbot/plugins/github


ExampleSenderPlugin (:code:`sender.py`)
=======================================

Example plugin providing a facade to do http request.

In this example the plugin is not listening for incoming event but only
providing a facade to access a service. In this case access to the
:code:`aiohttp session` and an easy way to make a :code:`get` request to an url.

For an in use example see the `pypi plugin`_

.. _pypi plugin: https://github.com/pyslackers/sirbot-plugins/blob/master/sirbot/plugins/pypi.py