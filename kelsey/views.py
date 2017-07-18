from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class InitialInvestment(Page):
    form_model = models.Player
    form_fields = ['first_decision']

class FinalInvestment(Page):
    pass


class Results(Page):
    pass


page_sequence = [
    InitialInvestment,
    FinalInvestment,
    Results
]
