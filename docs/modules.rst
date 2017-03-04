.. _modules:

=======
Modules
=======

Available modules
-----------------

.. _available_modules:

 * `Slack`_
 * `Web`_

.. _Slack: https://gitlab.com/PythonDevCommunity/sirbot-plugin-slack
.. _Web: https://gitlab.com/PythonDevCommunity/sirbot-plugin-web

Writing modules
---------------

.. _writing_modules:

Sir-bot-a-lot is build onto the `pluggy`_ library for plugins management.

.. _pluggy: https://github.com/pytest-dev/pluggy

Hooks
^^^^^

Two hooks are used. Ths first one to load the clients and the second one to load
the dispatchers.

.. literalinclude:: ../sirbot/hookspecs.py

Clients
^^^^^^^

The client is the part of a module receiving data from the outside world.

.. literalinclude:: ../sirbot/plugins/client.py


Dispatcher
^^^^^^^^^^

The dispatcher is the part of a module processing the incoming data and acting on it.
It should also provide a facade for plugins to interact between them

.. literalinclude:: ../sirbot/plugins/dispatcher.py
