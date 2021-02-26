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


class Constants(BaseConstants):
    name_in_url = 'public_covid'
    players_per_group = 2
    num_rounds = 10
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = c(10)


class Subsession(BaseSubsession):
    def creating_session(self):
        n_players = len(self.get_players())

        #equal repartition of types
        multipliers = [Constants.multiplier_good, ] * (n_players//2)\
                      + [Constants.multiplier_bad, ] * (n_players//2)
        np.random.shuffle(multipliers)

        for id, p in enumerate(self.get_players()):
            p.multiplier = multipliers[id]
        for group in self.get_groups():
            group.treatment = np.random.choice(['central_authority_voluntary', 'central_authority_non_voluntary', 'bilateral_voluntary',  'bilateral_non_voluntary'])


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    treatment = models.CharField()

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution*p.multiplier for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution / Constants.players_per_group
        for p in players:
            p.payoff = Constants.endowment - p.contribution + self.individual_share

    def see_opponent_type(self):
        for p in self.get_players():
            p.see_opponent_type(self)


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you contribute?"
    )
    disclose = models.BooleanField(
        #choices=[
        #    [True, "Yes"]
        #    [False, "No"]],
        label="Do you want to reveal your multiplier?")

    multiplier = models.FloatField()

    authority_disclose = np.random.choice([True, False])

    def see_opponent_type(self, group):
        for p in self.get_others_in_group():
            if group.treatment == 'central_authority_voluntary':
                return p.multiplier if p.disclose and p.authority_disclose else None
            elif group.treatment == 'central_authority_non_voluntary':
                return p.multiplier if p.authority_disclose else None
            elif group.treatment == 'bilateral_voluntary':
                return p.multiplier if p.disclose else None
            else:
                return p.multiplier

            import logging
            logger = logging.getLogger("mylogger")
            logger.info(p.multiplier)


