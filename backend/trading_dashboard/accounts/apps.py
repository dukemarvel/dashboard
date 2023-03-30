from django.apps import AppConfig
import threading

class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .management.commands.fetch_data import Command

        def run_handle_method():
            command_instance = Command()
            command_instance.handle()

        t = threading.Thread(target=run_handle_method)
        t.setDaemon(True)
        t.start()
