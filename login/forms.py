from django import forms
 
class PersonForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)
class RequestsForm(forms.Form):
    title= forms.CharField(max_length=200)