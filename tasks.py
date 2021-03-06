
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
    print("{:,} Files".format(len(pairs)))
    print("Total: {:,} Bytes".format(total))


def link(files, d):
    print("Linking files to {}...".format(d))
    with open('/dev/null', 'w') as null:
        Popen(['cp', '-al', '--parents'] + files + [d], stderr=null).wait()


def sync(files, d):
    print("Syncing files to {}...".format(d))
    Popen(['rsync', '-Ram', '--delete'] + files + [d]).wait()


# TODO: Allow more than one per day.
def ball(files, d, bconfig):
    name = "{now.year}_{now.month}_{now.day}_{name}.tar.gz".format(
        now=datetime.now(), name=os.path.basename(bconfig).split('.')[0])
    path = os.path.join(d, name)
    print("Creating archive {}...".format(path))
    with open('/dev/null', 'w') as null:
        Popen(['tar', 'czf', path] + files, stderr=null).wait()
