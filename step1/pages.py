from otree.api import Currency as c, currency_range
from step2._builtin import Page, WaitPage
from .models import Constants


class Init(WaitPage):
    # template_name = 'step1/Wait.html'
    template_name = 'step1/Wait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1

    @staticmethod
    def vars_for_template():
        # with open('templates/step1/Contribute.html') as file:
        #     str = file.read()
        #     html = str.split('{#content#}')[1]

        return {'bg': ''}



class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        opp_character, opp_multiplier = [self.player.see_opponent_type(), ] * 2
        player_character, player_multiplier = [self.player.participant.multiplier, ] * 2

        if opp_multiplier is None:
            opp_multiplier = '...'

        if not self.player.disclose:
            player_multiplier = '...'
            player_character = None

        return {
            'player_character': 'img/{}.gif'.format(player_character),
            'opponent_character': 'img/{}.gif'.format(opp_character),
            'opponent_multiplier': opp_multiplier,
            'player_multiplier': player_multiplier
        }


class Instruction1(Page):
    def is_displayed(self):
        return self.round_number == 1


class Disclose(Page):
    form_model = 'player'
    form_fields = ['disclose']

    def vars_for_template(self):
        return {
            'player_character': 'img/{}.gif'.format(self.player.participant.multiplier)
        }


class DiscloseWaitPage(WaitPage):
    template_name = 'step1/Wait.html'
    # timeout_seconds = 120
    @staticmethod
    def vars_for_template():
        # with open('templates/step1/Contribute.html') as file:
        #     str = file.read()
        #     html = str.split('{#content#}')[1]

        return {'bg': ''}


class ResultsWaitPage(WaitPage):
    template_name = 'step1/Wait.html'
    # timeout_seconds = 120
    # template_name = 'step1/Wait.html'
    after_all_players_arrive = 'end_round'

    @staticmethod
    def vars_for_template():
        # with open('step1/templates/step1/Contribute.html') as file:
        #     str = file.read()
        #     html = str.split('{#content#}')[1]

        return {'bg': ''}


class Results(Page):
    pass


page_sequence = [Init, Instruction1, Disclose, DiscloseWaitPage, Contribute, ResultsWaitPage, Results]
