from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from .forms import TaskFrom

# Create your views here.

def home(request):
    
    return render(request, 'home.html',{
        'form': UserCreationForm()
    }) 

def singup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registrar el usuario
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save() 
                
                login(request, user) #iniciar sesion automaticamente
                
                return redirect('/tasks/')
            
            except IntegrityError:
                return render(request, 'signup.html',{
                     'form': UserCreationForm,
                      "error": "El nombre de usuario ya existe"
                      })
                
                
        return render(request, 'signup.html',{
                'form': UserCreationForm,
                "error": "Las contraseñas no coinciden"
                })    

def tasks(request): 
    return render(request, 'tasks.html')          
    
def create_tasks(request):
    
    if request.method == "get":
        return render(request, 'create_tasks.html',{
        'form': TaskFrom()
    })
    else:
        print(request.POST)
        return render(request, 'create_tasks.html',{
        'form': TaskFrom()
    })
    
    
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method== 'GET':
            return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
    else:
        user = authenticate(
           request, username=request.POST['username'], password =request.POST['password'])
        if user is None:
                return render(request, 'signin.html', {
        'form': AuthenticationForm,
        'error' : 'el usuario o contraseña son incorrectos'
        })
        else:
            login(request, user)
            return redirect('tasks')        
<<<<<<< HEAD
        
=======

>>>>>>> 6ae29341170c078e339fa526af016e4c84aa3eac
    if user is None:
                return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
        
        
   
    


    

