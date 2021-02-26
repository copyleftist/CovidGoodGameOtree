from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Instruction1(Page):
    pass

class Disclose(Page):
    form_model = 'player'
    form_fields = ['disclose']


class DiscloseWaitPage(WaitPage):
    after_all_players_arrive = 'see_opponent_type'


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Instruction1, Disclose, DiscloseWaitPage, Contribute, ResultsWaitPage, Results]
