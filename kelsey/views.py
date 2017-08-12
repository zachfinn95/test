from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .forms import ConsentForm

class MyPage(Page):
    ...
    # timeout_seconds = 60


def vars_for_all_templates(self):
    p_1 = int(round(1 - Constants.p, 1)*100)
    p = int(round(Constants.p, 1)*100)
    return {'p_1': p_1,
            'p': p}


def what_to_highlight(p):

    return {
        'highlighted_high': p.investment_payoff == p.high_payoff,
        'highlighted_low': p.investment_payoff == p.low_payoff,
        'prob_realized': True,
        'modal_shown': True,
        }



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
            dict_to_return= what_to_highlight(self.player)
            if self.player.treatment == 'T2':
                dict_to_return['show_final_investment_block'] = True
            if (self.player.treatment == 'T0' and
                    self.player.investment_payoff >= Constants.final_cost):
                dict_to_return['show_final_investment_block'] = True
            if (self.player.treatment == 'T1' and
                    self.player.second_decision):
                dict_to_return['modal_shown'] = False
                dict_to_return['show_final_investment_block'] = True
            return dict_to_return




# INSTRUCTIONS AND QS BLOCK
class InstrPage(MyPage):
    def is_displayed(self):
        return self.extra_displayed and (self.round_number == 1 or
                                         self.round_number ==
                                         Constants.second_half)

    def extra_displayed(self):
        return True
class FirstRoundPage(InstrPage):
    def extra_displayed(self):
        return self.round_number == 1

from django.views.generic.edit import FormView
class Consent(FirstRoundPage):
    # form_class = ConsentForm
    form_model = models.Player
    form_fields = ['consent']
    # def get_form_class(self):
    #     # return
    #     return self.form_class

    def consent_error_message(self, value):
        if not value:
            return 'You must accept the consent form'
class Instr1(FirstRoundPage):
    ...


class Instr2(FirstRoundPage):
    ...


class Instr3(InstrPage):
    pass


class Instr4(InstrPage):
    pass


class Example(InstrPage):
    ...


class Q(InstrPage):
    form_model = models.Player
    def get_form_fields(self):
        return [i['qname'] for i in Constants.questions
                if i['treatment'] == self.player.treatment]

class QResults(InstrPage):

    def vars_for_template(self):
        fields_to_get = [i['qname'] for i in Constants.questions
                         if i['treatment'] == self.player.treatment]
        results = [getattr(self.player, f) for f in fields_to_get]
        qtexts = [i['verbose'] for i in Constants.questions
                         if i['treatment'] == self.player.treatment]
        qsolutions = [i['correct'] for i in Constants.questions
                         if i['treatment'] == self.player.treatment]
        is_correct = [True if i[0] == i[1] else False for i in zip(results, qsolutions)]
        data = zip(qtexts, results,  qsolutions, is_correct)
        return {'data': data}

class Final(FirstRoundPage):
    pass

# END OF INSTRUCTIONS AND QS BLOCK

page_sequence = [
    Consent,
    Instr1,
    Instr2,
    Instr3,
    Example,
    Q,
    QResults,
    InitialInvestment,
    FinalInvestment,
    Results
]
