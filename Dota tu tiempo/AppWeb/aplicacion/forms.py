from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Voluntario, InfoPersonal, Administrador

class Formulario(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    class Meta:
        model = None
        fields = "__all__"

    @classmethod
    def get_form(cls, model):
        custom_meta = type('Meta', (cls.Meta,), {'model': model})
        custom_form = type('Formulario', (cls,), {'Meta': custom_meta})
        return custom_form
    


class RegistrarVoluntarioForm(forms.Form):
    cedula = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nombres = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    apellidos = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    celular = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    profesion = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['cedula'], 
            password=self.cleaned_data['cedula'])
        
        personalInfo = InfoPersonal(
            user=user, 
            cedula=self.cleaned_data['cedula'], 
            nombres=self.cleaned_data['nombres'], 
            apellidos=self.cleaned_data['apellidos'],
            celular=self.cleaned_data['celular'], 
            correo=self.cleaned_data['correo'])
        
        voluntario = Voluntario(
            user=user, 
            info_personal=personalInfo,
            profesion=self.cleaned_data['profesion'])   
        
        administrador = Administrador(
            user=user,
            info_personal=personalInfo
        )
            

        try:
            user.save()
            personalInfo.save()
            voluntario.save()
        except:
            user.delete()
            personalInfo.delete()
            voluntario.delete()
            raise
        return voluntario
    
    def update(self, voluntario_instance, commit=True):
        voluntario_instance.info_personal.cedula = self.cleaned_data['cedula']
        voluntario_instance.info_personal.nombres = self.cleaned_data['nombres']
        voluntario_instance.info_personal.apellidos = self.cleaned_data['apellidos']
        voluntario_instance.info_personal.celular = self.cleaned_data['celular']
        voluntario_instance.info_personal.correo = self.cleaned_data['correo']
        voluntario_instance.profesion = self.cleaned_data['profesion']

        if commit:
            voluntario_instance.info_personal.save()
            voluntario_instance.save()
            
        return voluntario_instance
