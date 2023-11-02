from django import forms

class PostCreateForm(forms.Form):
  name = forms.CharField()
  apellido = forms.CharField()