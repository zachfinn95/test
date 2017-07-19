from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class MyPage(Page):
    timeout_seconds = 60


def vars_for_all_templates(self):
    p_1 = 1 - Constants.p
    return {'p_1': p_1}

def what_to_highlight(p):
    print('I AM IN!!')
    return ({
        'highlighted_high': p.investment_payoff == p.high_payoff,
        'highlighted_low': p.investment_payoff == p.low_payoff,
    })


class Part2(MyPage):
    def is_displayed(self):
        return self.round_number == Constants.first_half + 1


class InitialInvestment(MyPage):
    form_model = models.Player
    form_fields = ['first_decision']
    def vars_for_template(self):
        curlab = Constants.first_decision_labels[self.player.treatment]
        return {
            'first_decision_label': curlab,
        }

class FinalInvestment(MyPage):
    form_model = models.Player
    form_fields = ['second_decision']
    def is_displayed(self):
        return self.player.treatment == 'T1' and self.player.first_decision
    def vars_for_template(self):
        return what_to_highlight(self.player)


class Results(MyPage):
    def is_displayed(self):
        self.player.set_payoffs()
        return True
    def vars_for_template(self):
        if self.player.first_decision:
            return what_to_highlight(self.player)

page_sequence = [
    Part2,
    InitialInvestment,
    FinalInvestment,
    # WP,
    Results
]
