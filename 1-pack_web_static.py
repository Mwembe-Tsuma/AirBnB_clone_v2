#!/usr/bin/python3
"""Module creates .tgz archive of web_static using fabric."""


from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive form contents of web static."""
    try:
        local("mkdir -p versions")
        current_time = datetime.now()
        archive_filename = "web_static_{}.tgz".format(
                    current_time.strftime("%Y%m%d%H%M%S"))
        local("tar -czvf versions/{} web_static".format(archive_filename))
        return "versions/{}".format(archive_filename)
    except Exception as e:
        print("Erro:", str(e))
        return None
