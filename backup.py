
"""
Entry point for a collection of related backup utilities.
"""

import os
from subprocess import Popen

import load
import util
from constants import HOME


def main(args):
    files = load.filelist(args.file)

    # Safe functions.
    if args.task == 'list':
        for f in files:
            print(f)
            #print("-> ", dest(f, d))

    elif args.task == 'size':
        total = 0  # bytes
        pairs = []
        for f in files:
            s = os.path.getsize(f)
            pairs.append((s, f))
            total += s
        for s, f in sorted(pairs, key=lambda x: x[0]):
            print(s, f)
        print("Total:", total, "Bytes")

    elif args.task == 'covered':
        if not args.dest:
            print("No file given to check.")
        d = os.path.abspath(args.dest)
        if d in files:
            print(d, "is covered by", args.file)
        else:
            print(d, "is NOT covered by", args.file)

    # Dangerous functions.
    elif args.task in ['sync', 'link', 'ball']:
        if not args.safety_off:
            print("Safety on! Call again with --safety-off.")
            return
        if not args.dest:
            print("Missing destination folder.")
        d = os.path.abspath(args.dest)

        if args.task == 'sync':
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
    parser.add_argument("-d", "--dest")
    parser.add_argument("--safety-off", action='store_true')
    main(parser.parse_args())
