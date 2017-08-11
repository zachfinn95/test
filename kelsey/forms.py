from django import forms
from . import models


class ConsentForm(forms.Form):
    def __init__(self, instance, view, *args, **kwargs):
        super(ConsentForm, self).__init__(*args, **kwargs)
    # class Meta:
    #     model = models.Player
    #     fields = ['consent']
    #     widgets = {
    #         'consent': forms.CheckboxInput(required=True),
    #     }

    consent = forms.BooleanField(required = True)
    # your other form fields
