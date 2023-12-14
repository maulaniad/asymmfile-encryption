from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render

# Create your views here.

class Decryption(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(
            request=request,
            template_name="decryption.html"
        )
