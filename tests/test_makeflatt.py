import os
import json
from jsondiff import diff
from unittest import TestCase

from makeflatt import __version__, FlattMaker, NotADictionaryException


class TestFlattMaker(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.fm = FlattMaker()

    def test_version(self):
        self.assertEqual(__version__, "1.0.2")

    def test_noop(self):
        expected = {"a": 1, "b": 2, "c": 3}
        got = self.fm.apply(expected)
        self.assertEqual(got, expected)

    def test_apply_simple_dict(self):
        _input = {"a": 1, "b": {"c": 2}}
        expected = {"a": 1, "b.c": 2}
        got = self.fm.apply(_input)
        self.assertEqual(got, expected)

    def test_deep_apply_simple_dict(self):
        _input = {"a": 1, "b": [{"c": 2}]}
        expected = {"a": 1, "b.0.c": 2}
        got = self.fm.deep_apply(_input)
        self.assertEqual(got, expected)

    def test_apply_2_level_dict(self):
        _input = {"a": 1, "b": {"c": {"d": 2}}}
        expected = {"a": 1, "b.c.d": 2}
        got = self.fm.apply(_input)
        self.assertEqual(got, expected)

    def test_deep_apply_2_level_dict(self):
        _input = {"a": 1, "b": [{"c": [{"d": 2}]}]}
        expected = {"a": 1, "b.0.c.0.d": 2}
        got = self.fm.deep_apply(_input)
        self.assertEqual(got, expected)

    def test_apply_3_level_dict(self):
        _input = {"a": 1, "b": {"c": {"d": {"f": 2}}}}
        expected = {"a": 1, "b.c.d.f": 2}
        got = self.fm.apply(_input)
        self.assertEqual(got, expected)

    def test_deep_apply_3_level_dict(self):
        _input = {"a": 1, "b": [{"c": [{"d": [{"f": 2}]}]}]}
        expected = {"a": 1, "b.0.c.0.d.0.f": 2}
        got = self.fm.deep_apply(_input)
        self.assertEqual(got, expected)

    def test_apply_4_level_dict(self):
        _input = {"a": 1, "b": {"c": {"d": {"f": {"g": 2}}}}}
        expected = {"a": 1, "b.c.d.f.g": 2}
        got = self.fm.apply(_input)
        self.assertEqual(got, expected)

    def test_deep_apply_4_level_dict(self):
        _input = {"a": 1, "b": [{"c": [{"d": [{"f": [{"g": 2}]}]}]}]}
        expected = {"a": 1, "b.0.c.0.d.0.f.0.g": 2}
        got = self.fm.deep_apply(_input)
        self.assertEqual(got, expected)

    def test_apply_json_files(self):
        files = os.listdir("tests/json")
        for json_file in files:
            with open("tests/json/" + json_file) as fd:
                content = json.load(fd)
            _input = content["input"]
            expected = content["apply"]
            got = self.fm.apply(_input)
            self.assertEqual(got, expected, diff(expected, got))

            expected_deep_apply = content["deep_apply"]
            got = self.fm.deep_apply(_input)
            self.assertEqual(
                got,
                expected_deep_apply,
                diff(expected_deep_apply, got))

    def test_apply_passing_a_non_dictionary(self):
        with self.assertRaises(NotADictionaryException):
            self.fm.apply("THIS IS NOT A DICTIONARY")

    def test_deep_apply_passing_a_non_dictionary(self):
        with self.assertRaises(NotADictionaryException):
            self.fm.deep_apply("THIS IS NOT A DICTIONARY")

    def test_apply_with_different_sep(self):
        fm = FlattMaker(sep=":")
        _input = {"a": 1, "b": {"c": {"d": {"f": {"g": 2}}}}}
        expected = {"a": 1, "b:c:d:f:g": 2}
        got = fm.apply(_input)
        self.assertEqual(got, expected)

    def test_deep_apply_with_different_sep(self):
        fm = FlattMaker(sep=":")
        _input = {"a": 1, "b": [{"c": [{"d": [{"f": [{"g": 2}]}]}]}]}
        expected = {"a": 1, "b:0:c:0:d:0:f:0:g": 2}
        got = fm.deep_apply(_input)
        self.assertEqual(got, expected)
