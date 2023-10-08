#!/usr/bin/python3
"""Module creates .tgz archive, distributes it to the web servers"""

import os
from fabric.api import local, cd, put, run, env, execute
from datetime import datetime

env.hosts = [
    '54.160.78.191',  # web-01',
    '54.146.88.214',  # web-02',
]

# env.usr = 'ubuntu'


def do_pack():
    """Generates a .tgz archive form contents of web static."""
    try:
        local("mkdir -p versions")
        current_time = datetime.now()
        archive_filename = "web_static_{}.tgz".format(
            current_time.strftime("%Y%m%d%H%M%S")
        )
        local("tar -czvf versions/{} web_static".format(archive_filename))
        return "versions/{}".format(archive_filename)
    except Exception as e:
        print("Error:", str(e))
        return None


def do_deploy(archive_path):
    """Deploys static files to our web servers.

    Atributes:
        archive_path(str): path to archive with our static files.
    Returns:
        True(bool): on success,
        False(bool): on fail.
    """
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_name_without_ext = os.path.splitext((archive_name))[0]

    # Check if the target directory already exists in releases
    path = '/data/web_static/releases/{}'.format(archive_name_without_ext)

    releases = run('ls -d {}web_static_*'.format('/data/web_static/releases/'))
    directories = [dir.strip() for dir in releases.stdout.strip().split('\n')]

    if path in directories:
        return True  # The archive is already deployed, nothing to do

    # Upload the archive to the /tmp/
    uploaded = put(archive_path, "/tmp/")

    if uploaded.failed:
        return False

    path = run('mkdir -p /data/web_static/releases/{}'.format(
                    archive_name_without_ext))
    if path.failed:
        return False

    path = '/data/web_static/releases/{}'.format(archive_name_without_ext)

    # uncompress
    uncompressed = run(
            "tar -xzvf /tmp/{} -C {}".format(archive_name, path)
            )
    if uncompressed.failed:
        return False

    run('rm -rf /tmp/{}'.format(archive_name))

    move = run("mv {}/web_static/* {}".format(path, path))
    if move.failed:
        return False

    # Create a new symbolic link
    with cd("/data/web_static"):
        rm_lnk = run("rm -rf /data/web_static/current")
        if rm_lnk.failed:
            return False

        update_lnk = run(
            "ln -sf  {} /data/web_static/current".format(
                    path,
                    )
        )

        if update_lnk.failed:
            return False
    return True


archive_created = False  # global variable to track archive createion
archive_filename = None  # Gloable variable to store archive filename


def deploy():
    """Creates a single archive and deploys it to multiple web servers."""
    global archive_created, archive_filename

    # check if archive has already been created
    if not archive_created:
        archive_filename = do_pack()
        if not archive_filename:
            return False
        archive_created = True  # set flag

    results = execute(do_deploy, archive_path=archive_filename)

    if False in results.values():
        return False
    return True
