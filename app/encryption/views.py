from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.

class Encryption(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="encryption.html"
        )
