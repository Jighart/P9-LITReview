from django import forms
from django.contrib.auth.models import User

                # <input class='form-control' id='username' type='text' placeholder='Nom d'utilisateur' data-sb-validations='required' />
                # <label for='username'>Nom d'utilisateur</label>

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='username', min_length=3, max_length=250, help_text='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'username', 'type':'text', 'placeholder':'Nom d\'utilisateur', 'data-sb-validations':'required'}))
    password = forms.CharField(label='password', min_length=8, max_length=250, help_text='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'password', 'type':'password', 'placeholder':'Mot de passe', 'data-sb-validations':'required'}))
    cpassword = forms.CharField(label='cpassword', min_length=8, max_length=250, help_text='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'cpassword', 'type':'password', 'placeholder':'Mot de passe', 'data-sb-validations':'required'}))

    class Meta:
        model = User
        fields = ('username',)