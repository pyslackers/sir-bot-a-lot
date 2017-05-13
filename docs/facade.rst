======
Facade
======

The facade manager is the way to access other plugin functionality by requesting a plugin facade:

.. code-block:: python

    plugin_facade = facade.get('my_plugin')

A new plugin facade is created for each call to the :code:`Facade.get` method

Each incoming request should create a new facade manager object by calling :code:`facade.new()`
