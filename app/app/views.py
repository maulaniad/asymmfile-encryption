from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render

# Create your views here.

class Login(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="login.html"
        )


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
