# -*- coding: utf-8 -*-

import threading
import unittest2 as unittest

from mock import Mock

from taskthread import TaskThread, TaskInProcessException

forever_event = threading.Event()
def forever_function(*args, **kwargs):
    forever_event.wait()
    forever_event.clear()


class TaskThreadTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.TaskThread`.
    """


    def test___init__(self):
        """
        Test the __init__ method. It doesn't really do much.
        """
        task_thread = TaskThread(forever_function)
        self.assertEqual(forever_function, task_thread.task)

    def test_run_not_running(self):
        """
        Verifies that thread will shut down when running is false
        """
        event = Mock()
        event.wait = Mock(side_effect=[True])
        event.clear = Mock(side_effect=Exception("Should never be called"))
        task_thread = TaskThread(forever_function,
                                 event=event)
        task_thread.running = False
        task_thread.run()
        event.wait.assert_called_once_with()

    def test_run_executes_task(self):
        event = Mock()
        event.wait = Mock(side_effect=[True, True])

        def stop_iteration(*args, **kwargs):
            args[0].running = False

        task_thread = TaskThread(stop_iteration,
                                 event=event)

        task_thread.args = [task_thread]
        task_thread.kwargs = {'a':2}
        task_thread.in_task = True
        task_thread.run()
        self.assertEqual(False, task_thread.in_task)

    def test_run_task(self):
        event = Mock()
        task_thread = TaskThread(forever_function,
                                 event=event)
        args = [1]
        kwargs = {'a': 1}

        task_thread.run_task(*args, **kwargs)
        self.assertEqual(tuple(args), task_thread.args)
        self.assertEqual(kwargs, task_thread.kwargs)
        event.set.assert_called_once_with()

    def test_run_task_task_in_progress(self):
        event = Mock()
        task_thread = TaskThread(forever_function,
                                 event=event)
        task_thread.in_task = True
        self.assertRaises(TaskInProcessException, task_thread.run_task)

    def test_join(self):
        task_thread = TaskThread(forever_function)
        task_thread.start()
        task_thread.run_task()
        # Set the event so the task completes
        forever_event.set()
        task_thread.join(1)

    def test_execute_multiple_tasks(self):
        task_thread = TaskThread(forever_function)
        task_thread.start()
        task_thread.run_task()
        # Set the event so the task completes
        forever_event.set()
        while True:
            try:
                task_thread.run_task()
                break
            except TaskInProcessException:
                pass
        forever_event.set()
        task_thread.join(1)

