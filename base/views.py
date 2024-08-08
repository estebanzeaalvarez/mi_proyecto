# base/views.py
import requests
import arrow
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Post, Comment


def loginPage(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:   
                login(request, user)
                messages.success(request, "Se inicio sesion")
                return redirect('/')
            
        messages.error(request, 'Datos incorrectos', extra_tags='danger')

    return render(request, 'layouts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('/')

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not last_name:
            messages.error(request, 'El apellido es obligatorio')
            return redirect('/registro')

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('/registro')
        
        User.objects.create_user(username=username, email=email, first_name=name, last_name=last_name, password=password)
        return redirect('/login')
    
    return render(request, 'layouts/register.html')



def home(request):
    posts = Post.objects.order_by('-created')
    return render(request, 'home.html', {'posts': posts})

def post(request, id=None):
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if id:
            try:
                p = Post.objects.get(id=id)
                if p.user == request.user:
                    p.title = title
                    p.text = text
                    if image:
                        p.image = image
                    p.save()
                    messages.success(request, "Post actualizado correctamente")
                else:
                    messages.error(request, "No tienes permiso para editar este post")
            except Post.DoesNotExist:
                messages.error(request, "El post no existe")
        else:
            Post.objects.create(
                title=title,
                text=text,
                image=image,
                user=request.user
            )
            messages.success(request, "Post creado correctamente")
        return redirect('/')

    context = {}
    if id is not None:
        try:
            p = Post.objects.get(id=id)
            context['post'] = p
        except Post.DoesNotExist:
            messages.error(request, "El post no existe")
            return redirect('/')

    return render(request, 'layouts/post.html', context)

def comment(request):
    p = Post.objects.get(id = request.POST.get('post'))
    Comment.objects.create(
        text = request.POST.get('text'),
        user = request.user,
        post = p
    )
    return redirect('/')

def weather(request):
    api_key = settings.STORMGLASS_API_KEY
    start = arrow.now().floor('day').to('UTC').timestamp()
    end = arrow.now().ceil('day').to('UTC').timestamp()
    
    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat': 58.7984,  # Reemplaza con la latitud deseada
            'lng': 17.8081,  # Reemplaza con la longitud deseada
            'params': ','.join(['waveHeight', 'airTemperature']),
            'start': start,
            'end': end
        },
        headers={
            'Authorization': api_key
        }
    )
    
    return JsonResponse(response.json())
