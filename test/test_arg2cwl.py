import sys
import unittest
from unittest import mock
import argparse


class GeneralTestCase(unittest.TestCase):

    def prepare_argument_parser(self):
        parser = argparse.ArgumentParser(prog='test', description='test program')
        parser.add_argument('keyword', metavar='Q', type=str, nargs=1,
                            help='action keyword')

        parser.add_argument('integers', metavar='N', type=int, nargs='+',
                            help='an integer for the accumulator')

        parser.add_argument('--sum', '-s', dest='accumulate', action='store_const',
                            const=sum, default=max, help='sum the integers (default: find the max)')

        parser.add_argument('--foo', nargs='?', help='foo help')
        parser.add_argument('--file', nargs='?', help='foo help', type=argparse.FileType('w'))
        parser.add_argument('--bar', nargs='*', default=[1, 2, 3], help='BAR!')
        parser.add_argument('--true', action='store_true', help='Store a true')
        parser.add_argument('--false', action='store_false', help='Store a false')
        parser.add_argument('--append', action='append', help='Append a value')

        parser.add_argument('--nargs2', nargs=2, help='nargs2')

        parser.add_argument('--mode', choices=['rock', 'paper', 'scissors'], default='scissors')

        parser.add_argument('--version', action='version', version='2.0')
        return parser

    def test_general(self):
        parser = self.prepare_argument_parser()
        testargs = ["python3", "test.py", "--generate_cwl_tool"]
        print(sys.version)
        with self.assertRaises(SystemExit) as result:
            with unittest.mock.patch.object(sys, 'argv', testargs):
                parser.parse_args()
        self.assertEqual(result.exception.code, 0)

if __name__ == '__main__':
    unittest.main()