from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

author = 'Philipp Chapkovski, UZH'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'kelsey'
    players_per_group = None
    num_rounds = 1
    p = 0.5
    payoffs = [2, 15]
    initial_cost = 3
    final_cost = 6
    first_decision_labels = {
    'T0': """Do you want to pay an initial inv. cost of ${}  with the final
    investment cost determined based on what value payoff is drawn? """.format(initial_cost),
    'T1': """Do you want to pay an initial inv. cost of ${} to take this contract?
          """.format(initial_cost),
    'T2': """Do you want to pay an initial inv. cost of ${} and a final inv cost of ${} to release the randomly determined payoff??
    """.format(initial_cost, final_cost),
    }

class Subsession(BaseSubsession):
    def before_session_starts(self):
        for p in self.get_players():
            p.investment_payoff = random.choice(Constants.payoffs)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    investment_payoff = models.IntegerField()
    first_decision = models.BooleanField()
    second_decision = models.BooleanField()
