from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class Disclose(Page):
    form_model = 'player'
    form_fields = ['disclose']


class DiscloseWaitPage(WaitPage):
    pass


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    pass


page_sequence = [Disclose, DiscloseWaitPage, Contribute, ResultsWaitPage, Results]
