from django.contrib.auth.forms import forms
from .models import Client
from django.forms.widgets import NumberInput

class ClientForm(forms.ModelForm):
    genderChoice = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('custom', 'Custom'),
    ]
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=genderChoice)
    Date_Of_Birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = Client
        fields = [
            'first_name', 'last_name', 'email', 'password', 'gender', 'Date_Of_Birth']