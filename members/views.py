from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import TaskForm, CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
@login_required(login_url='members:login')
def dashboard(request):
    if request.user.is_authenticated:
        search_query = ''
        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')

        user = request.user
        tasks = Task.objects.filter(user = user, name__icontains=search_query)

        form = TaskForm()

        if request.method=='POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = user
                form.save()
            return redirect('/')

        context = {'tasks':tasks, 'form':form}
        return render(request, 'dashboard.html', context)

@login_required(login_url='members:login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'update_form': form}
    return render(request, 'update_task.html', context)

@login_required(login_url='members:login')
def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('members:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('members:dashboard')
            else:
                messages.info(request, 'Username or Password is incorrect')

        return render(request, 'user_login.html')

def user_logout(request):
  if request.method == 'POST':
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('members:login')
  
def user_register(request):
    if request.user.is_authenticated:
        return redirect('members:dashboard')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for' + user)
                return redirect('members:login')
        context = {'form':form}
        return render(request, 'user_register.html', context=context)
    

@login_required(login_url='members:login')
def contactus(request):
    if request.method == "POST":
        print("hii")
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_mobile = request.POST['message-mobile']

        try:
            send_mail('Contact Form',
            message_name + message_email + message_mobile,
            
            settings.EMAIL_HOST_USER,
            ['sarathupsrl@gmail.com'], 
            fail_silently=False)


            return redirect('members:dashboard')
        except:
            return redirect('members:contactus')
    else:
    
        return render(request, 'contact_us.html')
    