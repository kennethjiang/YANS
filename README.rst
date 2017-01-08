===============================
YANS
===============================

.. image:: https://badge.fury.io/py/YANS.png
    :target: http://badge.fury.io/py/YANS

.. image:: https://travis-ci.org/kennethjiang/YANS.png?branch=master
        :target: https://travis-ci.org/kennethjiang/YANS


**Yet Another Network Simulator**

Getting Started
====================

Install prerequisites:
------------------------

Mac OS X
^^^^^^^^

* `Docker <https://docs.docker.com/engine/installation/mac/>`__
* `Docker Machine <https://docs.docker.com/machine/install-machine/>`__

Ubuntu
^^^^^^^^

* `Docker <https://docs.docker.com/engine/installation/linux/ubuntulinux/>`__
* ``sudo apt install bridge-utils``


Install YANS
------------------

.. code:: bash

    pip install YANS


Create a file named ``topo.yaml``
-----------------------------------------------

.. code::

    - name: link1
      nodes:
         - node1
         - node2
    - name: link2
      nodes:
         - node1
    - name: link3


Go!
------------

Linux
^^^^^^^

    sudo yans -t <path_to_topo.yaml> up


Mac OS X
^^^^^^^^^^

    yans -t <path_to_topo.yaml> up


Requirements
------------

- Python >= 2.6 or >= 3.3

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/kennethjiang/yans/blob/master/LICENSE>`_ file for more details.
