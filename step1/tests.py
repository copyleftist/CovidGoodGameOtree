from otree.api import Currency as c
from . import pages
from step2._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield pages.Instruction1
        yield pages.Disclose, dict(disclose=True)
        yield pages.Contribute, dict(contribution=c(5))
        yield pages.Results
