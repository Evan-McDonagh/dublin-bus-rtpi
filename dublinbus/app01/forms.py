from django import forms
from django.forms import widgets
class leapForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=widgets.PasswordInput({ "class": "form-control"}))
    # remember_me = forms.MultipleChoiceField(widget=widgets.CheckboxInput)

class routeForm(forms.Form):
    route_id = forms.CharField()