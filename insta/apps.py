from django.apps import AppConfig


class InstaConfig(AppConfig):
    name = 'insta'

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import insta.signals