import inotify.adapters
import os.path
import os
import logging
import unittest
import fnmatch
from glob import glob
from .abstract_action import AbstractAction
from .event import Event
from time import time
from unittest.mock import Mock


class InputFile(AbstractAction):
    def __init__(self, tag, watch_path, path_pattern, remove=False):
        AbstractAction.__init__(self)
        self._tag = tag
        self._watch_path = watch_path
        self._path_pattern = path_pattern
        self._watcher = None
        self._remove = remove
        #self._log = logging.getLogger("InputFile")

    def update(self):
        if self._watcher is None:
            # first run
            self._watcher = inotify.adapters.InotifyTree(self._watch_path)
            self._log.debug("First run, finding fitting file with '{}'".format(self._path_pattern))
            for filename in glob(self._path_pattern):
                self._log.debug("->{}".format(self._path_pattern))
                self.process_file("", filename)

        for event in self._watcher.event_gen():
            if event is None:
                return

            if 'IN_CLOSE_WRITE' in event[1]:
                self.process_file(event[2], event[3])

    def process_file(self, directory, filename):
        path = os.path.join(directory, filename)
        match = fnmatch.fnmatch(path, self._path_pattern)
        if match:
            self._log.info ("Process file '{}'".format(path))
            with open(path) as f:
                line_number = 0
                for line in f:
                    data = line.rstrip()
                    event = Event(self._tag, int(time()), {"log":data})
                    self.call_next(event)
                    line_number += 1
                self._log.info("Processing file '{}' produce {} events".format(filename, line_number))

            if self._remove:
                self._log.debug ("Remove file '{}'".format(path))
                os.remove(path)

class TestInputFile(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_1(self):
        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log")
        action = Mock()
        input_file.set_next(action)

    def test_2(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log")
        action = Mock()
        input_file.set_next(action)
        input_file.update()

    def test_3(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log")
        action = Mock()
        input_file.set_next(action)
        input_file.update()

        with open("/tmp/test.log", "w") as f:
            f.write("test\n")

        input_file.update()

    def test_4(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log", True)
        action = Mock()
        input_file.set_next(action)
        input_file.update()

        with open("/tmp/test.log", "w") as f:
            f.write("test\n")

        input_file.update()

    def test_5(self):

        input_file = InputFile("syslog", "/tmp", "/tmp/*est.log", True)
        action = Mock()
        input_file.set_next(action)

        with open("/tmp/test.log", "w") as f:
            f.write("test\n")

        input_file.update()