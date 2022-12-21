from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label="password",widget=forms.PasswordInput, max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label="password",widget=forms.PasswordInput, max_length=100)