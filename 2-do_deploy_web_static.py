#!/usr/bin/python3
'''
Deploy files to remote server using Fabric

'''
from fabric.api import env, put, run
import os.path
env.hosts = ['web1.osala.tech', 'web2.osala.tech']


def do_deploy(archive_path):
    '''Upload achive to web servers'''
    if not os.path.isfile(archive_path):
        return False
    try:
        filename = archive_path.split('/')[-1]
        no_ext = filename.split('.')[0]
        path_no_ext = '/data/web_static/releases/{}/'.format(no_ext)
        symlink = '/data/web_static/current'
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_no_ext))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path_no_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv {}web_static/* {}'.format(path_no_ext, path_no_ext))
        run('rm -rf {}web_static'.format(path_no_ext))
        run('rm -rf {}'.format(symlink))
        run('ln -s {} {}'.format(path_no_ext, symlink))
        return True
    except Exception:
        return False
