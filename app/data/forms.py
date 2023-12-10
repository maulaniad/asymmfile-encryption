from django import forms

# Create your forms here.

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField(max_length=256)
    fullname = forms.CharField(max_length=50)
    username = forms.CharField(max_length=25)
    password = forms.CharField(widget=forms.PasswordInput)
