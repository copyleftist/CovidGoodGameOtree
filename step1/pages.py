from otree.api import Currency as c, currency_range
from step1._builtin import Page, WaitPage
from .models import Constants
import numpy as np
import time
from settings import pounds_per_point

from utils.debug import logger


SECOND = 1000
MINUTE = SECOND * 60
DROPOUT_TIME = 30 * SECOND
INSTRUCTIONS_TIME = 10 * MINUTE
RESULTS_TIME = 7.5 * SECOND


# ------------------------------------------------------------------------------------------------------------------- #
# Pages
# ------------------------------------------------------------------------------------------------------------------- #

class Sorting(WaitPage):
    template_name = 'step1/Wait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number >= Constants.num_rounds//2

    @staticmethod
    def after_all_players_arrive(subsession):
        subsession.group_by_disclosure()


class Init(WaitPage):
    template_name = 'step1/Wait.html'
    wait_for_all_groups = True

    def is_displayed(self):
        _set_as_connected(player=self.player)
        real_participants = [not p.participant.is_dropout
                             for p in _get_all_players(self.player)]
        return (self.round_number == 1) and (sum(real_participants) > 1)


class End(Page):

    def vars_for_template(self):
        total = self.player.participant.total
        pounds = np.round(total*pounds_per_point, 2)
        pences = np.round(pounds*100, 2)
        return {'total': total, 'pences': pences, 'pounds': pounds}

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        from .instructions import panels, titles
        if self.player.time_instructions == -1:
            self.player.time_instructions = time.time()
        limit = self.session.config.get('instructions_time') * SECOND
        return {'panels': panels, 'titles': titles, 'instructionsTime': limit}

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        time_since_opening = (time.time() - player.time_instructions) * SECOND
        limit = player.session.config.get('instructions_time') * SECOND
        if time_since_opening > limit:
            return {player.id_in_group: True}
        return False


class Disclose(Page):
    def get_template_name(self):
        if self.participant.is_dropout:
            return 'step1/Dropout.html'
        # if not dropout then execute the original method
        return super().get_template_name()

    def vars_for_template(self):
        from .html import wait, real
        _set_as_connected(self.player)
        training_round_number = self.session.config.get('training_round_number')
        return {
            'player_character': 'img/{}.gif'.format(self.player.participant.multiplier),
            'html': wait,
            'modalReal': real,
            'training': int(self.player.round_number <= training_round_number),
            'real': int(self.player.round_number == (training_round_number+1))
        }

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        players = _get_all_players(player)
        _check_for_disconnections(players)
        other_player = player.get_others_in_group()[0]

        if not player.response1:
            logger.debug(f'Participant {player.participant.id_in_session}'
                         ' saving disclosure response.')
            player.set_disclose(
                disclose=int(data['disclose']),
                rt1=int(data['RT'])
            )

        if other_player.response1:
            return {player.id_in_group: True}

        if other_player.participant.is_dropout:
            t = player.round_number
            if not _everybody_played_disclose(players, t-1):
                logger.debug('Wait for all players to play before bots response')
                return {player.id_in_group: False}

            disclose = _get_average_disclose(players, t-1)
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

        _set_as_connected(self.player)

        opp_character, opp_multiplier = [self.player.see_opponent_type(), ] * 2
        player_character, player_multiplier = [self.player.participant.multiplier, ] * 2

        if opp_multiplier is None:
            opp_multiplier = '...'

        if not self.player.disclose:
            player_multiplier = '...'
            player_character = None

        training_round_number = self.session.config.get('training_round_number')
        return {
            'player_character': 'img/{}.gif'.format(player_character),
            'opponent_character': 'img/{}.gif'.format(opp_character),
            'opp_color': '#5893f6' if opp_multiplier == Constants.multiplier_good else '#d4c84d',
            'opponent_multiplier': opp_multiplier,
            'player_multiplier': player_multiplier,
            'html': wait,
            'training': int(self.player.round_number <= training_round_number)
        }

    @staticmethod
    def live_method(player, data):
        _set_as_connected(player)
        players = _get_all_players(player)
        _check_for_disconnections(players)
        other_player = player.get_others_in_group()[0]

        if not player.response2:
            logger.debug(f'Participant {player.participant.id_in_session}'
                         ' saving contribution response.')
            player.set_contribution(
                contribution=int(data['contribution']),
                rt2=int(data['RT'])
            )

        if other_player.response2:
            player.group.end_round()
            return {player.id_in_group: True}

        if other_player.participant.is_dropout:
            t = player.round_number
            if not _everybody_played_contrib(players, t-1):
                logger.debug('Wait for all players to play before bots response')
                return {player.id_in_group: False}

            contribution = _get_average_contrib(players, t-1)
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

    def vars_for_template(self):
        player_multiplier = self.player.participant.multiplier

        opp = self.player.get_others_in_group()[0]
        opp_multiplier = opp.participant.multiplier
        opp_disclose = opp.disclose
        opp_contribution = opp.contribution
        opp_payoff = opp.payoff
        training_round_number = self.session.config.get('training_round_number')

        return {
            'player_character': 'img/{}.gif'.format(player_multiplier),
            'opp_character': 'img/{}.gif'.format(opp_multiplier),
            'player_multiplier': player_multiplier,
            'opp_multiplier': opp_multiplier,
            'opp_contribution': opp_contribution,
            'opp_left': Constants.endowment - opp_contribution,
            'player_left': Constants.endowment - self.player.contribution,
            'opp_payoff': opp_payoff,
            'player_color': '#5893f6' if player_multiplier == Constants.multiplier_good else '#d4c84d',
            'opp_color': '#5893f6' if opp_multiplier == Constants.multiplier_good else '#d4c84d',
            'disclose': opp_disclose,
            'resultsTime': self.session.config.get('results_time') * SECOND,
            'training': int(self.player.round_number <= training_round_number)

        }


