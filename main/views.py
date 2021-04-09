from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from . import forms
from .serializers import UserSerializer, BmiSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.

def bmi_calculator(height, weight):
    height /= 100
    bmi = weight/(height**2)
    return round(bmi, 2)


def bmi_status(bmi):
    if bmi <= 18.5:
        status = "کم وزن"
    elif 18.5 < bmi <= 24.9:
        status = "وزن طبیعی"
    elif 24.9 < bmi <= 29.9:
        status = "اضافه وزن"
    elif 29.9 < bmi <= 39.9:
        status = "چاقی مفرط-نوع1"
    else:
        status = "چاقی مفرط-نوع1"
    return status



#Views
def index(request):
    if request.user.is_authenticated: 
        context={ 
            "authenticated":True,
            "name": request.user.get_full_name(),
            }
    else:
        context={ 
            "authenticated":False,
            }
    return render(request, 'index.html', context)

def bmi(request):
    if request.method == "GET":
        return render(request, 'bmi.html')
    if request.method == "POST":
        if 'height' and 'weight' in request.POST:
            form = forms.BmiForm(request.POST)
            if form.is_valid():
                weight = request.POST['weight']
                height = request.POST['height']
                bmi = bmi_calculator(int(height), int(weight))
                status = bmi_status(bmi)
                context = {
                    "bmi":bmi,
                    "status":status,
                    "height":height,
                    "weight":weight,
                    "form":form,
                    }
                return render(request, 'bmi.html', context)
            else:
                context = {
                    "form":form,
                    }
                return render(request, 'bmi.html', context)



def signin(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'error':'نام کاربری یا کلمه عبور اشتباه است!'})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('/')




#APIViews
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )


class BmiApi(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = BmiSerializer(data=data)
        if serializer.is_valid():
            bmi = bmi_calculator(serializer.data["height"], serializer.data["weight"])
            status = bmi_status(bmi)
            response_data = {
                "height": serializer.data["height"],
                "weight": serializer.data["weight"],
                "bmi": bmi,
                "status": status
            }
            return Response(response_data, status=200)
        return Response(serializer.errors, status=400)