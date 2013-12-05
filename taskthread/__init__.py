# Copyright 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import logging
import threading

__version__ = '1.2'


logger = logging.getLogger(__name__)


class TaskInProcessException(BaseException):
    pass


class TaskThread(threading.Thread):
    """
    A thread object that repeats a task.

    Usage example::

        from taskthread import TaskThread

        import time

        def my_task(*args, **kwargs):
            print args, kwargs

        task_thread = TaskThread(my_task)
        task_thread.start()
        for i in xrange(10):
            task_thread.run_task()
            task_thread.join_task()
        task_thread.join()

    .. note:: If :py:meth:`~TaskThread.run_task` is
        invoked while run_task is in progress,
        :py:class:`~.TaskInProcessException` will
        be raised.

    :param task:
        A ``function``. This param is the task to execute when
         run_task is called.
    :param event:
        A ``threading.Event``. This event will be set when run_task
         is called. The default value is a new event, but may be
         specified for testing purposes.
    """

    daemon = True
    '''
    Threads marked as daemon will be terminated.
    '''
    def __init__(self, task, event=threading.Event(),
                 *args, **kwargs):
        super(TaskThread, self).__init__()
        self.task = task
        self.task_event = event
        self.running = True
        self.running_lock = threading.Lock()
        self.in_task = False
        self.task_complete = threading.Event()
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """
        Called by threading.Thread, this runs in the new thread.
        """
        while self.task_event.wait():
            if not self.running:
                logger.debug("TaskThread exiting")
                return
            logger.debug("TaskThread starting task")
            with self.running_lock:
                self.task_event.clear()
            self.task_complete.clear()
            self.task(*self.args, **self.kwargs)
            with self.running_lock:
                self.in_task = False
            self.task_complete.set()

    def run_task(self, *args, **kwargs):
        """
        Run an instance of the task.

        :param args:
            The arguments to pass to the task.

        :param kwargs:
            The keyword arguments to pass to the task.
        """
        # Don't allow this call if the thread is currently
        # in a task.
        with self.running_lock:
            if self.in_task:
                raise TaskInProcessException()
            self.in_task = True
        logger.debug("Waking up the thread")
        self.args = args
        self.kwargs = kwargs
        # Wake up the thread to do it's thing
        self.task_event.set()

    def join_task(self, time_out):
        """
        Wait for the currently running task to complete.

        :param time_out:
            An ``int``. The amount of time to wait for the
            task to finish.
        """
        with self.running_lock:
            if not self.in_task:
                return

        success = self.task_complete.wait(time_out)
        if success:
            self.task_complete.clear()
        return success

    def join(self, timeout=None):
        """
        Wait for the task to finish
        """
        self.running = False
        self.task_event.set()
        super(TaskThread, self).join(timeout=timeout)
