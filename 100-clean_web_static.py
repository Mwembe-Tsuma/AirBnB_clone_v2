#!/usr/bin/python3
"""script that distributes an archive to your web servers
"""


from os.path import exists
from fabric.api import *


env.hosts = ['100.25.181.19', '100.26.230.222']


def do_clean(number=0):
    ''' Removes out of date archives '''

    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for fd in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [fd for fd in archives if "web_static_" in fd]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for fd in archives]
