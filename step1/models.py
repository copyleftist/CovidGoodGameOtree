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
    name_in_url = 'step1'
    players_per_group = 2
    num_rounds = 3
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = c(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def init(self):
        """
        this method is called only once
        :return:
        """
        logger.debug(
            'Initialization: attributing multipliers, participant labels, treatment.')
        n_participant = self.session.num_participants

        # equal repartition of types
        multipliers = [Constants.multiplier_good, ] * (n_participant // 2) \
                    + [Constants.multiplier_bad, ] * (n_participant // 2)
        np.random.shuffle(multipliers)

        for p in self.get_players():
            # print(p.participant.id_in_session)
            p.participant.multiplier = multipliers[p.participant.id_in_session - 1]
            p.participant.label = f'ID{p.participant.id_in_session}'

            p.participant.treatment = self.session.config['treatment']

            # init data fields to use in next app
            p.participant.contribution = np.zeros(Constants.num_rounds)
            p.participant.disclose = np.zeros(Constants.num_rounds)

    def init_round(self):
        """
        this method is called at the beginning of each round
        :return:
        """
        for p in self.get_players():
            p.multiplier = p.participant.multiplier

    def end_round(self):
        self.set_payoffs()
        #self.record_round_data()

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
        if self.participant.treatment == 1:
            for p in self.get_others_in_group():
                return p.participant.multiplier if p.disclose else None
        elif self.participant.treatment == 2:
            for p in self.get_others_in_group():
                return p.participant.multiplier
        else:
            logger.debug('TO IMPLEMENT')
