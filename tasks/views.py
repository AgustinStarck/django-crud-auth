from django.shortcuts import render , get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks' : tasks})

@login_required
def completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks' : tasks})

@login_required
def create_tasks(request):
    
    if request.method == "GET":
        return render(request, 'create_tasks.html',{
        'form': TaskForm()
    })
    else:
        try:
            form1 = TaskForm(request.POST)
            new_task = form1.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect ('tasks')
        except ValueError:
            if request.method == "GET":
                return render(request, 'create_tasks.html',{
                'form': TaskForm(),
                'error' : 'please provide valid data'
                })

@login_required    
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

    if user is None:
                return render(request, 'signin.html', {
        'form': AuthenticationForm
    })
        
@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'task_detail.html',{'task': task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
             return render(request,'task_detail.html',{'task': task, 'form':form, 'error':"hubo un error la actualizar"})

@login_required
def task_completed(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    #return render(request, 'task:completed', {'task': task})

@login_required
def task_deleted(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
    
    
   
    


    

