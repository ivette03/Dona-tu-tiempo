from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict

from django.http import JsonResponse
import json
from django.db.models import Q
from django.db.models.fields.related import ForeignKey
from aplicacion.models import Voluntario, InfoPersonal, Disponibilidad
from aplicacion.forms import RegistrarVoluntarioForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()


def remove_csrf_token(values):
    values.pop("csrfmiddlewaretoken", None)
    
def process_data(request, id, model):
    if request.method == "GET":
        data = get_object_or_404(model, id=id)
        data_dict = model_to_dict(data)
        # Convertir los objetos relacionales a diccionarios para la respuesta JSON
        for field in model._meta.get_fields():
            if isinstance(field, ForeignKey):
                related_object = getattr(data, field.name)
                if related_object:
                    data_dict[field.name] = related_object.__str__()  # Mostrar el nombre del objeto relacionado
                else:
                    data_dict[field.name] = None
        return JsonResponse(data_dict)

    if request.method == "POST":
        values = request.POST.dict()
        remove_csrf_token(values)

        # Modificación para tratar las relaciones ForeignKey
        for field in model._meta.get_fields():
            if isinstance(field, ForeignKey):
                related_model = field.related_model
                related_id = values.get(f"{field.name}")
                
                if related_id:
                    try:
                        # Intenta obtener la instancia relacionada utilizando el id
                        related_instance = related_model.objects.get(id=related_id)
                    except related_model.DoesNotExist:
                        # Si el objeto relacionado no existe, muestra un mensaje de error
                        return JsonResponse({"error": f"El {field.name} con ID {related_id} no existe."}, status=400)
                    
                    # Asigna la instancia relacionada al campo ForeignKey en el diccionario de valores
                    values[field.name] = related_instance
                else:
                    # Si no se proporcionó un ID, asigna None al campo ForeignKey en el diccionario de valores
                    values[field.name] = None


        if id:
            # Es una solicitud de actualización, busca la materia existente
            data = get_object_or_404(model, id=id)
            for key, value in values.items():
                setattr(data, key, value)
            data.save()
            return JsonResponse({"success": "Datos actualizados correctamente"})
        else:
            # Es una solicitud de creación de una nueva materia
            model.objects.create(**values)
            return JsonResponse({"success": "Datos creados correctamente"})
        
    if request.method == "PUT":
        data = get_object_or_404(model, id=id)
        values = json.loads(request.body)
        remove_csrf_token(values)
        for key, value in values.items():
            setattr(data, key, value)
        data.save()
        return JsonResponse({"success": "Datos actualizados correctamente"})

    if request.method == "DELETE":
        data = get_object_or_404(model, id=id)
        data.delete()
        return JsonResponse({"success": "Datos eliminados correctamente"})
    

class UserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if not user:
            InvalidCredentials = "Credenciales inválidas. Inténtalo nuevamente."
            return render(request, 'login.html', {'LoginErrorMsg': InvalidCredentials})
        else:
            login(request, user)


            if user.user_type == 'Administrador':
                return redirect('admin_view')
            
            elif user.user_type == 'Voluntario':
                return redirect('voluntario_view')
            
            
            else:
                return render(request, 'login.html', {'LoginErrorMsg': 'No tienes permisos para ingresar'})
    else:
        return render(request, 'login.html')
    
    
    
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # check if the user is an admin or a volunteer
    user = request.user or User.objects.get(id=request.user.id)
    if user.user_type == 'Administrador':
        return redirect('admin_view')
    elif user.user_type == 'Voluntario':
        return redirect('voluntario_view')
    
    
    return render(request, 'home.html')

def voluntario_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user or request.user.user_type != 'Voluntario':
        return redirect('index')
    

    user = request.user or User.objects.get(id=request.user.id)
    info_personal = get_object_or_404(InfoPersonal, user=user)
    
    return render(request, 'voluntario/default.html', {
        "username": info_personal.nombres,
    })
    

