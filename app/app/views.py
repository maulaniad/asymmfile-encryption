from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import redirect, render

from data.models import User

# Create your views here.

class Login(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="login.html"
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        username_or_email = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user_data = User.objects.filter(
            Q(username=username_or_email) | Q(email=username_or_email)
        ).first()

        if not user_data:
            return redirect(to="/login/?login_status=USER_NOT_EXIST")

        if not check_password(password, user_data.password):
            return redirect(to="/login/?login_status=WRONG_PASSWORD")

        return redirect(to="/dashboard/")


class Register(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="register.html"
        )

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        fullname = request.POST.get('fullname', None)
        password = make_password(request.POST.get('passwordA', None))

        user_data = User(
            username=username,
            email=email,
            fullname=fullname,
            password=password
        )

        user_data.save()

        return redirect(to="/login/?register_status=OK")


class Dashboard(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="dashboard.html",
            context={'test': "Hello World"}
        )


class NotFound(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="404_not_found.html"
        )
