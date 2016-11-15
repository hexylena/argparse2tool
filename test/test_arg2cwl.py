import sys
import os
import shutil
import unittest
from itertools import chain
from io import StringIO

import yaml

import argparse
from argparse2tool.cmdline2cwl import Arg2CWLParser
from argparse.argparse_cwl_translation import ArgparseCWLTranslation as ac
from test.cwl_classes import Tool


class GeneralTestCase(unittest.TestCase):
    maxDiff = None

    @staticmethod
    def prepare_argument_parser(name=None, add_help=True):
        parser = argparse.ArgumentParser(prog=name, description='test program', add_help=add_help)
        parser.add_argument('keyword', metavar='Q', type=str, nargs=1,
                            help='action keyword')
        parser.add_argument('integers', metavar='N', type=int, nargs='+',
                            help='an integer for \n'
                                 'the accumulator')
        parser.add_argument('choices', type=int, choices=range(5, 10))
        parser.add_argument('foo', type=str,
                            help='positional argument with the same dest as optional argument')
        parser.add_argument('positional_nargs_asteriks', nargs='*',
                            help='positional argument with nargs = *')
        parser.add_argument('positional_nargs_question_mark', nargs='?',
                            help='positional argument with nargs = ?')
        parser.add_argument('positional_with_choices', choices=['rock', 'paper', 'scissors'])
        parser.add_argument('--req', required=True, help='required optional')
        parser.add_argument('--foo', nargs='?', help='foo help')
        parser.add_argument('--open', type=open, help='argument with type `open`')
        parser.add_argument('--file', nargs='?', help='foo help', type=argparse.FileType('w'))
        parser.add_argument('--bar', nargs='*', default=[1, 2, 3], help='BAR!')
        parser.add_argument('--true_p', action='store_true', help='Store a true')
        parser.add_argument('--false_p', action='store_false', help='Store a false')
        parser.add_argument('--append', action='append', help='Append a value')
        parser.add_argument('--str', dest='types', action='append_const', const=str, help='Append a value')
        parser.add_argument('--int', dest='types', action='append_const', const=int, help='Append a value')
        parser.add_argument('--output-file', help='Output file')

        parser.add_argument('--nargs2', nargs=2, help='nargs2')

        parser.add_argument('--mode', choices=['rock', 'paper', 'scissors'], default='scissors')

        parser.add_argument('--version', action='version', version='2.0')
        parser.set_defaults(foo='Lorem Ipsum')
        return parser


    def test_help_message(self):
        tool_parser = self.prepare_argument_parser(name='test_help_message')
        testargs = ["test.py", "--help_arg2cwl"]

        sys.stdout = StringIO()
        fakeOutput = sys.stdout
        sys.argv = testargs

        arg2cwl_parser = Arg2CWLParser().parser
        with self.assertRaises(SystemExit) as result:
            tool_parser.parse_args(testargs)
            self.assertEqual(result.exception.code, 0)
        help_message_actual = fakeOutput.getvalue().strip()
        # flushing stdout
        fakeOutput.truncate(0)
        fakeOutput.seek(0)
        arg2cwl_parser.print_help()
        help_message_desired = fakeOutput.getvalue().strip()
        self.assertEqual(help_message_actual, help_message_desired)

    def test_subparser(self):
        """
        Tests if tools with subparsers run without errors
        """
        parser = self.prepare_argument_parser(name="test_subparser")
        subparsers = parser.add_subparsers()
        subparser = subparsers.add_parser('sub', help='test subparser')
        subparser.add_argument('keyword', type=str)
        testargs = ["test.py", "sub", "--generate_cwl_tool"]
        with self.assertRaises(SystemExit) as result:
            parser.parse_args(testargs)
        self.assertEqual(result.exception.code, 0)

    def test_output_directory_storage_for_CWL_tool(self):
        parser = self.prepare_argument_parser(name="test-directory.py")
        directory = os.path.dirname(__file__)
        new_dir = 'test/'
        os.mkdir(new_dir)
        testargs = ["test-directory.py", "--generate_cwl_tool", "-d", new_dir]
        with self.assertRaises(SystemExit) as result:
            parser.parse_args(testargs)
            self.assertEqual(result.exception.code, 0)
        filepath = os.path.join(directory, new_dir, 'test-directory.cwl')
        self.assertTrue(os.path.isfile(filepath))
        shutil.rmtree(new_dir)


