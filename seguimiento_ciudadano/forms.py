from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from .models import Solicitudes, tiposolicitud, Seguimiento_solicitud

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
    


### ModelForm Hereda la info de los campos del modelo, y esto evita que los widgets sean declarados como en UserCreationForm y AuthenticationForm
### Pero a su ves, evita que tengan que ser declarados como tal, a menos que quieras hacer override de algunos datos, como labels o widgets(tipo de input)
### En cuyo caso, se declara como >[labels|widgets] = {'nombrecampo':'valorOverride'}<
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitudes
        fields = '__all__'
        exclude = ['request_id', 'activo', 'solicitud_datetime', 'updated_at', 'status', 'agency_responsible', 'country']
        # tipo_solicitud = forms.ModelChoiceField(queryset=tiposolicitud.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
        # descripcion = forms.CharField(label='Descripción del caso:', max_length=1500, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Ingresa una descripción detallada de tu consulta"}))
        # street_address = forms.CharField(label='Dirección:', max_length=500, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Dirección:"}))
        # bld_number = forms.CharField(label='Número exterior:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Número exterior:"}))
        # apt_number = forms.CharField(label='Número interior:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Ej. Apartamento 4B:"}))
        # colonia = forms.ChoiceField(label='Colonia:', widget=forms.Select(attrs={'class':'form-control'}))
        # city = forms.CharField(label='Ciudad:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Ejemplo: Chihuahua"}))
        # state = forms.CharField(label='Estado:', max_length=100, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Ejemplo: Chihuahua"}))
        # country = forms.CharField(label='País:', max_length=50, widget=forms.TextInput(attrs={'class':'form-control',"placeholder":"Ejemplo: México"}))
        # zip_code = forms.IntegerField(label='Código postal:', widget=forms.NumberInput(attrs={'class':'form-control',"placeholder":"31136:"}))
        # media_url = forms.FileField(label='Número exterior:', max_length=1000, widget=forms.FileInput(attrs={'class':'form-control'}))
        labels = {
            'tipo_solicitud':'Tipo de solicitud:',
            'descripcion':'Descripción del caso:',
            'street_address':'Dirección:',
            'bld_number':'Número exterior:',
            'apt_number':'Número interior:',
            'colonia':'Colonia:',
            'city':'Ciudad:',
            'state':'Estado:',
            'zip_code':'Código Postal:',
            'media_url':'Medios:',
        }
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows':'2'}),
            'colonia': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_solicitud'].widget.attrs.update({'class': 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class': 'form-control', 'placeholder':'Ingresa una descripción detallada de tu consulta'})
        self.fields['street_address'].widget.attrs.update({'class': 'form-control', 'placeholder':'Dirección:'})
        self.fields['bld_number'].widget.attrs.update({'class': 'form-control', 'placeholder':'Número exterior:'})
        self.fields['apt_number'].widget.attrs.update({'class': 'form-control', 'placeholder':'Ej. Apartamento 4B:'})
        self.fields['colonia'].widget.attrs.update({'class': 'form-control', 'placeholder':'Colonia:'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder':'Ejemplo: Chihuahua'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder':'Ejemplo: Chihuahua'})
        self.fields['zip_code'].widget.attrs.update({'class': 'form-control', 'placeholder':'Ejemplo: 31136'})
        self.fields['media_url'].widget.attrs.update({'class': 'form-control'})



class SolicitudStatusForm(forms.ModelForm):
    class Meta:
        model = Solicitudes
        fields = {'status'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})

class ActividadSeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento_solicitud
        fields = '__all__'
        exclude = ['fecha_actualizacion','tipo_solicitud', 'solicitud_id']

        labels = {
            'texto_status':'Actualización del caso:',
            'status': 'actualiza el status de la Solicitud',
            'evidencia':'Medios:',
        }
        widgets = {
            'texto_status': forms.Textarea(attrs={'rows':'2'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['texto_status'].widget.attrs.update({'class': 'form-control'})
        self.fields['evidencia'].widget.attrs.update({'class': 'form-control'})