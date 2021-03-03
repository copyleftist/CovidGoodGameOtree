from otree.api import Currency as c
from . import pages
from step1._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        yield pages.Contribute, dict(contribution=c(1))
        yield pages.Results