class CWLTestCase(unittest.TestCase):
    test_dir = "test_dir/"

    def setUp(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.mkdir(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def get_simple_tool(self, parser_name, testargs=None, add_help=True):
        parser = GeneralTestCase.prepare_argument_parser(parser_name, add_help)
        if not testargs:
            testargs = [parser_name, "--generate_cwl_tool", "-d", self.test_dir]
        with self.assertRaises(SystemExit) as result:
            parser.parse_args(testargs)
            self.assertEqual(result.exception.code, 0)
        return parser, Tool(self.test_dir + parser_name.replace('.py', '.cwl').strip('./'))

    @staticmethod
    def _strip_help_version_actions(actions):
        return filter(lambda action: type(action).__name__ not in ('_HelpAction', '_VersionAction'), actions)

    def test_position(self):
        parser_name = "test-position.py"
        parser, tool = self.get_simple_tool(parser_name)
        positional_count = 1
        for positional in parser._positionals._group_actions:
            self.assertEqual(positional_count, tool.inputs[positional.dest].input_binding.position)
            positional_count += 1
        for optional in self._strip_help_version_actions(parser._optionals._group_actions):
            self.assertRaises(AttributeError, tool.inputs[optional.dest].input_binding.position)
            self.assertIs(tool.inputs[optional.dest].input_binding.position, None)

    def test_shebang(self):
        parser_name = './test-shebang.py'
        parser, tool = self.get_simple_tool(parser_name)
        self.assertEqual([parser_name], tool.basecommand)

    def test_basecommand(self):
        """
        if `basecommand` is provided in a program which is run with shebang,
        it replaces autogenerated shebang basecommand
        """
        parser_name = './test-shebang.py'
        file_name = parser_name.strip('./')
        testargs = [parser_name, "--generate_cwl_tool", "-d", self.test_dir, "-b", "python3"]
        parser, tool = self.get_simple_tool(file_name, testargs)
        self.assertEqual(['python3'], tool.basecommand)
        self.assertEqual(file_name, tool.inputs[file_name].id)

    def test_default(self):
        parser, tool = self.get_simple_tool('test-default.py')
        for action in self._strip_help_version_actions(parser._actions):
            tool_default = tool.inputs[action.dest].default
            if action.default == 'null':
                action.default = None
            self.assertEqual(action.default, tool_default)

    def test_optional(self):
        parser, tool = self.get_simple_tool('test-optional.py')
        for action in self._strip_help_version_actions(parser._actions):
            if (action.option_strings and not action.required) or action.nargs in ('*', '?'):
                self.assertEqual('null', tool.inputs[action.dest].type[0])
            else:
                self.assertNotIsInstance(tool.inputs[action.dest].type, list)

    def test_type(self):
        parser, tool = self.get_simple_tool('test-optional.py')
        for action in self._strip_help_version_actions(parser._actions):
            arg_type = tool.inputs[action.dest].type
            if type(arg_type) is list:  # if argument is optional, the first type in list is `null`
                arg_type = arg_type[1]  # the second is the actual type
            if action.choices:
                if type(action.choices) is range:
                    self.assertEqual(list(action.choices), arg_type['symbols'])
                else:
                    self.assertEqual(action.choices, arg_type['symbols'])
                self.assertEqual('enum', arg_type['type'])
            if action.type:
                if isinstance(action.type, argparse.FileType):
                    action_type = 'File'
                else:
                    action_type = ac.get_cwl_type(action.type)
                if (action.nargs and action.nargs != '?') \
                        or type(action).__name__.startswith("_Append"):
                    self.assertEqual('array', arg_type['type'])
                    self.assertEqual(action.items_type or 'string', arg_type['items'])
                elif action.choices:
                    self.assertTrue(all(isinstance(x, action.type) for x in arg_type['symbols']))
                else:
                    self.assertEqual(action_type, arg_type)

    def test_output_replacement(self):
        """
        `--output_section FILENAME` option
        """
        output_section = \
        {'outputs':[
            {'id': 'outfile1',
             'type': 'File',
             'description': 'output file',
             'outputBinding':{
                 'glob': '$(inputs.outputPrefix+".vcf.gz")',
             }
            }
          ]
        }
        output_file = self.test_dir + 'example_output.cwl'
        with open(output_file, 'w') as f:
            yaml.dump(output_section, f)
        filename = 'test_output.py'
        testargs = [filename, "--generate_cwl_tool", "-d", self.test_dir, "-o", output_file]
        parser, tool = self.get_simple_tool(filename, testargs)
        output_0_name = output_section['outputs'][0]['id']
        self.assertEqual(output_section['outputs'][0]['id'], tool.outputs[output_0_name].id)
        self.assertEqual(output_section['outputs'][0]['outputBinding']['glob'],
                         tool.outputs[output_0_name].output_binding.glob)

    def test_outputs(self):
        parser_name = 'test-outputs.py'
        testargs = [parser_name, "--generate_cwl_tool", "-d", self.test_dir, "-go"]
        parser, tool = self.get_simple_tool(parser_name, testargs)
        for action in self._strip_help_version_actions(parser._actions):
            if 'output' in action.dest:
                self.assertTrue(tool.outputs[action.dest+'_out'].id)

    def test_parents(self):
        mum, mum_tool = self.get_simple_tool('mum.py', add_help=False)
        dad = argparse.ArgumentParser(prog='daddy.py', description='test program', add_help=False)
        dad.add_argument('pos_arg', type=int)
        dad.add_argument('--opt_arg', action='store_true')
        kid_name = 'kid.py'
        kid = argparse.ArgumentParser(prog=kid_name, parents=[mum, dad])
        kid.add_argument('--kids_argument', nargs='*')
        testargs = [kid_name, "--generate_cwl_tool", "-d", self.test_dir]
        with self.assertRaises(SystemExit) as result:
            kid.parse_args(testargs)
            self.assertEqual(result.exception.code, 0)
        tool = Tool(self.test_dir + kid_name.replace('.py', '.cwl').strip('./'))
        actions = list(chain(self._strip_help_version_actions(mum._actions),
                           self._strip_help_version_actions(dad._actions)))
        arguments = [arg.dest for arg in actions]
        arguments.append('kids_argument')
        for arg in arguments:
            self.assertIn(arg, tool.inputs.keys())

    def test_prefixes(self):
        parser_name = 'test-prefix-chars.py'
        parser = argparse.ArgumentParser(prog=parser_name,
                                         prefix_chars='-+',
                                         description='test prefix chars program')
        parser.add_argument('keyword', type=str, nargs=1,
                            help='action keyword')
        parser.add_argument('integers', metavar='N', type=int, nargs='+',
                            help='an integer for \n'
                                 'the accumulator')
        parser.add_argument('choices', type=int, choices=range(5, 10))
        parser.add_argument('foo', type=str,
                            help='positional argument with the same dest as optional argument')
        parser.add_argument('--req', required=True, help='required optional')
        parser.add_argument('++foo', nargs='?', help='foo help')
        parser.add_argument('+open', type=open, help='argument with type `open`')
        parser.add_argument('-file', nargs='?', help='foo help', type=argparse.FileType('w'))
        parser.add_argument('--bar', nargs='*', default=[1, 2, 3], help='BAR!')
        testargs = [parser_name, "--generate_cwl_tool", "-d", self.test_dir]
        with self.assertRaises(SystemExit) as result:
            parser.parse_args(testargs)
            self.assertEqual(result.exception.code, 0)
        tool = Tool(self.test_dir + parser_name.replace('.py', '.cwl').strip('./'))
        for optional in self._strip_help_version_actions(parser._optionals._group_actions):
            self.assertEqual(tool.inputs[optional.dest].input_binding.prefix, optional.option_strings[0])

    def test_type_conversions(self):
        self.assertEqual(ac.get_cwl_type(open), 'File')
        self.assertEqual(ac.get_cwl_type(argparse.FileType('r')), 'File')
        self.assertEqual(ac.get_cwl_type(str), 'string')
        self.assertEqual(ac.get_cwl_type('str'), 'string')


if __name__ == '__main__':
    unittest.main()
