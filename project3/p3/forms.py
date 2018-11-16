from django import forms
class person_forms(forms.Form):
    # id = forms.IntegerField()
    user_name = forms.CharField(label='user_name',max_length=30)
    pwd = forms.CharField(label='pwd',max_length=30)