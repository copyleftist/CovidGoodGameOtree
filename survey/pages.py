from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Section1(Page):
    form_model = 'player'
    form_fields = ['a2']#['a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','a12','a13']

class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class CognitiveReflectionTest(Page):
    form_model = 'player'
    form_fields = ['crt_bat', 'crt_widget', 'crt_lake']


page_sequence = [Section1]
