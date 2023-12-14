from django.urls import path

from decryption.views import Decryption


urlpatterns = [
    path("", Decryption.as_view(), name="decryption")
]
