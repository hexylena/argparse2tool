import argparse

parser = argparse.ArgumentParser(description='Process some integers.', prefix_chars='-+')
parser.add_argument('keyword', metavar='Q', type=str, nargs=1,
        help='action keyword')

parser.add_argument('integers', metavar='N', type=int, nargs='+',
        help='an integer for the accumulator')

parser.add_argument('--sum', '-s', dest='accumulate', action='store_const',
        const=sum, default=max, help='sum the integers (default: find the max)')

parser.add_argument('--foo', nargs='?', help='foo help')
parser.add_argument('--file', nargs='?', help='foo help', type=file)
parser.add_argument('--bar', nargs='*', default=[1, 2, 3], help='BAR!')
#parser.add_argument('+f', action='store_const', const='43')
parser.add_argument('--true', action='store_true', help='Store a true')
parser.add_argument('--false', action='store_false', help='Store a false')
parser.add_argument('--append', action='append', help='Append a value')


parser.add_argument('--version', action='version', version='2.0')
args = parser.parse_args()
print vars(args)
