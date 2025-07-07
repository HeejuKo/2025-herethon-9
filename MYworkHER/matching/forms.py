from django import forms
from .models import Matching


class MatchingForm(forms.ModelForm):
    class Meta:
        model = Matching
        fields = ['expert', 'date', 'time', 'notes']
