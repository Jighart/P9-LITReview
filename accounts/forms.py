from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

                # <input class='form-control' id='username' type='text' placeholder='Nom d'utilisateur' data-sb-validations='required' />
                # <label for='username'>Nom d'utilisateur</label>

class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='', min_length=3, max_length=250, help_text='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'username', 'type':'text', 'placeholder':'Nom d\'utilisateur', 'data-sb-validations':'required'}))
    password1 = forms.CharField(label='', min_length=8, max_length=250, help_text='8 caractères minimum', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'password', 'type':'password', 'placeholder':'Mot de passe', 'data-sb-validations':'required'}))
    password2 = forms.CharField(label='', min_length=8, max_length=250, help_text='Confirmez le mot de passe', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'cpassword', 'type':'password', 'placeholder':'Mot de passe', 'data-sb-validations':'required'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class FollowForm(forms.Form):
    followed_user = forms.CharField(label=False,widget=forms.TextInput())