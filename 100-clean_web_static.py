#!/usr/bin/python3
"""script that distributes an archive to your web servers
"""


from fabric.api import *
from datetime import datetime
import os

env.hosts = ['100.25.181.19', '100.26.230.222']


def deploy():
    """Fabric script that distributes an archive to your web servers"""
    file_archive = do_pack()
    if not file_archive:
        return False
    return do_deploy(file_archive)


def do_pack():
    '''
    Generates a tgz archive from
    '''
    try:
        local('mkdir -p versions')
        datestamp = '%Y%m%d%H%M%S'
        file_archive = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(datestamp))
        local('tar -cvzf {} web_static'.format(file_archive))
        print('web_static packed: {} -> {}'.format(file_archive,
              os.path.getsize(file_archive)))
        return file_archive
    except ValueError:
        return None


def do_deploy(file_archive):
    '''
    Deploy archive to web servers web_01 and web_02
    '''
    if not os.path.exists(file_archive):
        return False
    file_name = file_archive.split('/')[1]
    file_path = '/data/web_static/releases/'
    releases_path = file_path + file_name[:-4]
    try:
        put(file_archive, '/tmp/')
        run('mkdir -p {}'.format(releases_path))
        run('tar -xzf /tmp/{} -C {}'.format(file_name, releases_path))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}/'.format(releases_path, releases_path))
        run('rm -rf {}/web_static'.format(releases_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releases_path))
        print('New version deployed!')
        return True
    except ValueError:
        return False


def do_clean(number=0):
    ''' Removes out of date archives'''
    number = int(number)
    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions; ls -t | tail -n +{} | xargs rm -rf'
          .format(number))
    releases_path = '/data/web_static/releases'
    run('cd {}; ls -t | tail -n +{} | xargs rm -rf'
        .format(releases_path, number))
