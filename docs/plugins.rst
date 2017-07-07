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
 * `APScheduler`_
 * `Others`_

We can't wait to add your plugin to this list, just contact us trough GitHub.

.. _Slack: https://github.com/pyslackers/sirbot-slack
.. _Github: https://github.com/pyslackers/sirbot-plugins
.. _SQLite: https://github.com/pyslackers/sirbot-plugins
.. _APScheduler: https://github.com/pyslackers/sirbot-plugins
.. _Others: https://github.com/pyslackers/sirbot-plugins

.. _writing_plugins:

Writing plugins
---------------

Sir Bot-a-lot is build onto the `pluggy`_ library for plugin management.
A :ref:`references_plugin` must define one :ref:`references_hook` returning a
subclass of the plugin class.

.. _pluggy: https://github.com/pytest-dev/pluggy

Factory
^^^^^^^

The factory of a plugin is it's main interaction point with the other plugins.
At any time you can ask the :ref:`references_registry` to query the factory of
any available plugin.

This allow plugins to interact with each others. For example the `Github`_
plugin can query the `Slack`_ plugin factory through the
:ref:`references_registry` in order to obtain a wrapper for the slack API and
send a slack message.

Registry
^^^^^^^^

The :ref:`references_registry` is the object that regroups all the available
factories. It behave the same way as a dictionary.

Start
^^^^^

As plugins might need the functionality of other plugins during startup a
specific order is establish based on each plugin :ref:`conf_starting_priority`.

Sir Bot-a-lot will also wait for a plugin to be fully started before attempting
to start the next one. This ensure that no race condition exist in the starting
process.

When starting a plugin Sir Bot-a-lot create a new asyncio task in order to
allow it to run indefinitely.

Example
^^^^^^^

For examples plugins take a look at some of the :ref:`available plugins` code
on the `pyslackers github`_.

.. _pyslackers github: https://github.com/pyslackers/sirbot-plugins
