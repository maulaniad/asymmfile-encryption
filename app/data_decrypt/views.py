from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.

class DataDecrypt(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, 'data_decrypt.html')

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, 'data_decrypt.html')
