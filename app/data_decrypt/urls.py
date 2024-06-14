from django.urls import path

from data_decrypt.views import DataDecrypt


urlpatterns = [
    path('', DataDecrypt.as_view(), name='data_decrypt'),
]
