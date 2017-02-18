
import os
from datetime import datetime
from subprocess import Popen


def list(files):
    for f in files:
        print(f)


def size(files):
    total = 0  # bytes
    pairs = []
    for f in files:
        s = os.path.getsize(f)
        pairs.append((s, f))
        total += s
    for s, f in sorted(pairs, key=lambda x: x[0]):
        print(s, f)
    print("Total:", total, "Bytes")


def link(files, d):
    Popen(['cp', '-al', '--parents'] + files + [d]).wait()


def sync(files, d):
    Popen(['rsync', '-Ram', '--delete'] + files + [d]).wait()


def ball(files, d, bconfig):
    name = "{now.year}_{now.month}_{now.day}_{name}.tar.gz".format(
        now=datetime.now(), name=os.path.basename(bconfig).split('.')[0])
    path = os.path.join(d, name)
    Popen(['tar', 'czf', path] + files).wait()
