from django.urls import path
from django.contrib.auth import views
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', views.LoginView.as_view(),
         name='login', kwargs={'next_page': '/'}),
    path('logout/', views.LogoutView.as_view(),
         name='logout', kwargs={'next_page': '/'}),
]
