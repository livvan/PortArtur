# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from yafotki.fields import YFField
from redactor.fields import RedactorField

ALBUM = getattr(settings, 'YAFOTKI_ALBUM', 'default')
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Role(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Пользователь', null=True, blank=True, default=None)
    name = models.CharField(verbose_name='Фамилия Имя', max_length=255)
    year = models.IntegerField(verbose_name='Год рождения')
    fatherland = models.CharField(verbose_name='Место рождения', max_length=255)
    description = RedactorField(verbose_name='Общеизвестная информация')
    secret = RedactorField(verbose_name='Скелет в шкафу')
    work = models.CharField(verbose_name='Место работы', max_length=255, null=True, blank=True, default=None)
    conviction = RedactorField(verbose_name='Судимость', null=True, blank=True, default=None)
    quest = RedactorField(verbose_name='Квента')
    face = YFField(verbose_name='Фото в фас', upload_to=ALBUM, null=True, blank=True, default=None)
    halfface = YFField(verbose_name='Фото в профиль', upload_to=ALBUM, null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name='Заморожена', default=False,
                                    help_text='Можно ли человеку редактировать роль')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('role', args=[self.pk])

    def username(self):
        if not self.user:
            return '-'

        userinfo = self.get_userinfo()
        name = '%s %s' % (self.user.last_name, self.user.first_name)
        if userinfo.nick:
            name += ' (%s)' % userinfo.nick
        return name
    username.short_description = 'Игрок'

    def role_name(self):
        return self.name
    role_name.short_description = 'Персонаж'

    def save(self, check_diff=True, *args, **kwargs):
        if check_diff:
            report = ''
            if self.pk:
                prev = self.__class__.objects.get(pk=self.pk)
                header = 'измененные поля роли %s' % self.name
                for field in self._meta.fields:
                    if getattr(self, field.name) != getattr(prev, field.name):
                        report += '%s: "%s" -> "%s"\n' % (field.verbose_name, getattr(prev, field.name) or '-',
                                                          getattr(self, field.name) or '-')
            else:
                header = 'новая роль %s:' % self.name
                for field in self._meta.fields:
                    report += '%s: "%s"\n' % (field.verbose_name, getattr(self, field.name) or '-')

            if report:
                emails = [settings.MANAGERS[0][1]]
                if self.user:
                    emails.append(self.user.email)

                send_mail(
                    'ПортАртур: ' + header,
                    report + '\n\n(http://%s/role/%s)' % (settings.DOMAIN, self.id),
                    None,
                    emails,
                )

        super(Role, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class RoleConnection(models.Model):
    role = models.ForeignKey(Role, verbose_name='Роль', related_name='connections')
    role_rel = models.ForeignKey(Role, verbose_name='Связанная роль',
                                 related_name='rel_connections', null=True, blank=True)
    comment = models.TextField(verbose_name='Описание', null=True, blank=True, default=None)
    is_locked = models.BooleanField(verbose_name='Заморожено', default=False)

    def save(self, *args, **kwargs):
        emails = [settings.MANAGERS[0][1]]
        if self.role.user:
            emails.append(self.role.user.email)

        if self.pk:
            prev = self.__class__.objects.get(pk=self.pk)
            if getattr(self, 'comment') != getattr(prev, 'comment'):
                report = \
                    'Анкета: http://%s/role/%s/relations\n\nИзмененная связь: %s -> %s:\nБыло: %s\nСтало: "%s"' %\
                    (settings.DOMAIN, self.role_id, self.role, self.role_rel,
                     getattr(prev, 'comment') or '-', getattr(self, 'comment') or '-')

                send_mail(
                    'ПортАртур: изменения в связях роли %s' % self.role,
                    report,
                    None,
                    emails,
                )
        else:
            send_mail(
                'ПортАртур: новая связь между ролями',
                'Анкета: http://%s/role/%s/relations\n\n%s -> %s\n\n%s'
                % (settings.DOMAIN, self.role_id, self.role, self.role_rel, self.comment),
                None,
                emails,
            )

        return super(RoleConnection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Связь ролей'
        verbose_name_plural = 'Связи ролей'
