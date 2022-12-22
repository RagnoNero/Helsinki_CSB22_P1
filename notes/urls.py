from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "notes"

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
	path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('notes/', views.notes, name='notes'),
    path('note/', views.note, name='note'),
    path('remove/<int:id>', views.remove_note, name='remove')
]
