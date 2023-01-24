from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'title', 'type':'text', 'placeholder':'Titre'}))
    body = forms.CharField(max_length=2048, help_text='', required=True, widget=forms.Textarea(attrs={'class':'form-control', 'id':'description', 'style':'height: 10rem', 'placeholder':'Description'}))
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'form-control', 'id':'picture', 'type':'file'}))

    
    class Meta:
        model = Ticket
        fields = ['title', 'body', 'picture']


class ReviewForm(forms.ModelForm):
    headline = forms.CharField(max_length=128, help_text='', required=True, widget=forms.TextInput(attrs={'class':'form-control', 'id':'title', 'type':'text', 'placeholder':'Titre'}))
    body = forms.CharField(max_length=2048, help_text='', required=True, widget=forms.Textarea(attrs={'class':'form-control', 'id':'description', 'style':'height: 10rem', 'placeholder':'Description'}))
    rating = forms.ChoiceField(label='Note', initial=0, choices=((0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")), widget=forms.RadioSelect(attrs={'class':'form-check-input', 'id':'rating'}))
    
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']