def admin_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user or request.user.user_type != 'Administrador':
        return redirect('home')
    
    user = request.user or User.objects.get(id=request.user.id)
    info_personal = get_object_or_404(InfoPersonal, user=user)
    
    return render(request, 'administrador/default.html', {
        "username": info_personal.nombres,
    })



def horario_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'GET':    
        user = request.user or User.objects.get(id=request.user.id)
        info_personal = get_object_or_404(InfoPersonal, user=user)
        voluntario = get_object_or_404(Voluntario, user=user)
        
        try:
            disponibilidad = get_object_or_404(Disponibilidad, user=user)
        except:
            disponibilidad = Disponibilidad(user=user)
            disponibilidad.save()
        
        disponibilidad = get_object_or_404(Disponibilidad, user=user)

        
        disponibilidad = model_to_dict(disponibilidad)
        
        
        disponibilidad = {k: v for k, v in disponibilidad.items() if k.startswith('dia_')}
        return render(request, 'voluntario/horario.html', {
            "username": info_personal.nombres,
            "diasDisponibles" : disponibilidad,
            "infoPersonal": info_personal,
            "voluntario": voluntario,
        })
        
        
    elif request.method == 'POST':
        dias_seleccionados_json = request.POST.get('dias_seleccionados', '[]')
        dias_seleccionados = json.loads(dias_seleccionados_json)
        user = request.user or User.objects.get(id=request.user.id)
        dias_seleccionados_dict = {
            'dia_lunes': 'LU' in dias_seleccionados,
            'dia_martes': 'MA' in dias_seleccionados,
            'dia_miercoles': 'MI' in dias_seleccionados,
            'dia_jueves': 'JU' in dias_seleccionados,
            'dia_viernes': 'VI' in dias_seleccionados,
            'dia_sabado': 'SA' in dias_seleccionados,
            'dia_domingo': 'DO' in dias_seleccionados,
        }
        disponibilidad, created = Disponibilidad.objects.update_or_create(
            user=user,
            defaults=dias_seleccionados_dict
        )
        return redirect('horario_view')
def horarios_view(request):
    busqueda = request.GET.get("buscar")
    
    if busqueda:
        voluntarios = Voluntario.objects.filter(
            Q(info_personal__cedula=busqueda) |
            Q(info_personal__nombres__icontains=busqueda.split()[0]) |
            Q(info_personal__apellidos__icontains=busqueda.split()[0]) |
            Q(profesion=busqueda)
        ).distinct()
    else:
        voluntarios = Voluntario.objects.all()
    
    paginator = Paginator(voluntarios, 10)
    page = request.GET.get('page')
    voluntarios_paginated = paginator.get_page(page)
    
    if not request.user.is_authenticated:
        return redirect('login')
        
    if not request.user or request.user.user_type != 'Administrador':
        return redirect('home')
    
    disponibilidades = Disponibilidad.objects.filter(
        Q(dia_lunes=True) | Q(dia_martes=True) | Q(dia_miercoles=True) |
        Q(dia_jueves=True) | Q(dia_viernes=True) | Q(dia_sabado=True) |
        Q(dia_domingo=True)
    )
    
    voluntarios_dict = []  # Lista para almacenar los voluntarios y sus detalles
    
    for voluntario in voluntarios_paginated:
        voluntario_dict = model_to_dict(voluntario)
        info_personal = get_object_or_404(InfoPersonal, user=voluntario.user)
        voluntario_dict["infoPersonal"] = model_to_dict(info_personal)
        
        # Obtener la disponibilidad del voluntario y agregarla al diccionario, si no existe, agregar un diccionario vacío
        if disponibilidades.filter(user=voluntario.user).exists():
            voluntario_dict["diasDisponibles"] = model_to_dict(disponibilidades.get(user=voluntario.user))
        else:
            voluntario_dict["diasDisponibles"] = {}
        
        voluntarios_dict.append(voluntario_dict)  # Agregar el diccionario del voluntario a la lista
    
    return render(request, 'administrador/horarios.html', {
        "voluntarios": voluntarios_dict,
        "voluntarios_paginated": voluntarios_paginated  # Pasa la variable de paginación a la plantilla
    })

