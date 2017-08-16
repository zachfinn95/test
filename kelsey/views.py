from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from .forms import ConsentForm
from .models import Question, Player
from django.forms.models import inlineformset_factory
from django.views.generic import UpdateView
from django.forms import ModelForm

class MyPage(Page):
    ...
    # timeout_seconds = 60


def vars_for_all_templates(self):
    p_1 = int(round(1 - Constants.p, 1)*100)
    p = int(round(Constants.p, 1)*100)
    if self.round_number <= Constants.first_half:
        part_round_number = self.round_number
    else:
        part_round_number = self.round_number - Constants.first_half
    part_number = int(self.round_number > Constants.first_half) + 1
    max_rounds = Constants.first_half if \
        self.round_number <= Constants.first_half \
        else Constants.second_half - 1
    return {'p_1': p_1,
            'p': p,
            'part_round_number': part_round_number,
            'part_number': part_number,
            'max_rounds': max_rounds, }


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
                dict_to_return['show_final_investment_block'] = True
            if self.player.treatment == 'T1':
                dict_to_return['modal_shown'] = False
            return dict_to_return




# INSTRUCTIONS AND QS BLOCK
class InstrPage(MyPage):
    def is_displayed(self):
        return self.extra_displayed and (self.round_number == 1 or
                                         self.round_number ==
                                         Constants.second_half)

    def extra_displayed(self):
        return True


class FirstRoundPage(MyPage):
    def is_displayed(self):
        return self.round_number == 1


class Consent(FirstRoundPage):
    form_model = models.Player
    form_fields = ['consent']

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

class Separ(InstrPage):
    ...

# QuestionFormSet = modelformset_factory(Question, fields=('verbose', 'treatment'), extra=0)

class SponsorshipForm(ModelForm):
    class Meta:
        model = Question
        fields=('verbose', 'treatment')
    def is_valid(self):
        print("TRRRRR")
        return super(SponsorshipForm, self).is_valid()  


QuestionFormSet = inlineformset_factory(parent_model=Player,
                                        model=Question,
                                        form=SponsorshipForm, extra=10,
                                        fields=('verbose', 'treatment'),)

from django.db import transaction
from django.views.generic.edit import FormView
class Q( InstrPage, FormView):
    model = Question
    form_class = SponsorshipForm
    def post(self):
        print('SUKA')
        request = self.request
        self.object = self.get_object()
        post_data = request.POST
        print('SSSS$$$$', post_data)
        form = self.get_form(
            data=post_data, files=request.FILES, instance=self.object)
        self.form = form
        if self.form.is_valid():
            print(self.form.cleaned_data)
        return super(Q, self).post()
    def get(self):
        print('SUKAGET')
        return super(Q, self).get()
    def get_context_data(self, **kwargs):
        data = super(Q, self).get_context_data(**kwargs)
        print(data)
        qs = models.Question.objects.filter(player__exact=self.player)
        qs_formset = QuestionFormSet(queryset=qs)
        if self.request.POST:
            data['sponsorships'] = qs_formset(self.request.POST)
            print('#####::: ', data['sponsorships'])
        else:
            data['sponsorships'] = qs_formset
        return data
    def form_valid(self, form):
        print("SSSSUKA")
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        return super(Q, self).form_valid(form)
    def form_valid(self, form):
        print("SSSSUKA")
    #     context = self.get_context_data()
    #     sponsorships = context['sponsorships']
    #     with transaction.commit_on_success():
    #         # form.instance.created_by = self.request.user
    #         # form.instance.updated_by = self.request.user
    #         self.object = form.save()
    #     if sponsorships.is_valid():
    #         sponsorships.instance = self.object
    #         sponsorships.save()


    # def vars_for_template(self):
    #     # get decisions for this player
    #     qs = models.Question.objects.filter(player__exact=self.player)
    #     for q in qs:
    #         print(q.verbose)
    #     # assert len(decision_qs) == Constants.num_decisions_per_round
    #
    #     qs_formset = QuestionFormSet(queryset=qs)
    #
    #     return {
    #         'qs_formset': qs_formset,
    #         # 'decision_values_and_forms': zip([dec.value for dec in qs], qs_formset.forms),
    #     }
    # def post(self, request, *args, **kwargs):
    #     # form = self.form_class(request.POST)
    #     # if form.is_valid():
    #     #     print("PIZDA")
    #
    #     return super(Q, self).post(request, *args, **kwargs)

class QResults(InstrPage):
    ...

    def vars_for_template(self):
        qs = models.Question.objects.filter(player__exact=self.player)
        qs = [q.verbose for q in qs]
        return{'qs': qs}
    #     fields_to_get = [i['qname'] for i in Constants.questions
    #                      if i['treatment'] == self.player.treatment]
    #     results = [getattr(self.player, f) for f in fields_to_get]
    #     qtexts = [i['verbose'] for i in Constants.questions
    #                      if i['treatment'] == self.player.treatment]
    #     qsolutions = [i['correct'] for i in Constants.questions
    #                      if i['treatment'] == self.player.treatment]
    #     is_correct = [True if i[0] == i[1] else False for i in zip(results, qsolutions)]
    #     data = zip(qtexts, results,  qsolutions, is_correct)
    #     return {'data': data}


# END OF INSTRUCTIONS AND QS BLOCK

page_sequence = [
    # Consent,
    # Instr1,
    # Instr2,
    # Instr3,
    # Example,
    Q,
    QResults,
    # Separ,
    # InitialInvestment,
    # FinalInvestment,
    # Results
]
