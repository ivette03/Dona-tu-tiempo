from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ("Administrador", 'Administrador'),
        ("Voluntario", 'Voluntario'),
        ("Beneficiario", 'Beneficiario'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default= "Voluntario")

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.get_user_type_display()


class InfoPersonal(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=10, null=False)
    nombres = models.CharField(max_length=50, null=False)
    apellidos = models.CharField(max_length=50, null=False)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    celular = models.CharField(max_length=10, null=True, blank=True)
    correo = models.EmailField(max_length=254, null=True, blank=True)
    foto = models.ImageField(upload_to="imgs", null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class Voluntario(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    info_personal = models.OneToOneField(InfoPersonal, on_delete=models.CASCADE, null=True, blank=True)
    profesion = models.CharField(max_length=50, null=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    
class Beneficiario(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    info_personal = models.OneToOneField(InfoPersonal, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    
class Administrador(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    info_personal = models.OneToOneField(InfoPersonal, on_delete=models.CASCADE, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)



# disponibilidad
class Disponibilidad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='disponibilidades')    
    dia_lunes = models.BooleanField(default=False)
    dia_martes = models.BooleanField(default=False)
    dia_miercoles = models.BooleanField(default=False)
    dia_jueves = models.BooleanField(default=False)
    dia_viernes = models.BooleanField(default=False)
    dia_sabado = models.BooleanField(default=False)
    dia_domingo = models.BooleanField(default=False)
