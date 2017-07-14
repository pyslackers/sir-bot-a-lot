.. _references:

==========
References
==========

.. _references_sirbot:

SirBot
------

.. autoclass:: sirbot.core.SirBot
   :members:

.. _references_registry:

Registry
--------

.. autoclass:: sirbot.core.RegistrySingleton
   :members:

.. _references_plugin:


Plugin
------

.. autoclass:: sirbot.core.plugin.Plugin
   :members:

   .. autoattribute:: sirbot.core.plugin.Plugin.__name__
   .. autoattribute:: sirbot.core.plugin.Plugin.__version__
   .. autoattribute:: sirbot.core.plugin.Plugin.__registry__

.. _references_hook:

Hook
----

.. autofunction:: sirbot.core.hookspecs.plugins

.. _references_exceptions:

Exceptions
----------

.. autoexception:: sirbot.core.errors.SirBotError
   :members:

.. autoexception:: sirbot.core.errors.RegistryError
   :members:

.. autoexception:: sirbot.core.errors.FrozenRegistryError
   :members:
