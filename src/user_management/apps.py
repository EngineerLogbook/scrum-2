from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    name = 'user_management'

    def ready(self):
        import user_management.signals