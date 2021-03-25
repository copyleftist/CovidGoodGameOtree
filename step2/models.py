from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import numpy as np
from utils.debug import logger


class Constants(BaseConstants):
    name_in_url = 'step2'
    players_per_group = 2
    num_rounds = 3
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = c(10)


class Subsession(BaseSubsession):
    def init(self):
        """
        matching depending on results of step 1
        :return:
        """

        # ------------------------------------------------------------------ "
        # Compute social efficiency factor for each participant
        # ------------------------------------------------------------------ "
        n_participant = self.session.num_participants
        n_trial = Constants.num_rounds

        contribution = np.zeros((n_participant, n_trial))
        disclose = np.zeros((n_participant, n_trial))
        matching = np.zeros((n_participant, n_trial))
        multiplier = np.zeros((n_participant, n_trial))

        for p in self.get_players():
            n_trial = len(p.participant.contribution)
            pid = p.participant.id_in_session - 1
            for t in range(n_trial):
                contribution[pid, t] = p.participant.contribution[t]
                disclose[pid, t] = p.participant.disclose[t]
                matching[pid, t] = p.participant.opp_id[t] - 1
                multiplier[pid, t] = p.participant.multiplier

        social_efficiency = np.zeros(n_participant)
        for p in self.get_players():

            # temp array
            data = []
            n_trial = len(p.participant.contribution)
            pid = p.participant.id_in_session - 1

            for t in range(n_trial):

                opp_id = int(matching[pid, t])
                c1 = contribution[pid, t]
                c2 = contribution[opp_id, t]

                if p.participant.multiplier == Constants.multiplier_bad:
                    if multiplier[opp_id, t] == Constants.multiplier_good:
                        data.append(c1 > c2)
                else:
                    if multiplier[opp_id, t] == Constants.multiplier_bad:
                        data.append(c1 < c2)

            social_efficiency[pid] = np.mean(data)
            logger.debug(f'Participant {pid}')
            logger.debug(f'Social efficiency = {social_efficiency[pid]}')
        # ------------------------------------------------------------------ "


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def init_round(self):
        """
        this method is called at the beginning of each round
        :return:
        """
        for p in self.get_players():
            # set player multiplier in order to add it as column in data tables
            p.multiplier = p.participant.multiplier

    def end_round(self):
        self.set_payoffs()
        self.record_round_data()

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution*p.participant.multiplier for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution / Constants.players_per_group
        for p in players:
            p.payoff = Constants.endowment - p.contribution + self.individual_share

    def record_round_data(self):
        players = self.get_players()
        for p in players:
            p.participant.disclose[self.round_number-1] = p.disclose
            p.participant.contribution[self.round_number-1] = p.contribution


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you contribute?"
    )
    disclose = models.BooleanField(label="Do you want to reveal your multiplier to the other player?")
    multiplier = models.FloatField()

    def see_opponent_type(self):
        for p in self.get_others_in_group():
            return p.participant.multiplier if p.disclose else None
