from django.urls import path

from rsa_decrypt.views import Decryption


urlpatterns = [
    path("", Decryption.as_view(), name="decrypt")
]
