from otree.api import Currency as c, currency_range
from step2._builtin import Page, WaitPage
from .models import Constants


class Init(WaitPage):
    after_all_players_arrive = 'init'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class Instruction1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Disclose(Page):

    form_model = 'player'
    form_fields = ['disclose']


class DiscloseWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'end_round'


class Results(Page):
    pass


page_sequence = [Init, Instruction1, Disclose, DiscloseWaitPage, Contribute, ResultsWaitPage, Results]
