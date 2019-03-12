from django import forms
from pgmanage.models import PGManager, PG, Room, UserProfile


class PGManagerForm(forms.ModelForm):
    class Meta:
        model=PGManager
        fields=("name", "gender", "cell", "email")#__all__



class PGManagerSearchForm(forms.Form):
	name = forms.CharField(max_length=60, required=False )
	gender = forms.ChoiceField(choices=PGManager.gender_choices, required=False)
	cell = forms.CharField(max_length=15, required=False)
	email = forms.EmailField(required=False)
	page = forms.IntegerField(required=False)

class UserProfileCreation(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= UserProfile
        fields=("username", "password", "email", "cell", "role")