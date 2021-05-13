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
from settings import SESSION_CONFIGS


class Constants(BaseConstants):
    name_in_url = 'step1'
    players_per_group = 2
    num_rounds = 60
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = 10


class Subsession(BaseSubsession):
    deterministic = models.BooleanField(default=False)

    def init(self):
        """
        this method is called only once
        :return:
        """
        logger.debug('Initialization of the first phase:'
                     ' attributing multipliers and participant labels.')
        n_participant = self.session.num_participants
        logger.debug(f'N participants = {n_participant}')
        if n_participant % 3 == 0:
            self.deterministic = True

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

            p.participant.is_dropout = self.session.config.get('single_player')\
                                       and (p.participant.id_in_session != 1)

            p.participant.time_at_last_response = np.NaN

    def creating_session(self):
        """
        match according to deterministic good/bad, good/good, bad/bad
        """
        if self.round_number == 1:
            self.init()

        if self.deterministic:
            logger.debug(
                f'Round {self.round_number}: '
                'Set matching pairs with a fixed nb of GG, GB, BB.')
            n_players = self.session.num_participants

            n_group = n_players/3

            types = {
                Constants.multiplier_bad: [],
                Constants.multiplier_good: []
            }

            for p in self.get_players():
                types[p.participant.multiplier]\
                    .append(p.participant.id_in_session)

            np.random.shuffle(types[Constants.multiplier_good])
            np.random.shuffle(types[Constants.multiplier_bad])

            n_row = n_players//Constants.players_per_group
            matrix = np.zeros((n_row, Constants.players_per_group), dtype=int)

            # begin = [0,
            #     round(n_row_col*ratio[0]),
            #     round(n_row_col*ratio[0]+n_row_col*ratio[1])
            # ]
            #
            # end = [round(n_row_col*i) for i in ratio]
            multipliers = [
                (Constants.multiplier_good, Constants.multiplier_bad),
                (Constants.multiplier_good, Constants.multiplier_good),
                (Constants.multiplier_bad, Constants.multiplier_bad)
            ]

            count = 0
            for i, (m1, m2) in enumerate(multipliers):
                for g in range(n_group):
                    matrix[count, :] = [types[m1].pop(), types[m2].pop()]
                    count += 1

            assert count == n_row

            # for i, j, k in zip(begin, end, multipliers):
            #     matrix[i:i+j, :] = [
            #         [types[k[0]].pop(), types[k[1]].pop()]
            #         for _ in range(j)
            #     ]

            self.set_group_matrix(matrix)


class Group(BaseGroup):
    total_contribution = models.FloatField(default=-1)
    individual_share = models.FloatField(default=-1)
    response = models.BooleanField(default=False)

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
        if not self.response:
            self.set_payoffs()
            self.record_round_data()
            self.response = True

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution*p.participant.multiplier for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = np.round(self.total_contribution / Constants.players_per_group, 2)
        for p in players:
            p.payoff = np.round(Constants.endowment - p.contribution + self.individual_share, 2)
            p.reward = np.round(Constants.endowment - p.contribution + self.individual_share, 2)

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
    contribution = models.IntegerField(default=-1)
    disclose = models.IntegerField(default=-1)
    rt1 = models.IntegerField(default=-1)
    rt2 = models.IntegerField(default=-1)
    response1 = models.BooleanField(default=False)
    response2 = models.BooleanField(default=False)
    reward = models.FloatField(default=-1)
    time_instructions = models.FloatField(default=-1)

    def see_opponent_type(self):
        for p in self.get_others_in_group():
            return p.participant.multiplier if p.disclose else None

    def set_disclose(self, disclose: int, rt1: int = None):
        self.disclose = int(disclose)
        if rt1 is not None:
            self.rt1 = rt1
        self.response1 = True

    def set_contribution(self, contribution: int, rt2: int = None):
        self.contribution = int(contribution)
        if rt2 is not None:
            self.rt2 = rt2
        self.response2 = True


def custom_export(players):
        #header row
        yield [
            'app',
            'session',
            'session_is_demo',
            'p1.is_bot',
            'p1.participant_code',
            'p1.prolific_id',
            'p1.id_in_session',
            'p1.id_in_group',
            'p1.multiplier',
            'p1.disclose',
            'p1.contribution',
            'p1.rt1',
            'p1.rt2',
            'p1.payoff',
            'p2.is_bot',
            'p2.participant_code',
            'p2.prolific_id',
            'p2.id_in_session',
            'p2.id_in_group',
            'p2.multiplier',
            'p2.disclose',
            'p2.contribution',
            'p2.rt1',
            'p2.rt2',
            'p2.payoff',
            'round_number',
            'individual_share',
            'total_contribution',
            'group_id'
        ]
        groups = []
        for p in players:
            # participant = p.participant
            # session = p.session
            if p.group not in groups:
                groups.append(p.group)
        for group in groups:
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            assert p1.round_number == p2.round_number
            assert p1.group.id == p2.group.id
            yield [
                p1.participant._current_app_name,
                p1.session.code,
                p1.session.is_demo,
                p1.participant.is_dropout,
                p1.participant.code,
                p1.participant.label,
                p1.participant.id_in_session,
                p1.id_in_group,
                p1.participant.multiplier,
                p1.disclose,
                p1.contribution,
                p1.rt1,
                p1.rt2,
                p1.reward,
                p2.participant.is_dropout,
                p2.participant.code,
                p2.participant.label,
                p2.participant.id_in_session,
                p2.id_in_group,
                p2.participant.multiplier,
                p2.disclose,
                p2.contribution,
                p2.rt1,
                p2.rt2,
                p2.reward,
                group.round_number,
                group.individual_share,
                group.total_contribution,
                group.id
            ]
