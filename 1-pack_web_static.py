'''
A script to generate .tgz file from the contents of webstatic
'''
from fabric.api import local
from time import strftime


def do_pack():
    '''Generate required files'''
    timenow = strftime('%Y%M%d%H%M%S')
    try:
        local('mkdir -p versions')
        filename = f'versions/web_static_{timenow}.tgz'
        local(f'tar -czfv {filename} web_static/')
        return filename
    except Exception:
        return None

if __name__ == '__main__':
    do_pack()
