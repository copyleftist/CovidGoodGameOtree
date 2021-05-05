from otree.api import Currency as c, currency_range
from step1._builtin import Page, WaitPage
from .models import Constants
import numpy as np

from utils.debug import logger


SECOND = 1000
DROPOUT_TIME = 15 * SECOND
INSTRUCTIONS_TIME = 2 * SECOND

# ------------------------------------------------------------------------------------------------------------------- #
# Pages
# ------------------------------------------------------------------------------------------------------------------- #


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
            assert type(data['disclose']) == int
            assert type(data['RT']) == int
            player.set_disclose(
                disclose=int(data['disclose']),
                rt1=int(data['RT'])
            )

        other_player = player.get_others_in_group()[0]
        too_long = int(data['time']) > DROPOUT_TIME

        if other_player.response1:
            # if _everybody_played_disclose(player):
            #     _check_for_last_bots_disclose(player)

            return {player.id_in_group: True}

        if too_long or other_player.participant.is_dropout:
            other_player.participant.is_dropout = True
            if not _everybody_played_disclose(player):
                logger.debug('Wait for all players to play before bots response')
                return {player.id_in_group: False}

            disclose = _get_participants_disclose(player)
            assert type(disclose) == int
            other_player.set_disclose(disclose=disclose)
            logger.debug(
                f'Participant {other_player.participant.id_in_session} dropped out.'
                f' Bot disclose={disclose}')
            # _check_for_last_bots_disclose(player)
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
            player.set_contribution(
                contribution=int(data['contribution']),
                rt2=int(data['RT'])
            )

        other_player = player.get_others_in_group()[0]
        too_long = int(data['time']) > DROPOUT_TIME

        if other_player.response2:
            # if _everybody_played_contrib(player):
            #     _check_for_last_bots_contrib(player)

            player.group.end_round()
            return {player.id_in_group: True}

        if too_long or other_player.participant.is_dropout:
            other_player.participant.is_dropout = True
            if not _everybody_played_contrib(player):
                logger.debug('Wait for all players to play before bots response')
                return {player.id_in_group: False}

            contribution = _get_participants_contrib(player)
            other_player.set_contribution(contribution)
            logger.debug(
                f'Participant {other_player.participant.id_in_session} dropped out.'
                f' Bot contribution={contribution}')
            # _check_for_last_bots_contrib(player)
            player.group.end_round()
            return {player.id_in_group: True}


class Results(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'step1/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()


page_sequence = [Init, Instructions, Disclose, Contribute, Results]

# ------------------------------------------------------------------------------------------------------------------- #
# Side Functions
# ------------------------------------------------------------------------------------------------------------------- #


def _everybody_played_disclose(player):
    players = _get_all_players(player)
    real_participants = [p for p in players if not p.participant.is_dropout]
    response = [p.response1 for p in real_participants]
    return all(response)


def _everybody_played_contrib(player):
    players = _get_all_players(player)
    real_participants = [p for p in players if not p.participant.is_dropout]
    response = [p.response2 for p in real_participants]
    return all(response)


def _get_all_players(player):
    return [player, ] + player.get_others_in_subsession()


def _get_participants_contrib(player):
    contribution = np.round(np.mean(
        [p.contribution for p in _get_all_players(player) if not p.participant.is_dropout]
    ))
    return contribution


def _get_participants_disclose(player):
    p_disclose = np.mean(
        [p.disclose for p in _get_all_players(player) if not p.participant.is_dropout]
    )
    return int(np.random.choice(
            [0, 1], p=[1-p_disclose, p_disclose]))


def _get_groups(player):
    groups = []

    for p in player.get_others_in_subsession():
        if p.group not in groups:
            groups.append(p.group)
    return groups


def _check_for_last_bots_disclose(player):
    groups = _get_groups(player)
    for group in groups:

        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)

        if p1.participant.is_dropout and p2.participant.is_dropout:

            if not p1.response1:
                disclose = _get_participants_disclose(player)
                p1.set_disclose(disclose, 0)

            if not p2.response1:
                disclose = _get_participants_disclose(player)
                p2.set_disclose(disclose, 0)


def _check_for_last_bots_contrib(player):
    groups = _get_groups(player)
    for group in groups:

        p1 = group.get_player_by_id(1)
        p2 = group.get_player_by_id(2)

        if p1.participant.is_dropout and p2.participant.is_dropout:

            contribution = _get_participants_contrib(player)

            if not p1.response2:
                p1.set_contribution(contribution, 0)

            if not p2.response2:
                p2.set_contribution(contribution, 0)

            p1.group.end_round()
