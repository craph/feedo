from feedo.action_date import ActionDate
from feedo.event import Event
import unittest

# parse a date field and transform it

class TestActionDate(unittest.TestCase):
    def test_1(self):
        action = ActionDate("*", "t")
        event = Event("my_tag", 123456789, {"t": "2020-10-22T08:50:20+00:00"})
        result = action.do(event)
        expected = {"t": 1603356620.0}

        self.assertEqual(result.record, expected)

    def test_2(self):
        action = ActionDate("*", "t", "%Y-%m-%d")
        event = Event("my_tag", 123456789, {"t": 1603356620.0})
        result = action.do(event)
        expected = {"t": "2020-10-22"}

        self.assertEqual(result.record, expected)





