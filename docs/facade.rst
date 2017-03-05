======
Facade
======

The MainFacade object is the way to access other plugin functionality.
Each plugin should expose a facade.

To request a plugin facade:

.. code-block:: python

    plugin_facade = main_facade.get('my_plugin')

A new plugin facade is created for each called to the :code:`MainFacade.get` method
