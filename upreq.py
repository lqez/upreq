#!/usr/bin/python
import argparse
import re
from collections import OrderedDict
from subprocess import Popen, PIPE

parser = argparse.ArgumentParser(description='Update requirements.txt with pip freeze result')
parser.add_argument('-i', dest='input', default='requirements.txt')
parser.add_argument('-c', dest='command', default='pip freeze')
parser.add_argument('-o', dest='output', default='requirements.txt')
parser.add_argument('--add-new', dest='add_new', action='store_true')
parser.set_defaults(add_new=False)

PACKAGE_RULES = {
    'pip': {
        'pattern': r'(?P<package>[^=]+)==(?P<version>.+)',
        'output': '{package}=={version}',
    },
    'egg': {
        'pattern': r'(?P<package_url>[^#]+)#egg=(?P<package>.+)',
        'output': '{package_url}#egg={package}',
    },
}


def upreq(args):
    packages = OrderedDict()

    # 1. Read current package list from file
    fh = open(args.input, 'r')
    for package_str in fh.readlines():
        for package_type, rule in PACKAGE_RULES.iteritems():
            m = re.match(rule['pattern'], package_str)
            if m:
                packages[m.group('package')] = {'type': package_type}
                packages[m.group('package')].update(m.groupdict())
    fh.close()

    # 2. Read package list from external command
    process = Popen(args.command.split(' '), stdout=PIPE)
    (output, err) = process.communicate()
    process.wait()

    for package_str in output.splitlines():
        for package_type, rule in PACKAGE_RULES.iteritems():
            m = re.match(rule['pattern'], package_str)
            if m:
                package = packages.get(m.group('package'))
                if package:
                    version = package.get('version')
                    if version and version < m.group('version'):
                        package['version'] = m.group('version')
                        print('[UPDATE] {package} to {version}'.format(**m.groupdict()))

    # 3. Write package list to output file
    fh = open(args.output, 'w')
    for package, info in packages.iteritems():
        fh.write(PACKAGE_RULES[info['type']]['output'].format(**info) + '\n')
    fh.close()


def main():
    args = parser.parse_args()
    upreq(args)


if __name__ == '__main__':
    main()
