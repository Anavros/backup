
"""
Entry point for a collection of related backup utilities.
"""

import os
from subprocess import Popen

import load
from constants import HOME


def dest(source, destroot):
    return os.path.join(destroot, source.replace(HOME, ''))


def ensure_mkdir(dest):
    Popen(['mkdir', '-p', os.path.dirname(dest)]).wait()


def piecewise(files, destroot):
    for f in files:
        d = dest(f, destroot)
        ensure_mkdir(d)
        print(f, '->', d)
        Popen(['rsync', '-am', f, d]).wait()


def link(files, destroot):
    for f in files:
        d = dest(f, destroot)
        ensure_mkdir(d)
        print(f, '<=>', d)
        Popen(['cp', '-al', f, d]).wait()


def tarball(files, d):
    print("Tarring files into {}...".format(d))
    Popen(['tar', 'czf', d] + files).wait()


def main(args):
    d = os.path.abspath(args.dest)
    files = load.filelist(args.file)

    # Safe functions.
    if args.task == 'list':
        for f in files:
            print(f)
            #print("-> ", dest(f, d))

    # Dangerous functions.
    if args.task in ['sync', 'link', 'ball'] and not args.safety_off:
        print("Safety on! Call again with --safety-off.")
        return

    elif args.task == 'sync':
        piecewise(files, d)

    elif args.task == 'link':
        link(files, d)

    elif args.task == 'ball':
        tarball(files, args.dest)

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
