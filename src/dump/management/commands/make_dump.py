from __future__ import unicode_literals
from datetime import datetime
from subprocess import check_output
import os
import zipfile

from django.conf import settings
from django.core.management.base import NoArgsCommand
from YaDiskClient.YaDiskClient import YaDisk, YaDiskException


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        disk = YaDisk(settings.DUMP_ACCOUNT_NAME, settings.DUMP_PASSWORD)

        def save_mkdir(dir):
            try:
                disk.mkdir(dir)
            except YaDiskException:
                pass

        now = datetime.now()
        save_mkdir('Backup')
        save_mkdir('Backup/db')
        save_mkdir('Backup/db/%s' % now.strftime('%Y_%m'))

        dump_filename = '%s_backup_%s.sql' % (settings.DATABASES['default']['NAME'], now.strftime('%Y%m%d_%H%M'))
        tmp_filename = dump_filename + '.gz'
        tmp = open(tmp_filename, 'wb')

        dump = check_output([
            'mysqldump',
            '--user=' + settings.DATABASES['default']['USER'],
            '--password=' + settings.DATABASES['default']['PASSWORD'],
            '--host=' + settings.DATABASES['default']['HOST'],
            settings.DATABASES['default']['NAME'],
        ])

        archive = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
        archive.writestr(dump_filename, dump)
        archive.close()

        tmp.close()

        disk.upload(tmp_filename, 'Backup/db/%s/%s' % (now.strftime('%Y_%m'), tmp_filename))

        os.remove(tmp_filename)
