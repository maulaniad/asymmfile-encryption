from django.http import HttpRequest, HttpResponse
from django.views import View
from django.shortcuts import render

# Create your views here.

class Dashboard(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request=request,
            template_name="dashboard.html",
            context={'test': "Hello World"}
        )
