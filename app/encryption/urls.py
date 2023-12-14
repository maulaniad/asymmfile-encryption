from django.urls import path

from encryption.views import Encryption


urlpatterns = [
    path("", Encryption.as_view(), name="encryption")
]
