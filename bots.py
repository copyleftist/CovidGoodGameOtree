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
import os
import numpy as np
from settings import SESSION_CONFIGS
# from step1.pages import DROPOUT_TIME
# from step1.models import Constants

if os.name == 'nt':
    CHROMEDRIVER = \
        'C:/Users/Basile/.wdm/drivers/chromedriver/win32/90.0.4430.24/chromedriver.exe'
else:
    CHROMEDRIVER = '/usr/lib/chromium-browser/chromedriver'


class Bot:
    def __init__(self, idx, url, p_disclose, p_contrib, slow=False):
        super().__init__()

        self.idx = idx
        self.p_contrib = p_contrib
        self.p_disclose = p_disclose

        with mp.Lock():
            options = webdriver.ChromeOptions()
            # options.add_argument('headless')
            self.driver = webdriver.Chrome(CHROMEDRIVER, options=options)
            self.driver.get(url)

        self.slow = slow

    @property
    def time_wait(self):
        if self.slow:
            return np.random.choice(np.linspace(2, 20, 10))

        return np.random.choice(np.linspace(2, 3, 10))

    def find(self, el_id):
        while True:
            try:

                el = self.driver.find_element_by_id(el_id)
                return el

            except Exception as e:
                print(f'Bot {self.idx}: {e}')
                try:
                    self.driver.find_element_by_id('dropout')
                    exit('Bot is dropout')
                except:
                    time.sleep(1)

    def wait_until_el(self, el_id):
        timeout = 60
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

        for _ in range(15):

            self.wait_until_el('disc')
            time.sleep(self.time_wait)
            self.disclose()

            self.wait_until_el('slider')
            time.sleep(self.time_wait)
            self.contribute()

            # self.wait_until_el('results')
            # time.sleep(2)

        exit()

    def disclose(self):
        disclose = np.random.choice([False, True], p=[1-self.p_disclose, self.p_disclose])
        btn = self.find('disc') if disclose else self.find('hide')
        btn.click()

    def contribute(self):
        contrib = np.random.choice(range(1, 11), p=self.p_contrib)
        self.set_value('slider', contrib)
        btn = self.find('ok')
        btn.click()

    def set_value(self, el_id, v):
        self.driver.execute_script(f"$('#{el_id}').val({v})")

    def submit(self):
        form = self.find('form')
        form.submit()


def run(idx, url):
    time.sleep(1)
    slow = idx % 10 == 0
    p_contrib = np.ones(10)
    if idx < 10:
        p_contrib[idx] = 10
    else:
        i = int(str(idx)[1])
        p_contrib[i] = 10

    p_disclose = np.arange(11) / 10

    if idx < 10:
        p_disclose = p_disclose[idx]
    else:
        i = int(str(idx)[1])
        p_disclose = p_disclose[i]
    p_contrib = np.exp(p_contrib)/np.sum(np.exp(p_contrib))

    b = Bot(url=url+f"?participant_label=Bob{idx}", idx=idx, slow=slow, p_disclose=p_disclose, p_contrib=p_contrib)
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

