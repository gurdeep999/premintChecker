from selenium import webdriver
import os
from prettytable import PrettyTable
from Premint.verification import Verification
from utils import get_base_url, get_wallets


class Premint(webdriver.Chrome):
    def __init__(self, driver_path=r'D:\python\SeleniumDrivers', teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        self.base_url = get_base_url()
        self.wallets = get_wallets()
        self.results = []
        os.environ['PATH'] += self.driver_path
        super(Premint, self).__init__()
        self.maximize_window()
        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def verify_wallets(self):
        print("Fetching results. Please wait...")
        for wallet in self.wallets:
            # self.get(f"{self.base_url}/verify/?wallet={wallet}")
            url = f"{self.base_url}/verify/?wallet={wallet}"
            verify = Verification(self)
            verify.land_page(url)
            phrase = verify.check_win()
            self.results.append([wallet, phrase])

    def display_results(self):
        print("Displaying Results...")
        table = PrettyTable(
            field_names=["Wallet", "Result"]
        )
        table.add_rows(self.results)
        print(table)
