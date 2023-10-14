
from django.urls import path, include
from .views import contacto,index,testimonios,videos

urlpatterns = [
    path('',index,name="inicio"),
    path('testimonios/',testimonios,name="testimonios"),
    path('videos/',videos,name="videos"),
    path('contacto/',contacto,name="contacto"),
    path('app/', include('aplicacion.urls')),
    
]