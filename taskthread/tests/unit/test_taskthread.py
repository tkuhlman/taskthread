# -*- coding: utf-8 -*-
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
# under the License.:w


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
        task_thread.kwargs = {'a': 2}
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

    def test_join_task(self):
        task_thread = TaskThread(forever_function)
        task_thread.in_task = True
        task_thread.task_complete = Mock()
        task_thread.task_complete.wait = Mock(side_effect=[True])
        success = task_thread.join_task(1)
        self.assertTrue(success)

    def test_join_task_not_running(self):
        task_thread = TaskThread(forever_function)
        task_thread.task_complete = Mock()
        task_thread.wait =\
            Mock(side_effect=Exception("Should never be called"))
        task_thread.join_task(1)

    def test_join(self):
        task_thread = TaskThread(forever_function)
        task_thread.start()
        task_thread.run_task()
        # Set the event so the task completes
        forever_event.set()
        task_thread.join_task(1)
        task_thread.join(1)

    def test_execute_multiple_tasks(self):
        task_thread = TaskThread(forever_function)
        task_thread.start()
        task_thread.run_task()
        # Set the event so the task completes
        forever_event.set()
        task_thread.join_task(1)
        forever_event.set()
        task_thread.join_task(1)
        task_thread.join(1)
