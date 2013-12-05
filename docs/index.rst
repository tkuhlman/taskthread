.. taskthread documentation master file, created by
   sphinx-quickstart on Wed Dec  4 15:35:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to taskthread's documentation!
======================================

*taskthread* provides a thread implementation that executes a repetitive
task several times without the need to start up a new thread.

Installation
------------

*taskthread* can be installed with pip, via ``pip install taskthread``.

Usage
-----

TaskThread
~~~~~~~~~~
.. autoclass:: taskthread.TaskThread
    :members:

TaskInProcessException
~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: taskthread.TaskInProcessException
    :members:
