# fabfile for i
# by ez@smartstudy.co.kr

from fabric.api import *
from fabric.colors import *
import os, socket

env['prod']     = False
env['master']   = False
service         = 'ndc13'
service_id      = 9
fabhome         = '/home/svc/%s' % service
hostname        = socket.gethostname()
settings        = 'ndc.settings_prod'

def _title(s):
    print(blue(s, bold=True))

def _sudo(s):
    return os.system('sudo %s' % s)

def _do(s):
    return os.system('%s' % s)

def _python(s):
    return '%s/env/bin/python %s' % (fabhome, s)

def _manage(s):
    return _python('%s/manage.py %s --settings=%s' % (fabhome, s, settings))

def prod():
    _title('=== [PRODUCTION]')
    env['prod'] = True
    settings = 'ndc.settings_prod'

def master():
    _title('=== [MASTER]')
    env['master'] = True

def init():
    _title('\n--- Initializing')
    # prepare directories
    _sudo('mkdir /var/log/%s -p' % service)
    _sudo('mkdir /etc/init/%s -p' % service)

    # copy nginx configuration
    _sudo('rm -f /etc/nginx/sites-enabled/%s' % service)
    _sudo('cp %s/etc/nginx/%s /etc/nginx/sites-enabled/' % (fabhome, service))

    # copy upstart configuration
    _sudo('cp %s/etc/init/* /etc/init/%s/' % (fabhome, service))

def collectstatic():
    _title('\n--- Gathering static files')
    _do(_manage('collectstatic --noinput'))

def flush_compressed_files():
    _title('\n--- Flushing compressed css/js files')
    _sudo('rm -v %s/static/compress_cache/css/*' % fabhome)
    _sudo('rm -v %s/static/compress_cache/js/*' % fabhome)

def flush_thumbnail_files():
    _title('\n--- Flushing thumbnail files')
    _sudo(_manage('thumbnail clear'))
    _sudo(_manage('thumbnail cleanup'))

def flush_redis():
    _title('\n--- Flushing Redis')
    os.system('echo \'SELECT %s\nFLUSHDB\' | redis-cli' % service_id)

def start_nginx():
    _title('\n--- Starting Nginx')
    _sudo('service nginx start')

def stop_nginx():
    _title('\n--- Stopping Nginx')
    _sudo('service nginx stop')

def status_nginx():
    _title('\n--- Checking Nginx status')
    _sudo('service nginx status')

def start_uwsgi():
    _title('\n--- Starting uWSGI')
    _sudo('start %s/uwsgi' % service)

def stop_uwsgi():
    _title('\n--- Stopping uWSGI')
    _sudo('stop %s/uwsgi' % service)

def status_uwsgi():
    _title('\n--- Checking uWSGI status')
    _sudo('initctl status %s/uwsgi' % service)

def start_celery():
    _title('\n--- Starting Celery')
    _sudo('start %s/celeryd' % service)
    _sudo('start %s/celerycam' % service)

def stop_celery():
    _title('\n--- Stopping Celery')
    _sudo('stop %s/celeryd' % service)
    _sudo('stop %s/celerycam' % service)

def status_celery():
    _title('\n--- Checking Celery status')
    _sudo('initctl status %s/celeryd' % service)
    _sudo('initctl status %s/celerycam' % service)

def start():
    collectstatic()
    start_uwsgi()
#    if env['master']:
#        start_celery()

def stop():
    stop_uwsgi()
#    if env['master']:
#        stop_celery()

def restart():
    stop()
    start()

def restart_nginx():
    stop_nginx()
    start_nginx()

def status():
    status_nginx()
    status_uwsgi()
    if env['master']:
        status_celery()

def syncdb():
    _do(_manage('syncdb --all'))

def migrate():
    _do(_manage('migrate --all'))

def migrate_fake():
    _do(_manage('migrate --all --fake'))

def flush():
    if env['master']:
        flush_redis()
        flush_thumbnail_files()
    #flush_compressed_files()

def restart_with_flush():
    stop()
    flush()
    start()

print(magenta('FABRIC : %s on %s' % (service, hostname), bold=True))
if hostname == 'beyonce': print red('I\'m in test environment.', bold=True); master()
if hostname == 'orange3': master()