def getVoluntarioById(id):
    user = get_object_or_404(User, id=id)
    voluntario = get_object_or_404(Voluntario, user=user)
    
    info_personal = get_object_or_404(InfoPersonal, user=user)
    
    voluntario_dict = model_to_dict(voluntario)
    
    info_personal_dict = model_to_dict(info_personal)
    
    info_personal_dict["foto"] = info_personal.foto.url if info_personal.foto else None
    
    voluntario_dict["info_personal"] = info_personal_dict
    
    return JsonResponse(voluntario_dict)
def registrar_voluntario(request, id=None):
    
    if not request.user.is_authenticated:
        return redirect('login')

    if not request.user or request.user.user_type != 'Administrador':
        return redirect('home')

    user = request.user or User.objects.get(id=request.user.id)
    info_personal = get_object_or_404(InfoPersonal, user=user)

    if not id and request.method == "GET":
        busqueda = request.GET.get("buscar")

        if not busqueda:
            tvalues = Voluntario.objects.all()
        else:
            tvalues = Voluntario.objects.filter(
                Q(info_personal__cedula=busqueda) |
                Q(info_personal__nombres__icontains=busqueda.split()[0]) |
                Q(info_personal__apellidos__icontains=busqueda.split()[0]) |
                Q(profesion=busqueda)
            ).distinct()

        paginator = Paginator(tvalues, 10)
        page = request.GET.get('page')
        voluntarios_paginated = paginator.get_page(page)

        return render(request, "administrador/agregar_voluntario.html", {
            "categoria": "Voluntario",
            "tvalues": voluntarios_paginated,
            "form": RegistrarVoluntarioForm,
            "username": info_personal.nombres,
            
        })
    else:
        if request.method == "GET":
            return getVoluntarioById(id)

        elif request.method == "POST":
            tvalues = Voluntario.objects.all()
            existUser = User.objects.filter(username=request.POST['cedula']).exists()
            paginator = Paginator(tvalues, 10)
            page = request.GET.get('page')
            voluntarios_paginated = paginator.get_page(page)

            try:
                values = request.POST.dict()
                remove_csrf_token(values)
                form = RegistrarVoluntarioForm(values)

                if form.is_valid():
                    form.save()
                    return redirect("registrar_voluntario")
            except IntegrityError:
                integrity_error = "No se pudo agregar, este usuario ya existe!"
                return render(request,'administrador/agregar_voluntario.html',{
                    'integrity_error':integrity_error, "tvalues": voluntarios_paginated,
                    "form": RegistrarVoluntarioForm,
                    "username": info_personal.nombres,
                    })

        elif request.method == "PUT":
            user = get_object_or_404(User, id=id)
            voluntario = get_object_or_404(Voluntario, user=user)

            # Parsea el JSON recibido en la solicitud
            data = json.loads(request.body)

            # Rellena el formulario con los datos del JSON y la instancia del voluntario existente
            form = RegistrarVoluntarioForm(data)

            if form.is_valid():
                # Guarda los cambios en el objeto Voluntario
                form.update(voluntario_instance=voluntario)
                # Devuelve una respuesta JSON con los datos actualizados

            return redirect("registrar_voluntario")

        elif request.method == "DELETE":
            user = get_object_or_404(User, id=id)
            user.delete()
            return JsonResponse({"success": "Datos eliminados correctamente"})



def cambiar_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        password = request.POST['password']
        user = request.user or User.objects.get(id=request.user.id)
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'cambiar_password.html')



def logout_view(request):
    logout(request)
    return redirect('login')





















