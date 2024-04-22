from django import forms
from .models import Tools, Jobs, Service
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tools
        fields = ['name', 'model', 'quantity', 'accessories']
        labels = {
            'name': 'Nazwa',
            'model': 'Model',
            'quantity': 'Ilość',
            'accessories': 'Akcesoria'
        }
        widgets = {
            'quantity': forms.TextInput(attrs={'type': 'text'}),
        }

class BuyNewToolForm(forms.Form):
    tool_id = forms.IntegerField(widget=forms.HiddenInput())

class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['job_name', 'address']
        labels = {
            'job_name': 'Nazwa zlecenia',
            'address': 'Adres',
        }

class AddToolToJobForm(forms.Form):
    job = forms.ModelChoiceField(queryset=Jobs.objects.all(), label='Zlecenie')
    tool = forms.ModelChoiceField(queryset=Tools.objects.filter(quantity__gt=0), label='Narzędzie')


class AddToolToServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['tool', 'fault_description', 'expected_pickup_date']
        widgets = {
            'tool': forms.Select(attrs={'class': 'form-control'}),
            'fault_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40}),
            'expected_pickup_date': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'tool': 'Narzędzie',
            'fault_description': 'Opis usterki',
            'expected_pickup_date': 'Data odbioru',
        }

class TakeFromServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = []

    service_id = forms.IntegerField(widget=forms.HiddenInput())

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa użytkownika", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

class AddNewUser(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')

    class Meta:
        model = User
        fields = ('username', 'email')

        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'email',

        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ten email jest już zajęty.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

