from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from . import forms
from rest_framework.views import APIView
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




def index(request):
    if request.user.is_authenticated: 
        print(request.user.get_full_name())
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



@csrf_exempt
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
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form)
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



# @api_view(['POST'])
def create_user_api(request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

def login_user_api(request):
    return None


def bmi_api(request):
    return None
