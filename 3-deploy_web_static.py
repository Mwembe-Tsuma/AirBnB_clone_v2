#!/usr/bin/python3
"""script that distributes an archive to your web servers
"""


from os.path import exists
from fabric.api import *
from datetime import datetime


env.hosts = ['100.25.181.19', '100.26.230.222']


def do_pack():
    """generates a .tgz archive the web_static folder
    """
    local("sudo mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(timestamp)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """Fabric script that distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    fd = archive_path.split('/')[-1]
    file_tgz = '/data/web_static/releases/' +\
        "{}".format(fd.split('.')[0])
    tmp = "/tmp/" + fd

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
    except ValueError:
        return False


def deploy():
    """ creates and distributes the archive servers
    """
    archive_path = do_pack()
    if exists(archive_path) is False:
        return False
    result = do_deploy(archive_path)
    return result
