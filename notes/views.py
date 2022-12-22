from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Note


# Create your views here.
def index(request):
    return render(request, 'index.html')


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
            return redirect('/allNotes')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def add_note(request):
    if request.method == 'POST':
        note_id = int(request.POST.get('id', 0))
        user_id = request.user.id
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if note_id > 0:
            document = Note.objects.get(pk=note_id)
            document.title = title
            document.content = content
            document.save()

            return redirect('/?id=%i' % note_id)
        else:
            document = Note.objects.create(title=title, content=content, user_id=user_id)

            return redirect('/?id=%i' % document.id)
    return render(request, 'addNote.html')


@login_required
def view_notes(request):
    notes = Note.objects.filter(user_id=request.user.id)
    return render(request, 'allNotes.html', notes)


@login_required
def remove_note(request):
    note_id = request.POST.get('remove')
    note = Note.objects.get(id=note_id)
    note.delete()
    return redirect('/allNotes')
