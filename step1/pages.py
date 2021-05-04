from otree.api import Currency as c, currency_range
from step1._builtin import Page, WaitPage
from .models import Constants
import numpy as np

from utils.debug import logger


SECOND = 1000
DROPOUT_TIME = 6 * SECOND
INSTRUCTIONS_TIME = 2 * SECOND


class Init(WaitPage):
    template_name = 'step1/Wait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1

    @staticmethod
    def vars_for_template():
        from .instructions import panels, titles
        return {'panels': panels, 'titles': titles}

    @staticmethod
    def live_method(player, data):
        return {0: int(data['time']) > INSTRUCTIONS_TIME}


class Disclose(Page):

    def get_template_name(self):
        if self.participant.is_dropout:
            return 'step1/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()

    def vars_for_template(self):
        from .html import wait
        return {
            'player_character': 'img/{}.gif'.format(self.player.participant.multiplier),
            'html': wait
        }

    @staticmethod
    def live_method(player, data):

        if not player.response1:
            logger.debug(f'Participant {player.participant.id_in_session}'
                         ' saving disclosure response.')
            player.disclose = bool(data['disclose'])
            player.RT1 = int(data['RT'])
            player.response1 = True

        other_player = player.get_others_in_group()[0]
        too_long = int(data['time']) > DROPOUT_TIME

        if other_player.round_number != player.round_number:
            return {player.id_in_group: False}

        if other_player.response1:
            return {player.id_in_group: True}

        if too_long or other_player.participant.is_dropout:
            other_player.participant.is_dropout = True
            others = [player, ] + other_player.get_others_in_subsession()
            for p in others:
                if p.round_number != player.round_number:
                    return {player.id_in_group: False}
            real_participants = [p for p in others if not p.participant.is_dropout]
            response = [p.response1 for p in real_participants]
            if all(response):
                p_disclose = np.mean(
                    [p.disclose for p in real_participants]
                )
            else:
                logger.debug('Wait for all players to play before bots response')
                return {player.id_in_group: False}

            disclose = np.random.choice(
                [False, True], p=[1-p_disclose, p_disclose])

            other_player.disclose = disclose
            other_player.RT1 = 0
            other_player.response1 = True
            logger.debug(
                f'Participant {other_player.participant.id_in_session} dropped out.'
                f' Bot p(disclose)={p_disclose}')
            return {player.id_in_group: True}


class Contribute(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'step1/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()

    def vars_for_template(self):
        from .html import wait

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
            'player_multiplier': player_multiplier,
            'html': wait
        }

    @staticmethod
    def live_method(player, data):

        if not player.response2:
            logger.debug(f'Participant {player.participant.id_in_session}'
                         ' saving contribution response.')
            player.contribution = int(data['contribution'])
            player.RT2 = int(data['RT'])
            player.response2 = True

        other_player = player.get_others_in_group()[0]
        too_long = int(data['time']) > DROPOUT_TIME

        if other_player.round_number != player.round_number:
            return {player.id_in_group: False}

        if other_player.response2:
            player.group.end_round()
            return {player.id_in_group: True}

        if too_long or other_player.participant.is_dropout:
            other_player.participant.is_dropout = True
            others = [player, ] + other_player.get_others_in_subsession()
            for p in others:
                if p.round_number != player.round_number:
                    return {player.id_in_group: False}

            real_participants = [p for p in others if not p.participant.is_dropout]
            response = [p.response2 for p in real_participants]
            if all(response):
                contribution = np.round(np.mean(
                    [p.contribution for p in real_participants]
                ))

            else:
                logger.debug('Wait for all players to play before bots response')
                return {player.id_in_group: False}

            other_player.contribution = contribution
            other_player.RT2 = 0
            other_player.response2 = True
            logger.debug(
                f'Participant {other_player.participant.id_in_session} dropped out.'
                f' Bot contribution={contribution}')
            player.group.end_round()
            return {player.id_in_group: True}


class Results(Page):
    pass


page_sequence = [Init, Instructions, Disclose, Contribute, Results]
