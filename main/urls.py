from . import views
from django.urls import path
urlpatterns = [
    path('', views.index),
    path('login', views.signin),
    path('register', views.signup),
    path('logout', views.signout),
    path('bmi', views.bmi),
    path('api/register', views.UserCreate.as_view()),
    path('api/bmi', views.BmiApi.as_view()),
]
