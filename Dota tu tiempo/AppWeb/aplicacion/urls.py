from django.contrib import admin
from django.urls import path
from aplicacion.views import login_view, admin_view, voluntario_view, logout_view, index, registrar_voluntario, cambiar_password, horario_view, horarios_view

urlpatterns = [
    path('', index ,name="home"),
    
    path('login/', login_view, name='login'),
    
    path('administrador/', admin_view, name='admin_view'),
    path('administrador/', admin_view, name='admin_view'),
    
    path('administrador/registrar_voluntario/', registrar_voluntario, name='registrar_voluntario'),
    path('administrador/registrar_voluntario/<int:id>', registrar_voluntario, name='registrar_voluntario'),
    path('administrador/horarios/', horarios_view, name='horarios_view'),

    
    path('voluntario/', voluntario_view, name='voluntario_view'),
    path('voluntario/horario/', horario_view, name='horario_view'),

    
    path('logout/', logout_view, name='logout'),

    path('cambiar_password/', cambiar_password, name='cambiar_password'),    
]
