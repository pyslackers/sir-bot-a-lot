.. _plugins:

=======
Plugins
=======

.. _available_plugins:

Available plugins
-----------------

 * `Slack`_
 * `Github`_
 * `SQLite`_
 * `Others`_

.. _Slack: https://github.com/pyslackers/sirbot-slack
.. _Github: https://github.com/pyslackers/sirbot-plugins
.. _SQLite: https://github.com/pyslackers/sirbot-plugins
.. _Others: https://github.com/pyslackers/sirbot-plugins

.. _writing_plugins:

Writing plugins
---------------

Sir Bot-a-lot is build onto the `pluggy`_ library for plugin management.

.. _pluggy: https://github.com/pytest-dev/pluggy


A plugin must define one hook returning a subclass of the plugin class.

.. literalinclude:: ../sirbot/core/hookspecs.py


.. literalinclude:: ../sirbot/core/plugin.py


Facade
^^^^^^

If needed a plugin can expose a facade to Sir Bot-a-lot allowing other plugins access to its functionality.

A new facade instance is created each time a plugin request it.

Example
^^^^^^^

The `pypi`_ plugin provide a simple facade for the `Python Package Index`_ API.
It can be retrieve inside another plugin with:

.. code-block:: python
    
    # Create a new pypi facade by calling
    # PyPIPlugin.facade()
    pypi = facades.get('pypi')
    
    # The pypi plugin facade only expose the search function
    result = await pypi.search('sir-bot-a-lot')

.. _pypi: https://github.com/pyslackers/sirbot-plugins/blob/master/sirbot/plugins/pypi.py
.. _Python Package Index: https://pypi.python.org/pypi
