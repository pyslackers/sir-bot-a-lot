.. _plugins:

=======
Plugins
=======

.. _available_plugins:

Available plugins
-----------------

 * `Slack`_
 * `Pythondev plugins repositorie`_

.. _Slack: http://sirbot-plugin-slack.readthedocs.io/en/latest/
.. _Pythondev plugins repositorie: https://gitlab.com/PythonDevCommunity/sirbot-plugin

.. _writing_plugins:

Writing plugins
---------------

Sir-bot-a-lot is build onto the `pluggy`_ library for plugins management.

.. _pluggy: https://github.com/pytest-dev/pluggy


A plugin must define one hook returning the plugin name and a subclass of the plugin class.

.. literalinclude:: ../sirbot/hookspecs.py


.. literalinclude:: ../sirbot/plugin.py


Example
^^^^^^^

The `giphy`_ plugin provide a simple facade for the `Giphy.com`_ API.
It can be retrieve inside another plugin with:

.. code-block:: python

    facades.get('giphy')


.. _giphy: https://gitlab.com/PythonDevCommunity/sirbot-plugin/blob/master/sirbot_plugin/giphy.py
.. _Giphy.com: http://giphy.com/