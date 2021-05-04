from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import threading
import argparse
import time
import numpy as np
from settings import SESSION_CONFIGS
# from step1.pages import DROPOUT_TIME
# from step1.models import Constants

CHROMEDRIVER = \
    'C:/Users/Basile/.wdm/drivers/chromedriver/win32/90.0.4430.24/chromedriver.exe'


class Bot:
    def __init__(self, idx, url, slow=False):
        super().__init__()

        self.idx = idx

        # with threading.Lock():
        self.driver = webdriver.Chrome(CHROMEDRIVER)
        self.driver.get(url)

        self.slow = slow

    @property
    def time_wait(self):
        if self.slow:
            return np.random.choice(np.linspace(2, 7+2, 10))

        return np.random.choice(np.linspace(2, 3, 10))

    def find(self, el_id):
        while True:
            try:

                return self.driver.find_element_by_id(el_id)

            except Exception as e:
                print(f'Bot {self.idx}: {e}')
                try:
                    self.driver.find_element_by_id('dropout')
                    exit('Bot is dropout')
                except:
                    time.sleep(1)

    def wait_until_el(self, el_id):
        timeout = 15
        try:
            element_present = EC.presence_of_element_located((By.ID, el_id))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print(f"Bot {self.idx}: Timed out waiting for page to load")
            try:
                self.driver.find_element_by_id('dropout')
                exit(f'Bot {self.idx} is dropout')
            except:
                pass

    def run(self):
        #instructions
        # self.wait_until_el('next')
        # self.submit()

        for _ in range(3):

            self.wait_until_el('disc')
            time.sleep(self.time_wait)
            self.disclose()

            self.wait_until_el('slider')
            time.sleep(self.time_wait)
            self.contribute()

            self.wait_until_el('results')
            time.sleep(3)
            self.submit()
        exit()

    def disclose(self):
        btn = self.find('disc')
        btn.click()

    def contribute(self):
        # self.set_value(slider, 5)
        btn = self.find('ok')
        btn.click()

    def set_value(self, el, v):
        self.driver.execute_script(f"arguments[0].setAttribute('value', {v})", el)

    def submit(self):
        form = self.find('form')
        form.submit()


def run(idx, url):
    time.sleep(1)
    slow = idx % 3 == 0
    b = Bot(url=url, idx=idx, slow=slow)
    print(f'Bot {b.idx} is running')
    b.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', help='global link for the experiment')
    args = parser.parse_args()

    n_bot = SESSION_CONFIGS[0]['num_demo_participants']
    n_process = n_bot

    with ThreadPool(processes=n_process) as pool:
        # idx = [(i, i+1, i+2) for i in range(0, n_bot, 3)]
        pool.starmap(run, [(i, args.url) for i in range(n_bot)])

