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


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # a1 = models.IntegerField(
    #     label="For me to install and use the covid tracing app on my phone for the next three months is..."
    # labels_importance = [1, 2, 3, 4, 5]
    # labels_efficiency = [1, 2, 3, 4, 5]
    # labels_harmful = [1, 2, 3, 4, 5]
    # labels_necessity = [1, 2, 3, 4, 5]
    # labels_usage = [1, 2, 3, 4, 5]
    # labels_difficulty = [1, 2, 3, 4, 5])
    labels_agreement = (
        'Strongly disagree',
        'Disagree',
        'Neither agree or disagree',
        'Agree',
        'Strongly agree'
    )

    labels_likelihood = (
        'Extremely unlikely',
        'unlikely',
        'Neutral',
        'likely',
        'Extremely likely'
    )

    labels_importance = (
        'Very Unimportant',
        'Somewhat Unimportant',
        'Somewhat important',
        'Important',
        'Very Important'
    )

    labels_confidence = (
        'Not at all confident',
        'Not really confident',
        'Undecided',
        'Somewhat confident',
        'Very much confident'
    )

    labels_efficiency = (
        'Totally inefficient',
        'Inefficient',
        'Undecided'
        'Efficient',
        'Totally efficient'
    )

    labels_harmful = (
        'Extremely harmful',
        'Harmful',
        'Undecided',
        'Beneficial',
        'Extremely beneficial'
    )

    labels_necessity = (
        'Extremely unnecesary',
        'Unnecessary',
        'Undecided',
        'Necessary',
        'Extremely necessary'
    )

    labels_usage = (
        'Totally useless',
        'Useless',
        'Undecided',
        'Useful',
        'Totally useful'
    )

    labels_difficulty = (
        'Extremely difficult',
        'Difficult',
        'Undecided',
        'Easy',
        'Extremely easy'
    )

    a2 = models.IntegerField(
        label="Most people who are important to me approve my installation"
              " and usage of the covid tracing app on my phone for the next three months.",
        choices=enumerate(labels_agreement), widget=widgets.RadioSelect
    )
    # a3 = models.IntegerField(
    #     label="It is expected of me that I install and use the covid tracing app on my phone for the next three months."
    # labels_likelihood = [1, 2, 3, 4, 5])
    # a4 = models.IntegerField(
    #     label="The people in my life whose opinions I value would think that I should install and use the app on my phone for the next three months."
    # labels_agreement = [1, 2, 3, 4, 5])
    # a5 = models.IntegerField(
    #     label="Most people that are important to me install and use the Covid tracing app on their phone for the next three months."
    # labels_agreement = [1, 2, 3, 4, 5])
    # a6 = models.IntegerField(
    #     label="Most people like me install and use the covid tracing app on my phone for the next three months."
    # labels_likelihood = [1, 2, 3, 4, 5])
    # a7 = models.IntegerField(
    #     label="The people in my life whose opinions I value install and use the covid a tracing app on their phone for the next three months."
    # labels_agreement = [1, 2, 3, 4, 5])
    # a8 = models.IntegerField(
    #     label="I am confident that I know how to install and use the covid tracing app on my phone for the next three months."
    # labels_confidence = [1, 2, 3, 4, 5])
    # a9 = models.IntegerField(
    #     label="If I wanted I could install and use the covid tracing app on my phone for the next three months."
    # labels_agreement = [1, 2, 3, 4, 5])
    # a10 = models.IntergerField(
    #     label="It is mostly up to me whether I install and use the Covid tracing app on my phone or not."
    # labels_agreement = [1, 2, 3, 4, 5])
    # a11 = models.IntegerField(
    #     label="I intend on installing and using the covid tracing app on my phone for the next three months."
    # labels_likelihood = [1, 2, 3, 4, 5])
    # a12 = models.InterField(
    #     label="I will plan to install and use the covid tracing app on my phone for the next three months."
    # labels_agreement = [1, 2, 3, 4, 5])
    # a13 = models.InterField(
    #     label="In the past three months, I installed and used the covid tracing app on my phone."
    # labels_agreement = [1, 2, 3, 4, 5])
