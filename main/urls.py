from . import views
from django.urls import path
urlpatterns = [
    path('', views.index),
    path('login', views.signin),
    path('register', views.signup),
    path('logout', views.signout),
    path('bmi', views.bmi),
    path('api/login', views.login_user_api),
    path('api/register', views.create_user_api),
    path('api/bmi', views.bmi_api),
]
