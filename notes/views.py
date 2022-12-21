from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create(username=username, password=password)
            return redirect('/login')

    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #don't use get, otherwise django raises an exception if no user was found
        user = User.objects.filter(username=username, password=password).first()
        if user is not None:
            login(request, user)
            return redirect('/index')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})