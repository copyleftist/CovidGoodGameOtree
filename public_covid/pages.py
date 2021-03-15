from otree.api import Currency as c, currency_range
<<<<<<< Updated upstream:public_covid/pages.py
from ._builtin import Page, WaitPage
=======
from step1._builtin import Page, WaitPage
>>>>>>> Stashed changes:step1/pages.py
from .models import Constants


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

class Instruction1(Page):
    pass

class Disclose(Page):
    form_model = 'player'
    form_fields = ['disclose']

    def is_displayed(self):
        return self.subsession.session.config['treatment'] != 2


class DiscloseWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Instruction1, Disclose, DiscloseWaitPage, Contribute, ResultsWaitPage, Results]
