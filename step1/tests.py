from otree.api import Currency as c, Submission

from . import pages
from step2._builtin import Bot
import time
import numpy as np


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            # time.sleep(120)
            yield pages.Instruction1
        yield pages.Disclose, dict(disclose=True, RT=1)
        yield Submission(pages.Contribute, dict(contribution=c(5), RT=1), check_html=False)
        yield pages.Results
