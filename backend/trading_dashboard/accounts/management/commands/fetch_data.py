from django.core.management.base import BaseCommand
import MetaTrader5 as mt5
import time
from accounts.models import EquityData
import datetime

class Command(BaseCommand):
    help = 'Fetch data from MetaTrader 5 accounts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account = {
            "server": "MetaQuotes-Demo",
            "login": 5011829976,
            "password": "d6flborb",
            "platform": "MT5",
            'path': "C:/Program Files/MetaTrader 5/terminal64.exe"
        }

    def initialize(self):
        if not mt5.initialize(self.account['path'], timeout=20000):
            print(f"initialize() failed, error code {mt5.last_error()}")
        else:
            self.account_login()

    def account_login(self):
        if mt5.login(self.account['login'], self.account['password'], self.account['server']):
            print(f"Logged in successfully for account {self.account['login']}")
        else:
            print(f"Login failed for account {self.account['login']}, error code: {mt5.last_error()}")

    def get_account_data(self):
        self.initialize()

        account_info = mt5.account_info()
        symbol_tick = mt5.symbol_info_tick("EURUSD")
        if symbol_tick is None:
            print(f"Error getting symbol info tick for account {self.account['login']}: {mt5.last_error()}")
            mt5.shutdown()
            return None

        market_watch_time = datetime.datetime.fromtimestamp(symbol_tick.time).strftime('%Y-%m-%d %H:%M:%S')

        mt5.shutdown()

        return {
            "equity": account_info.equity,
            "balance": account_info.balance,
            "timestamp": market_watch_time
        }
    def handle(self, *args, **options):
        while True:
            account_data = self.get_account_data()
            if account_data:
                account_data["account_id"] = self.account['login']  # account login as account_id
                EquityData(**account_data).save()

            time.sleep(60)

