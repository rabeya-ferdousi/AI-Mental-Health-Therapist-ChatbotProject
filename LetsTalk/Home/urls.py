
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loadpage, name='load'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('homepage/<str:user_name>/', views.home_screen, name='homepage'),


]
