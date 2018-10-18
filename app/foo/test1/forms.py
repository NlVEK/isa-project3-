from django import forms

class person_forms(forms.Form):
    # id = forms.IntegerField()
    first_name = forms.CharField(label='first_name',max_length=30)
    last_name = forms.CharField(label='last_name',max_length=30)


class thing_forms(forms.Form):
    info = forms.CharField(label='info', max_length=30)