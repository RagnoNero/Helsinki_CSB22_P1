from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Note
from django.template.loader import render_to_string

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
    if request.user.is_authenticated:
        return redirect('notes')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #don't use get, otherwise django raises an exception if no user was found
        user = User.objects.filter(username=username, password=password).first()
        if user is not None:
            login(request, user)
            return redirect('/notes')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def note(request):
    if request.method == 'GET':
        note_id = int(request.GET.get('id', 0))
        if note_id > 0:
            selected_note = Note.objects.filter(id=note_id).first()
            if not selected_note or selected_note.user_id != request.user:
                return HttpResponse(render_to_string('error.html', {'error_message': 'Unauthorized!'}), status=401)
            return render(request, 'note.html', { 'note': selected_note })
        return render(request, 'note.html')
    
    if request.method == 'POST':
        id = request.POST.get('id', 0)
        note_id = int(0 if not id else id)
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if note_id > 0:
            note = Note.objects.get(pk=note_id)
            note.title = title
            note.content = content
            note.save()

            return redirect('/note/?id=%i' % note_id)
        else:
            note = Note.objects.create(title=title, content=content, user_id=request.user)
            return redirect('/note/?id=%i' % note.id)
    return render(request, 'notes.html')


@login_required
def notes(request):
    notes = Note.objects.filter(user_id=request.user.id)
    context = {
        'notes': notes,
    }
    return render(request, 'notes.html', context)


@login_required
def remove_note(request, id):
    note = Note.objects.filter(id=id)
    if not note or note.user_id != request.user:
        return HttpResponse(render_to_string('error.html', {'error_message': 'Unauthorized!'}), status=401)
    note.delete()
    return redirect('/notes')
