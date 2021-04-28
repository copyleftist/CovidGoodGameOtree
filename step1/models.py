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
    num_rounds = 10
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = c(10)
    deterministic = False


class Subsession(BaseSubsession):
    def init(self):
        """
        this method is called only once
        :return:
        """
        logger.debug('Initialization of the first phase:'
                     ' attributing multipliers and participant labels.')
        n_participant = self.session.num_participants
        logger.debug(f'N participants = {n_participant}')

        # equal repartition of types
        multipliers = [Constants.multiplier_good, ] * (n_participant // 2) \
                    + [Constants.multiplier_bad, ] * (n_participant // 2)
        np.random.shuffle(multipliers)

        for p in self.get_players():
            # print(p.participant.id_in_session)
            p.participant.idx = p.participant.id_in_session - 1
            p.participant.multiplier = multipliers[p.participant.idx]

            # init data fields to use in next app
            p.participant.contribution = np.zeros(Constants.num_rounds)
            p.participant.disclose = np.zeros(Constants.num_rounds)
            # p.participant.opp_multiplier = np.zeros(Constants.num_rounds)
            p.participant.opp_id = np.zeros(Constants.num_rounds)

    def creating_session(self):
        """
        match according to deterministic good/bad, good/good, bad/bad
        """
        if self.round_number == 1:
            self.init()

        if Constants.deterministic:
            logger.debug(
                f'Round {self.round_number}: '
                'Set matching pairs with a fixed nb of GG, GB, BB.')
            n_players = self.session.num_participants

            ratio = [.33,  # GB
                     .33,  # GG
                     .33]  # BB

            types = {
                Constants.multiplier_bad: [],
                Constants.multiplier_good: []
            }

            for p in self.get_players():
                types[p.participant.multiplier]\
                    .append(p.participant.id_in_session)

            np.random.shuffle(types[Constants.multiplier_good])
            np.random.shuffle(types[Constants.multiplier_bad])

            n_row_col = n_players//Constants.players_per_group
            matrix = np.zeros((n_row_col, Constants.players_per_group), dtype=int)

            begin = [0,
                round(n_row_col*ratio[0]),
                round(n_row_col*ratio[0]+n_row_col*ratio[1])
            ]

            end = [round(n_row_col*i) for i in ratio]
            multipliers = [
                (Constants.multiplier_good, Constants.multiplier_bad),
                (Constants.multiplier_good, Constants.multiplier_good),
                (Constants.multiplier_bad, Constants.multiplier_bad)
            ]

            for i, j, k in zip(begin, end, multipliers):
                matrix[i:i+j, :] = [
                    [types[k[0]].pop(), types[k[1]].pop()]
                    for _ in range(j)
                ]

            self.set_group_matrix(matrix)


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def init_round(self):
        """
        this method is called at the beginning of each round
        :return:
        """
        pass

        # logger.debug(f'Round {self.round_number}: attributing multipliers to players.')
        # players = self.get_players()
        # for p in players:
        #     p.multiplier = p.participant.multiplier

    def end_round(self):
        """
        this method is called at the end of each round
        :return:
        """
        logger.debug(f'Round {self.round_number}/ Group {self.id_in_subsession}:'
                     f' Setting payoffs and saving data.')
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
        id_of_opp = {1: 2, 2: 1}
        for p in players:
            p.participant.disclose[self.round_number-1] = p.disclose
            p.participant.contribution[self.round_number-1] = p.contribution
            opp = self.get_player_by_id(id_of_opp[p.id_in_group])
            # p.participant.opp_multiplier[self.round_number-1] = opp.multiplier
            p.participant.opp_id[self.round_number-1] = opp.participant.idx


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0, max=Constants.endowment
    )
    disclose = models.BooleanField()
    multiplier = models.FloatField()
    RT = models.FloatField()

    def see_opponent_type(self):
        for p in self.get_others_in_group():
            return p.participant.multiplier if p.disclose else None

    def custom_export(self):
        # header row
        yield [
            'app',
            'session',
            'is_bot',
            'participant_code',
            'prolific_id',
            'id_in_session',
            'multiplier',
            'disclose',
            'contribution',
            'RT',
            'round_number',
            'id_in_group',
            'payoff',
            'individual_share',
            'total_contribution'
        ]
        for p in self.get_players():
            participant = p.participant
            session = p.session
            group = p.group
            yield [
                participant._is_bot,
                participant._current_app_name,
                session.code,
                participant.code,
                participant.label,
                participant.id_in_session,
                participant.multiplier,
                p.disclose,
                p.contribution,
                p.RT,
                p.round_number,
                p.id_in_group,
                p.payoff,
                group.individual_share,
                group.total_contribution,
            ]

