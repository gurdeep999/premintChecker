from selenium import webdriver
import os
from prettytable import PrettyTable
from Premint.verification import Verification
from utils import get_base_url, get_wallets
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class Premint(webdriver.Chrome):
    def __init__(self, teardown=False):

        self.teardown = teardown
        self.base_url = get_base_url()
        self.wallets = get_wallets()
        self.results = []

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')

        super(Premint, self).__init__(chrome_options=chrome_options,service=ChromeService(ChromeDriverManager().install()))
        self.maximize_window()
        self.implicitly_wait(10)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def verify_wallets(self):
        print("Fetching results. Please wait...")
        try:
            for wallet in self.wallets:
                # if using regex
                # self.get(f"{self.base_url}/verify/?wallet={wallet}")

                url = f"{self.base_url}/verify/?wallet={wallet}"

                verify = Verification(self)
                verify.land_page(url)
                phrase = verify.check_win()
                self.results.append([wallet, phrase])

        except Exception as e:
            self.get_screenshot_as_file("screenshot.png")
            print(e)

    def display_results(self):
        print("Displaying Results...")
        table = PrettyTable(
            field_names=["Wallet", "Result"]
        )
        table.add_rows(self.results)
        print(table)
