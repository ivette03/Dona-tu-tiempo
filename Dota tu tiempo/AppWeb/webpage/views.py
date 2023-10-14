from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')
def contacto(request):
    return render(request,'contacto.html')
def testimonios(request):
    return render(request,'testimonios.html')
def videos(request):
    return render(request,'videos.html')

