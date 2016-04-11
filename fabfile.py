# -*- coding: utf-8 -*-
import os
from datetime import date
from copy import copy
from fabric.api import *
from fabric.contrib.files import exists, append, upload_template

from fab_settings import *

env.directory = {
    'production': '/home/%s/projects/port' % SSH_USER,
}
env.manage_dir = '%s/src'
env.activate = 'source %s/ENV/bin/activate'

env.deploy_user = env.user = SSH_USER
env.www_ssh_key = 'ssh-dss AAAAB3NzaC1kc3MAAACAbN+8KDO1jkRluNqiqO2KjkaSn4Qs66zBcV+JaUFrnoVt5tBaEMGW56ihtd1zmPqSufpDKTMXKneZWLAx8evFobvU5S32OKtFpR6oylZwIWg0SQNtjBE7lFHC5VnN4BtjpLp6DBzUOt6mTXYyCjaYhorMWmyw5641KXOsW0V7et0AAAAVALlYgGve+sIVrw7MTQFD4Hvb1utVAAAAgAGktSDpYw1sEC9tA593z3Ymk9r4J939DsKiL3d+RK/RXfY9KgoFtMHmCzL8goYpyWdaE2XQzCrIfp3EFW41NUWUfxsaDzXSEg4Q/CYAfJm7nNDpwv1eAq3c0Mw7RMGEw3pxsAnQrq0snHI7cVhdZ12Z6wO147+ybAbOXW7XF04sAAAAgGzFeuezmdfyS0N4VE42/kgC4SusMTxYOj5nrb8VRvzQ08Msa5FChXIWv0Fj5hMpOVX/gc4uEkbt7knpjqouo+K+8jadQ4I+sRidqG13U6b2UGJy844THSqL3HIhuPmhvWPOFjJbsNFxcoakSqLxn3ewkDzco7CH/aYo9u9VrLwk dsa-key-20080514'
env.env_type = 'production'

if not env.hosts:
    env.hosts = ['82.196.9.202']


def init():
    with settings(user='root'):
        append('/etc/apt/sources.list', 'deb-src http://archive.ubuntu.com/ubuntu precise main')
        append('/etc/apt/sources.list', 'deb-src http://archive.ubuntu.com/ubuntu precise-updates main')

        run('apt-get update')
        run('apt-get upgrade -y')
        run('apt-get install -y mc nginx mysql-client git-core python-setuptools python-dev rrdtool sendmail memcached fail2ban')
        run('apt-get build-dep -y python-mysqldb')
        run('apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev')  # Pillow dependencies

        if not exists('/home/%s' % SSH_USER):
            run('yes | adduser --disabled-password %s' % SSH_USER)
            run('mkdir /home/%s/.ssh' % SSH_USER)
            run('echo "%s" >> /home/%s/.ssh/authorized_keys' % (env.www_ssh_key, SSH_USER))

        if not exists('/var/log/projects/port'):
            run('mkdir -p /var/log/projects/port')
            run('chmod 777 /var/log/projects/port')
            run('touch /var/log/projects/port/restart.log')
            run('chown -R %(user)s:%(user)s /var/log/projects/port' % {'user': SSH_USER})

        if exists('/etc/nginx/sites-enabled/default'):
            run('rm /etc/nginx/sites-enabled/default')

        if not exists('/etc/nginx/listen'):
            put('tools/nginx/listen', '/etc/nginx/listen')

        if not exists('/etc/nginx/sites-available/90-port.conf'):
            run('touch /etc/nginx/sites-available/90-port.conf')
            run('chown %s /etc/nginx/sites-available/90-port.conf' % SSH_USER)
        if not exists('/etc/nginx/sites-enabled/90-port.conf'):
            run('ln -s /etc/nginx/sites-available/90-port.conf /etc/nginx/sites-enabled/90-port.conf', shell=False)

        if not exists('/etc/init/port.conf'):
            run('touch /etc/init/port.conf')
            run('chown %s /etc/init/port.conf' % SSH_USER)

        append('/etc/sudoers', '%s ALL=(ALL) NOPASSWD:/sbin/restart port' % SSH_USER)

        run('mkdir -p /home/%s/projects/port' % SSH_USER)
        run('chown -R %(user)s:%(user)s /home/%(user)s' % {'user': SSH_USER})


