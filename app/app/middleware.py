from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# Create your middleware here, a class that can be used for allowed routes when authenticated.

class AuthMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        login_url = reverse('login')
        register_url = reverse('register')
        dashboard_url = reverse('dashboard')

        if "is_loggedin" not in request.session:
            if request.path not in [login_url, register_url]:
                return redirect(login_url)
        else:
            if request.path in [login_url, register_url]:
                return redirect(dashboard_url)

        response = self.get_response(request)

        return response
