.. _plugins:

=======
Plugins
=======

.. _available plugins:

Available plugins
-----------------

 * `Slack`_
 * `Github`_
 * `SQLite`_
 * `Scheduler`_
 * `Others`_

.. _Slack: https://github.com/pyslackers/sirbot-slack
.. _Github: https://github.com/pyslackers/sirbot-plugins
.. _SQLite: https://github.com/pyslackers/sirbot-plugins
.. _Scheduler: https://github.com/pyslackers/sirbot-plugins
.. _Others: https://github.com/pyslackers/sirbot-plugins

.. _writing_plugins:

Writing plugins
---------------

Sir Bot-a-lot is build onto the `pluggy`_ library for plugin management.
A :ref:`references_plugin` must define one :ref:`references_hook` returning a
subclass of the plugin class.

.. _pluggy: https://github.com/pytest-dev/pluggy

Facade
^^^^^^

If needed a plugin can expose a :ref:`facade` to Sir Bot-a-lot allowing other
plugins access to its functionality.

A new facade instance is created each time a plugin request one.

Example
^^^^^^^

For example plugins take a look at the `example folder`_ in the github repository.

.. _example folder: https://github.com/pyslackers/sir-bot-a-lot/tree/master/examples/plugin