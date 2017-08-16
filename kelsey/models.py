from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from math import ceil
from itertools import product
import csv
from collections import OrderedDict
from django import forms as djforms
author = 'Philipp Chapkovski, UZH'

doc = """
Kelsey-Oliva lottery game
"""


class Constants(BaseConstants):
    name_in_url = 'kelsey'
    players_per_group = None
    num_rounds = 18
    # till what round we play T0 and then change to whatever treatment
    # we have?::
    first_half = 9
    second_half = first_half + 1
    assert first_half <= num_rounds, "SOMETHING WRONG WITH NUMBER OF ROUNDS!"
    p = 0.3
    initial_cost = 9
    final_cost = 15
    first_decision_labels = {
    'T0': """Do you want to pay an initial investment cost of ${}  with the final
    investment cost determined based on what value payoff
    is drawn?""".format(initial_cost),
    'T1': """Do you want to pay an initial investment cost of ${} to
    take this contract?""".format(initial_cost),
    'T2': """Do you want to pay an initial investment cost of ${} and a final investment
     cost of ${} to release the randomly determined payoff?""".format(initial_cost, final_cost),
    }
    low_payoff_set = [0, 6, 12]
    high_payoff_set = [24, 36, 54]
    payoffs_sets = list(product(low_payoff_set, high_payoff_set))
    # values for control questions:
    q_parameters = {'initial_cost': 9,
                    'final_cost': 15,
                    'high_payoff': 40,
                    'low_payoff': 8,
                    'PT0ExampleHigh': 16,
                    'PT0ExampleLow': -16,
                    }
    with open('kelsey/qs_to_add.csv') as f:
        questions = list(csv.DictReader(f))
    for q in questions:
        q['verbose'] = q['verbose'].format(
         initial=q_parameters['initial_cost'],
         final=q_parameters['final_cost'],
         hpayoff=q_parameters['high_payoff'],
         lpayoff=q_parameters['low_payoff'],
        )
    # a = dict(questions)
        # questions = OrderedDict(sorted(questions.items(), key=lambda item: item['number']))

def weighted_choice(a, b):
    assert 0 <= Constants.p <= 1, 'SOMETHING WRONG WITH PROBABILITIES, DUDE'
    selector = random.random()
    if selector <= Constants.p:
        return a
    return b
class Subsession(BaseSubsession):
    def before_session_starts(self):


        first_half = self.session.config.get('first_half', 'T0')
        second_half = self.session.config.get('second_half', 'T0')
        for p in self.get_players():
            curpayoffset = (Constants.payoffs_sets.copy())
            random.shuffle(curpayoffset)
            p.participant.vars.setdefault('payoffsets', curpayoffset)
            i = p.round_number % Constants.first_half - 1
            p.low_payoff = p.participant.vars['payoffsets'][i][0]
            p.high_payoff = p.participant.vars['payoffsets'][i][1]
            p.investment_payoff = weighted_choice(p.low_payoff, p.high_payoff)
            if p.round_number <= Constants.first_half:
                p.treatment = first_half
            else:
                p.treatment = second_half
        # print('######', len(Player.objects.filter(subsession=self)))
        # for p in self.get_players():
        #     p.treatment='yyyy'
        # import otree.db.idmap
        # # otree.db.idmap.save_objects()
        # otree.db.idmap.flush_cache()
        # Player.objects.filter(subsession=self).update(treatment='ыыыы')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(widget=djforms.CheckboxInput,
                                  initial=False
                                  )
    treatment = models.CharField()
    investment_payoff = models.IntegerField()
    low_payoff = models.IntegerField()
    high_payoff = models.IntegerField()
    first_decision = models.BooleanField()
    second_decision = models.BooleanField(
        verbose_name="""Do you want to pay the final
        investment cost of ${} to
         release this payoff?""".format(Constants.final_cost)
    )
    # set of control questions for each treatment

# filtered_dict = {k:v for (k,v) in d.items() if filter_string in k}
    #  END OF set of control questions for each treatment
    def set_payoffs(self):
        if self.treatment == 'T0':
            self.payoff = self.first_decision * \
                (-Constants.initial_cost +
                 max(self.investment_payoff - Constants.final_cost, 0))
        if self.treatment == 'T1':
            self.payoff = self.first_decision * \
                (-Constants.initial_cost +
                 (self.investment_payoff - Constants.final_cost) *
                    (self.second_decision or 0))
        if self.treatment == 'T2':
            self.payoff = self.first_decision * \
                (-Constants.initial_cost +
                 self.investment_payoff - Constants.final_cost)


for i in Constants.questions:
    Player.add_to_class(i['qname'],
                        models.CharField(verbose_name=i['verbose'],
                        widget=widgets.RadioSelectHorizontal(),
                        choices=[i['option1'],i['option2']]))
