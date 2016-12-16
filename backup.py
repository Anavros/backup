
"""
Entry point for a collection of related backup utilities.
"""

import os
from subprocess import Popen

import load


HOME = os.path.expanduser('~/')
SYNCROOT = os.path.join(HOME, 'backup', 'sync')
LINKROOT = os.path.join(HOME, 'backup', 'link')


def dest(source, destroot):
    return os.path.join(destroot, source.lstrip(HOME))


def ensure_mkdir(dest):
    Popen(['mkdir', '-p', os.path.dirname(dest)]).wait()


def piecewise(files, destroot):
    for f in files:
        d = dest(f, destroot)
        ensure_mkdir(d)
        Popen(['rsync', '-avm', f, d]).wait()


def link(files, destroot):
    for f in files:
        d = dest(f, destroot)
        ensure_mkdir(d)
        Popen(['cp', '-al', f, d]).wait()


def main(args):
    d = os.path.abspath(args.dest)
    if args.task == 'list':
        files = load.filelist(args.file)
        for f in files:
            print(f)
            #print("-> ", dest(f, d))
    elif args.task == 'sync':
        if not args.safety_off:
            print("Safety on! Call again with --safety-off.")
            return
        files = load.filelist(args.file)
        piecewise(files, d)
    elif args.task == 'link':
        if not args.safety_off:
            print("Safety on! Call again with --safety-off.")
            return
        files = load.filelist(args.file)
        link(files, d)
    else:
        print("Unknown task:", args.task)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    parser.add_argument("file")
    parser.add_argument("dest")
    parser.add_argument("--safety-off", action='store_true')
    main(parser.parse_args())
