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
from settings import export_style


class Constants(BaseConstants):
    name_in_url = 'step1'
    players_per_group = 2
    num_rounds = 14
    multiplier_bad = .8
    multiplier_good = 1.2
    endowment = 10


class Subsession(BaseSubsession):
    is_grouped_by_disclosure = models.BooleanField(default=False)

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

        self.session.group1 = np.ones(n_participant//2)*-1
        self.session.group2 = np.ones(n_participant//2)*-1

        for i, p in enumerate(self.get_players()):
            # print(p.participant.id_in_session)
            p.participant.idx = i
            assert len(multipliers) > i
            p.participant.multiplier = multipliers[p.participant.idx]

            # init data fields to use in next app
            p.participant.contribution = np.ones(Constants.num_rounds)*-1
            p.participant.disclose = np.ones(Constants.num_rounds)*-1
            # p.participant.opp_multiplier = np.zeros(Constants.num_rounds)
            p.participant.opp_id = np.ones(Constants.num_rounds)*-1

            p.participant.is_dropout = self.session.config.get('single_player') \
                                       and (p.participant.id_in_session != 1)

            p.participant.time_at_last_response = np.NaN

            p.participant.total = 0

    def creating_session(self):
        """
        match according to deterministic good/bad, good/good, bad/bad
        """
        if self.round_number == 1:
            self.init()

        if self.session.num_participants % 3 == 0:
            self.deterministic_matching()

    def deterministic_matching(self):
        logger.debug(
            f'Round {self.round_number}: '
            'Set matching pairs with a fixed nb of GG, GB, BB.')

        n_players = self.session.num_participants
        types = {
            Constants.multiplier_bad: [],
            Constants.multiplier_good: []
        }

        for p in self.get_players():
            types[p.participant.multiplier] \
                .append(p.participant.id_in_session)

        np.random.shuffle(types[Constants.multiplier_good])
        np.random.shuffle(types[Constants.multiplier_bad])

        n_row = n_players // Constants.players_per_group
        n_group_per_matching = n_row // 3
        multipliers = [
            (Constants.multiplier_good, Constants.multiplier_bad),
            (Constants.multiplier_good, Constants.multiplier_good),
            (Constants.multiplier_bad, Constants.multiplier_bad)
        ]

        matrix = np.zeros((n_row, Constants.players_per_group), dtype=int)
        count = 0
        for m1, m2 in multipliers:
            for _ in range(n_group_per_matching):
                matrix[count, :] = [types[m1].pop(), types[m2].pop()]
                count += 1
        assert count == n_row
        self.set_group_matrix(matrix)

    def group_by_disclosure(self):
        if not self.is_grouped_by_disclosure:

            if all(self.session.group1 == -1):
                self.create_groups()

            logger.debug(
                    f'Round {self.round_number}: '
                    'Match groups according to disclosure rate')

            group1 = self.session.group1.copy()
            group2 = self.session.group2.copy()

            np.random.shuffle(group1)
            np.random.shuffle(group2)

            assert len(group1) == len(group2)

            group1 = np.reshape(group1, [len(group1) // 2, 2])
            group2 = np.reshape(group2, [len(group2) // 2, 2])

            matrix = np.concatenate((group1, group2), axis=0)

            self.set_group_matrix(matrix)

            self.is_grouped_by_disclosure = True

    def create_groups(self):
        logger.debug(
            f'Round {self.round_number}: '
            'Create groups according to disclosure rate')

        data = np.zeros(self.session.num_participants)
        players = self.get_players()

        for p in players:
            cond = p.participant.disclose != -1
            data[p.participant.id_in_session - 1] = np.mean(p.participant.disclose[cond])

        idx_order = np.argsort(data) + 1
        length = len(idx_order)
        group1 = idx_order[0:length // 2]
        group2 = idx_order[length // 2:]

        for p in players:
            p.participant.disclosure_group = \
                1 if p.participant.id_in_session in group1 else 2

        self.session.group1 = group1.copy()
        self.session.group2 = group2.copy()


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

        if not self.response:
            logger.debug(f'Round {self.round_number}/ Group {self.id_in_subsession}:'
                         f' Setting payoffs and saving data.')
            self.set_payoffs()
            self.record_round_data()
            self.response = True

    def set_payoffs(self):
        players = self.get_players()
        contributions = [p.contribution * p.participant.multiplier for p in players]
        self.total_contribution = sum(contributions)
        self.individual_share = np.round(self.total_contribution / Constants.players_per_group, 2)
        for p in players:
            p.payoff = np.round(Constants.endowment - p.contribution + self.individual_share, 2)
            p.reward = np.round(Constants.endowment - p.contribution + self.individual_share, 2)
            p.participant.total += p.reward
            p.participant.total = np.round(p.participant.total, 2)
            p.total = p.participant.total

            if self.round_number == self.session.config.get('training_round_number'):
                p.participant.total = 0

    def record_round_data(self):
        players = self.get_players()
        id_of_opp = {1: 2, 2: 1}

        for p in players:
            p.participant.disclose[self.round_number - 1] = p.disclose
            p.participant.contribution[self.round_number - 1] = p.contribution
            opp = self.get_player_by_id(id_of_opp[p.id_in_group])
            # p.participant.opp_multiplier[self.round_number-1] = opp.multiplier
            p.participant.opp_id[self.round_number - 1] = opp.participant.idx


class Player(BasePlayer):
    contribution = models.IntegerField(default=-1)
    disclose = models.IntegerField(default=-1)
    rt1 = models.IntegerField(default=-1)
    rt2 = models.IntegerField(default=-1)
    response1 = models.BooleanField(default=False)
    response2 = models.BooleanField(default=False)
    reward = models.FloatField(default=-1)
    time_instructions = models.FloatField(default=-1)
    total = models.FloatField(default=0)

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
    if export_style == 'round':
        # header row
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
            'p1.total',
            'p1.disclosure_group',
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
            'p2.total',
            'p2.disclosure_group',
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
                p1.total,
                p1.participant.disclosure_group,
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
                p2.total,
                p2.participant.disclosure_group,
                group.round_number,
                group.individual_share,
                group.total_contribution,
                group.id
            ]

    else:
        # header row
        yield [
            'session',
            'is_bot',
            'prolific_id',
            'id_in_session',
            'id_in_group',
            'multiplier',
            'disclose',
            'contribution',
            'rt1',
            'rt2',
            'payoff',
            'total',
            'round_number',
            'individual_share',
            'total_contribution',
            'group_id',
            'disclosure_group'
        ]
        for p in players:
            group = p.group
            yield [
                p.session.code,
                p.participant.is_dropout,
                p.participant.label,
                p.participant.id_in_session,
                p.id_in_group,
                p.participant.multiplier,
                p.disclose,
                p.contribution,
                p.rt1,
                p.rt2,
                p.reward,
                p.total,
                group.round_number,
                group.individual_share,
                group.total_contribution,
                group.id,
                p.participant.disclosure_group
            ]
