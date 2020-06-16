from django import forms

from .models import Question

class QuestionForm(forms.Form):

    class Meta:
        ans = forms.ChoiceField()
        fields = ('ans')