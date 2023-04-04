
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loadpage, name='load'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('homepage/<str:user_name>/', views.home_screen, name='homepage'),
    path('homepage/<str:user_name>/profile/', views.profile, name='profile'),
    path('homepage/<str:user_name>/ResetPassword', views.password_reset, name='password'),
    path('loadout/', views.loadpage, name='loadout'),
    path('homepage/<str:user_name>/botchat/', views.chat_with_bot_page, name='botchat'),

]
