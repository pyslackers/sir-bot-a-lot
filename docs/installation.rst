.. _installation:

============
Installation
============


Stable release
--------------

**NOT YET RELEASED**

To install sir-bot-a-lot, run this command in your terminal:

.. code-block:: console

    $ pip install sir-bot-a-lot

This is the preferred method to install sir-bot-a-lot, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

From sources
------------

The sources for Sir Bot-a-lot can be downloaded from the `github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://gitlab.com/PythonDevCommunity/sir-bot-a-lot

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/pyslackers/sir-bot-a-lot/tarball/master

Install
~~~~~~~

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

or:

.. code-block:: console

    $ pip install sir-bot-a-lot/

Install and run with Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Build the image:

.. code-block:: console

    $ docker build -t sir-bot-a-lot .

And run the image:

.. code-block:: console

    $ docker run -ti -p "8080:8080" sir-bot-a-lot

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
.. _github repo: https://github.com/pyslackers/sir-bot-a-lot
.. _tarball: https://github.com/pyslackers/sir-bot-a-lot/tarball/master
