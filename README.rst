TaskThread
==========

Python thread module to repeat an predefined task on a thread mulitple times.
A TaskThread is useful when a task needs to be repeated several times on 
a separate thread. Normal usage of the threading.Thread class would call for
creation of a new thread each time the same task needs to be run. This module
allows for repetitive tasks to be run multiple times on the same thread by having
the thread wait until the task needs to be executed again.


Provided Classes
----------------
``taskthread.TaskThread```
    A sub-class of ``threading.Thread`` that may execute a single task
    multiple times without the overhead of starting a new thread.
``taskthread.TaskInProcessException``
    Exception that is thrown if a task is started on a thread that is
    already executing.


Installation
------------

*taskthread* may be installed by executing ``pip install taskthread``.


Links
-------------

* `documentation <http://taskthread.readthedocs.org/en/latest/>`_ 
* `source <http://github.com/hpcs-som/taskthread/>`_


Changes
-------

v1.4
~~~~

* **ADD** ``TimerTask`` class that runs a repetitive task on a taskthread.


v1.3
~~~~

* Change task loop to support python 2.6.


v1.2
~~~~

* Refactor the module so classes are defined in __init__.py.


v1.1
~~~~

* **ADD** ``TaskThread.join_task`` method that waits for the currently executing.
  task to complete.


v1.0
~~~~

* First release



