#!/usr/bin/python
import argparse
import re
from collections import OrderedDict
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='Update requirements.txt with pip freeze result')
parser.add_argument('-i', dest="input", type=argparse.FileType('r'), default='requirements.txt')
parser.add_argument('-c', dest="command", default='pip freeze')
parser.add_argument('-o', dest="output", type=argparse.FileType('w', 0), default='requirements.txt')
parser.add_argument('--add-new', dest='add_new', action='store_true')
parser.set_defaults(add_new=False)

PIP_PATTERN = r'(?P<package>\w+)==(?P<version>.+)'


def upreq(args):
    # 1. Read current package list from file
    packages = OrderedDict()
    for package_info in args.input.readlines():
        m = re.match(PIP_PATTERN, package_info)

        if m:
            packages[m.group('package')] = m.group('version')

    # 2. Read package list from external command
    process = Popen(args.command.split(' '), stdout=PIPE)
    (output, err) = process.communicate()
    process.wait()

    for package_info in output.splitlines():
        m = re.match(PIP_PATTERN, package_info)

        if m:
            version = packages.get(m.group('package'))
            if version and version < m.group('version'):
                packages[m.group('package')] = m.group('version')

    # 3. Write package list to output file
    for package, version in packages.iteritems():
        args.output.write('{}=={}\n'.format(package, version))


def main():
    args = parser.parse_args()
    upreq(args)


if __name__ == '__main__':
    main()
