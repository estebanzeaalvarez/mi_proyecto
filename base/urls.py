# base/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('registro/', views.registerPage, name='register'),
    path('comment/', views.comment, name='comment'),
    path('logout/', views.logoutPage, name='logout'),
    path('post/', views.post, name='create_post'),  # Ruta para crear un post
    path('post/<int:id>/', views.post, name='edit_post'),  # Ruta para editar un post
    path('weather/', views.weather, name='weather'),
]

