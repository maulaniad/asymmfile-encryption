from django.urls import path

from rsa_encrypt.views import Encryption


urlpatterns = [
    path("", Encryption.as_view(), name="encrypt")
]
