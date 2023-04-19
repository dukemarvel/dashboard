from django.core.management.base import BaseCommand
import MetaTrader5 as mt5
import time
from accounts.models import EquityData
import datetime
import os
from django.conf import settings




class Command(BaseCommand):
    help = 'Fetch data from MetaTrader 5 accounts'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accounts = [
            {
                "server": settings.ACCOUNT1_SERVER,
                "login": settings.ACCOUNT1_LOGIN,
                "password": settings.ACCOUNT1_PASSWORD,
                "platform": "MT5",
                'path': settings.ACCOUNT1_PATH
            },
            {
                "server": settings.ACCOUNT2_SERVER,
                "login": settings.ACCOUNT2_LOGIN,
                "password": settings.ACCOUNT2_PASSWORD,
                "platform": "MT5",
                'path': settings.ACCOUNT2_PATH
            },
            {
                "server": settings.ACCOUNT3_SERVER,
                "login": settings.ACCOUNT3_LOGIN,
                "password": settings.ACCOUNT3_PASSWORD,
                "platform": "MT5",
                'path': settings.ACCOUNT3_PATH
            }
        ]


    def initialize(self, account):
        if not mt5.initialize(account['path'], timeout=20000):
            print(f"initialize() failed, error code {mt5.last_error()}")
        else:
            self.account_login(account)

    def account_login(self, account):
        if mt5.login(account['login'], account['password'], account['server']):
            print(f"Logged in successfully for account {account['login']}")
        else:
            print(f"Login failed for account {account['login']}, error code: {mt5.last_error()}")

    def get_account_data(self, account):
        self.initialize(account)

        account_info = mt5.account_info()
        symbol_tick = mt5.symbol_info_tick("EURUSD")
        if symbol_tick is None:
            print(f"Error getting symbol info tick for account {account['login']}: {mt5.last_error()}")
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
            for account in self.accounts:
                account_data = self.get_account_data(account)
                if account_data:
                    account_data["account_id"] = account['login']  # account login as account_id
                    EquityData(**account_data).save()

            time.sleep(60)
