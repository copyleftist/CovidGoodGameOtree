# Don't change anything in this file.
<<<<<<< Updated upstream:public_covid/_builtin/__init__.py
from .. import models
=======
from step1 import models
>>>>>>> Stashed changes:step1/_builtin/__init__.py
import otree.api


class Page(otree.api.Page):
    subsession: models.Subsession
    group: models.Group
    player: models.Player


class WaitPage(otree.api.WaitPage):
    subsession: models.Subsession
    group: models.Group
    player: models.Player


class Bot(otree.api.Bot):
    subsession: models.Subsession
    group: models.Group
    player: models.Player
