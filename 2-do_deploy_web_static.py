#!/usr/bin/python3
"""script that distributes an archive to your web servers
"""


from os.path import exists
from fabric.api import *
from datetime import datetime


env.hosts = ['100.25.181.19', '100.26.230.222']


def do_deploy(archive_path):
    """Fabric script that distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    file_archive = archive_path.split('/')[-1]
    file_tgz = '/data/web_static/releases/' + "{}".format(file_archive.split('.')[0])
    tmp = "/tmp/" + file_archive

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(file_tgz))
        run("tar -xzf {} -C {}/".format(tmp, file_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(file_tgz, file_tgz))
        run("rm -rf {}/web_static".format(file_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(file_tgz))
        return True
    except:
        return False
