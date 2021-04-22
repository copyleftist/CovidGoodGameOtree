from otree.api import Currency as c
from . import pages
from step2._builtin import Bot
import time
import numpy as np


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            # time.sleep(120)
            yield pages.Instruction1
        time.sleep(1+np.random.random())
        yield pages.Disclose, dict(disclose=True)
        time.sleep(1+np.random.random())
        yield pages.Contribute, dict(contribution=c(5))
        time.sleep(5)
        yield pages.Results