def production():
    upload()
    environment()
    local_settings()
    nginx()
    upstart()
    dump()
    migrate()
    collect_static()
    restart()


def upload():
    directory = env.directory[env.env_type]
    os.chdir(os.path.dirname(__file__))
    local('git archive HEAD | gzip > archive.tar.gz')
    put('archive.tar.gz', directory + '/archive.tar.gz')
    with cd(directory):
        run('tar -zxf archive.tar.gz')
        run('rm archive.tar.gz')
    local('del archive.tar.gz')


def virtualenv(command):
    with cd(env.directory[env.env_type]):
        run(env.activate % env.directory[env.env_type] + ' && ' + command)


def environment():
    with cd(env.directory[env.env_type]):
        with settings(warn_only=True):
            run('python virtualenv.py ENV')
        virtualenv('pip install -r requirements.txt')


def local_settings():
    os.chdir(os.path.dirname(__file__))
    manage_dir = env.manage_dir % env.directory[env.env_type]
    params = copy(globals())
    params['ENV_TYPE'] = env.env_type

    with cd(manage_dir):
        upload_template(
            'src/local_settings.py.sample',
            'local_settings.py',
            params,
            backup=False
        )


def nginx():
    run('cp %s/tools/nginx/90-port.conf /etc/nginx/sites-available/90-port.conf' % env.directory[env.env_type], shell=False)


def upstart():
    run('cp %s/tools/upstart/port.conf /etc/init/port.conf' % env.directory[env.env_type], shell=False)


def dump():
    with cd(env.directory[env.env_type]):
        tmp_filename = run("date +/tmp/port_backup_%Y%m%d_%H%M.sql.gz")
        month_dir = date.today().strftime("%Y_%m")
        backup_dir = "Backup/db/%s" % month_dir
        webdav_command =\
            "import easywebdav;"\
            "webdav = easywebdav.connect('webdav.yandex.ru', username='glader.dump', password='%s', protocol='https');"\
            "webdav.mkdirs('%s');"\
            "webdav.upload('%s', '%s/%s');" % (DUMP_PASSWORD, backup_dir, tmp_filename, backup_dir, tmp_filename.split('/')[-1])

        run("mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s | gzip > " % globals() + tmp_filename)
        virtualenv('python -c "%s"' % webdav_command)
        run("rm %s" % tmp_filename)


def manage_py(command):
    manage_dir = env.manage_dir % env.directory[env.env_type]
    virtualenv('cd %s && python manage.py %s' % (manage_dir, command))


def migrate():
    manage_py('syncdb')
    manage_py('migrate')


def collect_static():
    run('mkdir -p %s/static' % env.directory[env.env_type])
    manage_py('collectstatic -c --noinput')


def restart():
    run('sudo restart port')


def gunicorn():
    manage_py("run_gunicorn --bind 'unix:%s/wsgi.sock'" % env.directory[env.env_type])

#------------------------------------------------------------------------------------------

def enter(args):
    local('cd src && ..\\ENV\\Scripts\\python manage.py %s' % args)


def run_local():
    enter('runserver 0.0.0.0:8000')


def local_env():
    with settings(warn_only=True):
        local('c:\\python\\python virtualenv.py ENV --system-site-packages')
    local('ENV\\Scripts\\pip install -r requirements.txt ')


def local_static():
    enter('collectstatic -c --noinput')


def update_local_db():
    run("mysqldump -u %(DATABASE_USER)s -p%(DATABASE_PASSWORD)s -h %(DATABASE_HOST)s %(DATABASE_DB)s > dump.sql" % globals())
    get("dump.sql", "dump.sql")
    run("rm dump.sql")
    local("mysql -uroot %(DATABASE_DB)s < dump.sql" % globals())
    local("del dump.sql")


def local_migrate():
    with settings(warn_only=True):
        enter('makemigrations')
    enter('migrate')
