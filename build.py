#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import platform
import subprocess
import time


def exec_command(cmd, log_path='out/build.log', **kwargs):
    with open(log_path, 'at') as f:
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True,
                                   **kwargs)
        for line in iter(process.stdout.readline, ''):
            sys.stdout.write(line)
            f.write(line)

    process.wait()
    ret_code = process.returncode

    if ret_code != 0:
        with open(log_path, 'at') as f:
            for line in iter(process.stderr.readline, ''):
                sys.stdout.write(line)
                f.write(line)
        print('you can check build log in {}'.format(log_path))
        raise Exception("{} failed, return code is {}".format(cmd, ret_code))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='action, build or clean path.',
                        nargs='*')
    parser.add_argument('-v', '--build_type', help='Release or debug version.',
                        nargs='*')
    args = parser.parse_args()

    product_path = './out/'
    log_path = os.path.join('./', 'build.log')

    args.action = ['build'] if not args.action else args.action

    if args.action[0] == 'build':
        gn_cmd = ''
        ninja_cmd = ''
        print("\n=== start build ===\n")
        if platform.system().find('Windows') == 0:
            gn_cmd = ['gn.exe', 'gen', product_path, '--root=.',
                      '--dotfile=./.gn']

            ninja_cmd = ['ninja.exe',
                         '-C', product_path]
        else:
            gn_cmd = ['gn', 'gen', product_path, '--root=.',
                      '--dotfile=./.gn']
            if args.build_type == 'debug':
                gn_cmd += ['--args=build_type=\"debug\"']

            ninja_cmd = ['ninja', '-C', product_path]
        print("=== gn working ===\n")
        exec_command(gn_cmd, log_path)
        time.sleep(2)
        print("\n=== ninja working ===")
        exec_command(ninja_cmd, log_path)
        print("build success!")
    elif args.action[0] == 'clean':
        clean_cmd = ''
        if not os.path.exists(product_path):
            print('Nothing to clean! No build found.')
            return 0
        print("\n=== start clean ===\n")
        if platform.system().find('Windows') == 0:
            clean_cmd = ['ninja.exe', '-C', product_path, '-t', 'clean']
        else:
            clean_cmd = ['ninja', '-C', product_path, '-t', 'clean']
        print("=== clean working ===\n")
        exec_command(clean_cmd, log_path)
        print("clean success!")


if __name__ == '__main__':
    sys.exit(main())
