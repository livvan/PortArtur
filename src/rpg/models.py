# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from redactor.fields import RedactorField

ALBUM = getattr(settings, 'YAFOTKI_ALBUM', 'default')
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Role(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Пользователь', null=True, blank=True, default=None)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    middle_name = models.CharField(verbose_name='Отчество', max_length=255)
    age = models.IntegerField(verbose_name='Возраст')
    title = models.CharField(verbose_name='Титул/звание', max_length=255)
    position = models.CharField(verbose_name='Должность', max_length=255)
    FAMILY_STATES = (
        ('married', 'женат/замужем'),
        ('date', 'есть сердечный друг'),
        ('widower', 'вдовец/вдова'),
        ('alone', 'сердечной привязанности нет'),
        ('none', 'все сложно'),
    )
    family_state = models.CharField(verbose_name='Семейное положение', max_length=255, choices=FAMILY_STATES)
    description = RedactorField(verbose_name='Общеизвестная информация')
    party = models.CharField(verbose_name='Партия', max_length=255, null=True, blank=True, default=None,
                             choices=(('war', 'Партия войны'), ('peace', 'Партия мира')))
    military = models.CharField(verbose_name='Военный', max_length=255, null=True, blank=True, default=None,
                                choices=(('army', 'Армия'), ('navy', 'Флот')))
    character_1 = models.CharField(verbose_name='Макаров / Стессель',
                                   max_length=255, null=True, blank=True, default=None,
                                   choices=(('1', 'Макаров'), ('2', 'Стессель')))
    character_2 = models.CharField(verbose_name='Вор / честный', max_length=255, null=True, blank=True, default=None,
                                   choices=(('1', 'Вор'), ('2', 'честный')))
    character_3 = models.CharField(verbose_name='Англофилы / Русофилы',
                                   max_length=255, null=True, blank=True, default=None,
                                   choices=(('1', 'Англофилы'), ('2', 'Русофилы')))
    character_4 = models.CharField(verbose_name='Революционеры/монархисты',
                                   max_length=255, null=True, blank=True, default=None,
                                   choices=(('1', 'Революционеры'), ('2', 'Монархисты')))
    character_5 = models.CharField(verbose_name='Россия/Япония',
                                   max_length=255, null=True, blank=True, default=None,
                                   choices=(('1', 'Россия'), ('2', 'Япония')))
    quest = RedactorField(verbose_name='Квента')

    def __unicode__(self):
        return "%s %s" % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse('rpg:role', args=[self.pk])

    def save(self, check_diff=True, *args, **kwargs):
        if check_diff:
            report = ''
            if self.pk:
                prev = self.__class__.objects.get(pk=self.pk)
                header = 'измененные поля роли %s' % self
                for field in self._meta.fields:
                    if getattr(self, field.name) != getattr(prev, field.name):
                        report += '%s: "%s" -> "%s"\n' % (field.verbose_name, getattr(prev, field.name) or '-',
                                                          getattr(self, field.name) or '-')
            else:
                header = 'новая роль %s:' % self
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

    def send_mail(self, subject, message):
        if self.user and self.user.email:
            send_mail(subject, message, None, [self.user.email])
        else:
            send_mail('Для %s: %s' % (self.name, subject), message, None, [settings.ADMINS[0][1]])

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