page_sequence = [Init, Sorting, Instructions, Disclose, Contribute, Results, End]

# ------------------------------------------------------------------------------------------------------------------- #
# Side Functions
# ------------------------------------------------------------------------------------------------------------------- #


def _set_as_connected(player):
    player.participant.time_at_last_response = time.time()


def _check_for_disconnections(players):
    player = players[0]
    real_players = [p for p in players if not p.participant.is_dropout]
    limit = player.session.config.get('dropout_time')*SECOND
    for p in real_players:
        t = (time.time() - p.participant.time_at_last_response) * SECOND
        if t > limit:
            p.participant.is_dropout = True


def _everybody_played_disclose(players, t):
    t = (t==0) + t
    real_participants = [p.in_round(t) for p in players
                         if not p.participant.is_dropout]
    response = [p.response1 for p in real_participants]
    return all(response)


def _everybody_played_contrib(players, t):
    t = (t==0) + t
    real_participants = [p.in_round(t) for p in players
                         if not p.participant.is_dropout]
    response = [p.response2 for p in real_participants]
    return all(response)


def _get_all_players(player):
    return [player, ] + player.get_others_in_subsession()


def _get_average_contrib(players, t):
    if t == 0:
        contribution = np.round(np.mean(
            [p.contribution for p in players if not p.participant.is_dropout]
        ))
    else:
        contribution = []
        for p in players:
            if not p.participant.is_dropout:
                contribution.append(p.participant.contribution[t - 1])
        contribution = np.round(np.mean(contribution))
    return contribution


def _get_average_disclose(players, t):
    if t == 0:
        p_disclose = np.mean(
            [p.disclose for p in players if not p.participant.is_dropout]
        )
    else:
        disclose = []
        for p in players:
            if not p.participant.is_dropout:
                disclose.append(p.participant.disclose[t - 1])
        p_disclose = np.mean(disclose)
    return np.random.choice(
            [0, 1], p=[1-p_disclose, p_disclose])


# def _get_groups(player):
#     groups = []
#
#     for p in player.get_others_in_subsession():
#         if p.group not in groups:
#             groups.append(p.group)
#     return groups