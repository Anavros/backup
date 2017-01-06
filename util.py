
import os
from subprocess import Popen
from datetime import datetime
from constants import HOME


def ensure_mkdir(dest):
    Popen(['mkdir', '-p', os.path.dirname(dest)]).wait()


def dest(source, destroot):
    return os.path.join(destroot, source.replace(HOME, ''))


def generate_name(configname):
    now = datetime.now()
    name = "{now.year}_{now.month}_{now.day}_{name}.tar.gz".format(
        now=now, name=configname)
    return name
