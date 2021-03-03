from otree.api import Currency as c, currency_range
from step1._builtin import Page, WaitPage
from .models import Constants


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class Instruction1(Page):
    pass

class Disclose(Page):
    form_model = 'player'
    form_fields = ['disclose']


class DiscloseWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    after_all_players_arrive = 'record_round_data'


page_sequence = [Instruction1, Disclose, DiscloseWaitPage, Contribute, ResultsWaitPage, Results]
