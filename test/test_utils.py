from builtins import str
from builtins import range
from unittest import TestCase
import sys
import hashlib
import copy


class GeneralTests(TestCase):

    def test_load(self):
        gxap = sys.modules['argparse2tool']
        ap = sys.modules['argparse']
        # Ensure we've loaded the correct argparse ;)
        self.assertTrue('argparse2tool/argparse' in str(ap))
        self.assertTrue('argparse2tool/argparse2tool' in str(gxap))

        import argparse as fake_ap
        # Do we have a ref to the real ap
        self.assertTrue('ap' in dir(fake_ap))
        # Is it the real argparse?
        self.assertTrue('_os' in dir(fake_ap.ap))

    def __gen_id(self, kwargs):
        key = ""
        for x in sorted(kwargs.keys()):
            key += str(kwargs[x])
        digest = hashlib.sha1(key).hexdigest()
        repl = 'qrstuvwxyz'
        for c in range(10):
            digest = digest.replace(str(c), repl[c])
        return digest

    def dict_product(self, odl, key_name, new_key_list):
        for x in new_key_list:
            if x is None:
                for od in odl:
                    yield od
            else:
                for od in odl:
                    od2 = copy.deepcopy(od)
                    od2[key_name] = x
                    yield od2

    def test_dict_product(self):
        a = [{'a': 0}, {'a': 1}]
        correct = [
            {'a': 0},
            {'a': 1},
            {'a': 0, 'b': 1},
            {'a': 1, 'b': 1},
        ]

        results = list(self.dict_product(a, 'b', [None, 1]))
        self.assertCountEqual(correct, results)

    def __blacklist(self, item_list):
        for i in item_list:
            try:
                if i['action'] in ('store_true', 'store_false', 'count', 'version', 'help'):
                    if 'type' not in i and 'nargs' not in i:
                        yield i
                else:
                    yield i
            except Exception:
                yield i

    def arg_gen(self):
        import argparse
        prefixes = ['--']
        types = [None, str, int, float, argparse.FileType('w'), argparse.FileType('r')]
        nargs = [None, 1, 2, '+', '*', '?']
        actions = [None, 'store', 'store_true', 'store_false',
                   'append', 'count', 'version', 'help']

        a0 = list(self.dict_product([{}], 'type', types))
        a1 = list(self.dict_product(a0, 'nargs', nargs))
        a2 = list(self.dict_product(a1, 'action', actions))
        a3 = list(self.dict_product(a2, 'prefix', prefixes))

        for x in self.__blacklist(a3):
            prefix = x['prefix']
            id = self.__gen_id(x)
            del x['prefix']
            yield {'args': prefix + id,
                   'kwargs': x}


    def parse_args(self, args, **setup):
        import argparse
        parser = argparse.ArgumentParser(**setup)

        for arg in self.arg_gen():
            print(arg)
            parser.add_argument(arg['args'], **arg['kwargs'])
        return parser.parse_args(args)


class SimpleTests(TestCase):
    pass
