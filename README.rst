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

Changes
-------

v1.0
~~~~
* First release



