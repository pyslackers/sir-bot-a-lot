.. _facade:

======
Facade
======

The :ref:`references_facade` is the way to access other plugin functionality by requesting a plugin facade:

.. code-block:: python

    plugin_facade = facade.get('my_plugin')

A new plugin facade is created for each call to :meth:`sirbot.core.facade.MainFacade.get`

Each incoming request should create a new facade manager object by calling :meth:`sirbot.core.facade.MainFacade.new`

Example
-------

.. code-block:: python

    # Create a new pypi facade by calling
    # PyPIPlugin.facade()
    pypi = MainFacades.get('pypi')

    # The pypi plugin facade only expose the search function
    result = await pypi.search('sir-bot-a-lot')

.. _pypi: https://github.com/pyslackers/sirbot-plugins/blob/master/sirbot/plugins/pypi.py
.. _Python Package Index: https://pypi.python.org/pypi