
import util
from subprocess import Popen


def link(files, destroot):
    for f in files:
        d = util.dest(f, destroot)
        util.ensure_mkdir(d)
        print(f, '<=>', d)
        Popen(['cp', '-al', f, d]).wait()


def sync(files, destroot):
    for f in files:
        d = util.dest(f, destroot)
        util.ensure_mkdir(d)
        print(f, '->', d)
        Popen(['rsync', '-am', '--delete', f, d]).wait()


def tarball(files, d):
    print("Tarring files into {}...".format(d))
    Popen(['tar', 'czf', d] + files).wait()
