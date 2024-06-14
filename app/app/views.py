from datetime import datetime

from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render

from database.forms import LoginForm, RegisterForm
from database.models import User

# Create your views here.

class SessionCorrector(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            if request.session['is_loggedin']:
                request.session['user_id']

            return redirect(to="/dashboard/")
        except KeyError:
            return redirect(to="/login/")


class Login(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="login.html"
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = LoginForm(request.POST)

        if not form.is_valid():
            return redirect(to="/login/?login_status=BAD")

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user_data = User.objects.filter(
            Q(begin_date__lte=datetime.now()),
            Q(end_date__gte=datetime.now()),
            Q(username=username) | Q(email=username)
        ).first()

        if not user_data:
            return redirect(to="/login/?login_status=USER_DOES_NOT_EXIST")

        if not check_password(password=password, encoded=user_data.password):
            return redirect(to="/login/?login_status=WRONG_PASSWORD")

        request.session['user_id'] = user_data.id
        request.session['email'] = user_data.email
        request.session['fullname'] = user_data.fullname
        request.session['username'] = user_data.username
        request.session['is_loggedin'] = True

        return redirect(to="/dashboard/")


class Register(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="register.html"
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return redirect(to="/login/?register_status=BAD")

        email = form.cleaned_data['email']
        fullname = form.cleaned_data['fullname']
        username = form.cleaned_data['username']
        password = make_password(form.cleaned_data['password'])

        user_data = User(
            email=email,
            fullname=fullname,
            username=username,
            password=password
        )

        user_data.save()

        return redirect(to="/login/?register_status=OK")


class Logout(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        request.session.pop('user_id', None)
        request.session.pop('email', None)
        request.session.pop('username', None)
        request.session.pop('fullname', None)
        request.session.flush()

        return redirect(to="/login/")


class Dashboard(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="dashboard.html",
        )


class MasterData(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="master_data.html",
        )
