from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class InitialInvestment(Page):
    form_model = models.Player
    form_fields = ['first_decision']

class FinalInvestment(Page):
    form_model = models.Player
    form_fields = ['second_decision']
    def is_displayed(self):
        return self.player.treatment == 'T1'


class Results(Page):
    def is_displayed(self):
        self.player.set_payoffs()
        return True


page_sequence = [
    InitialInvestment,
    FinalInvestment,
    # WP,
    Results
]
