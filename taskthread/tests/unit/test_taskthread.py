# -*- coding: utf-8 -*-

import unittest2 as unittest

from mock import Mock, patch

from taskthread import TaskThread, TaskInProcessException


class TaskThreadTestCase(unittest.TestCase):
    """
    Tests for :py:class:`.TaskThread`.
    """

    def test___init__(self):
        self.assertEqual(1, 1)
