from otree.api import Currency as c, Submission

from . import pages
from step1._builtin import Bot
import time
import numpy as np


# def call_live_method(method, **kwargs):
    # player = method.__self__.player
    # print(type(player))
    # print(player.slow)
    # method(1, dict(disclose=True, RT=0, time=5, contribution=5))
    # method(2, dict(disclose=True, RT=0, time=5, contribution=5))
    # method(2, dict(dis))
    # method(1, {"offer": 60})
    # method(2, {"accepted": True})


class PlayerBot(Bot):
    def play_round(self):

        if self.round_number == 1:
            yield Submission(pages.Instructions, dict(), check_html=False)

        # time_wait = np.random.random()
        # if self.slow:
        #     time_wait = np.random.randint(5, 20)

        time.sleep(3)
        # time.sleep(time_wait)

        yield Submission(pages.Disclose, dict(disclose=False, RT=0), check_html=False)

        # time_wait = np.random.random()
        # if self.slow:
        #     time_wait = np.random.randint(5, 20)
        # time.sleep(time_wait)
        time.sleep(3)

        yield Submission(pages.Contribute, dict(contribution=c(0), RT=0), check_html=False)
        yield pages.Results
