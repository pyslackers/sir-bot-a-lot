.. _facade:

======
Facade
======

The :ref:`references_facade` is the way to access other plugin functionality by requesting a plugin facade:

.. code-block:: python

    plugin_facade = facade.get('my_plugin')

A new plugin facade is created for each call to :meth:`sirbot.core.facade.MainFacade.get`

Each incoming request should create a new facade manager object by calling :meth:`sirbot.core.facade.MainFacade.new`
