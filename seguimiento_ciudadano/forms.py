from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError

class AuthenticateUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Nombre de usuario:', min_length=5, max_length=30, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Correo electrónico', widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Contraseña',
                                min_length=8, max_length=30,
                                widget=forms.PasswordInput(attrs={'class':'form-control', "autocomplete": "new-password"}),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Confirmar contraseña', min_length=8, max_length=30, widget=forms.PasswordInput(attrs={'class':'form-control', "autocomplete": "new-password"}))
    field_order = ['username','email','password1','password2']
    
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("El usuario ya existe")  
        return username
    def clean_email(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("correo electrónico ya en uso")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Las contraseñas no coinciden")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1'] 
        )  
        return user