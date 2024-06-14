from django.shortcuts import render
from django.views import View

# Create your views here.

class DataDecrypt(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'data_decrypt.html')
