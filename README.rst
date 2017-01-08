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

In the same directory as file ``topo.yaml``, run::

    yans up


Requirements
------------

- Python >= 2.6 or >= 3.3

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/kennethjiang/yans/blob/master/LICENSE>`_ file for more details.
