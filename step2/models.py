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
    name_in_url = 'step2'
    players_per_group = 2
    num_rounds = 1
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = c(10)


class Subsession(BaseSubsession):
    def matching(self):
        print('Matching')
        for p in self.get_players():
            print('Participant id: ', p.participant.id_in_session)
            print(p.participant.vars)


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution*p.multiplier for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = self.total_contribution / Constants.players_per_group
        for p in players:
            p.payoff = Constants.endowment - p.contribution + self.individual_share



class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment, label="How much will you contribute?"
    )
    disclose = models.BooleanField(label="Do you want to reveal your multiplier to the other player?")
    multiplier = models.FloatField()

    def see_opponent_type(self):
        for p in self.get_others_in_group():
            return p.multiplier if p.disclose else None
