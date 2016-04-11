from django.apps import AppConfig
from django.contrib.auth import get_user_model

class RPGConfig(AppConfig):
    name = 'rpg'

    def ready(self):
        get_user_model().__unicode__ = lambda user: u"%s %s" % (user.last_name, user.first_name)

default_app_config = 'rpg.RPGConfig'
