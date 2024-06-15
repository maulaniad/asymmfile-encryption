"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from app.views import (SessionCorrector,
                       Login,
                       Register,
                       Logout,
                       Dashboard,
                       MasterData,
                       DownloadPDF)


urlpatterns = [
    path("", SessionCorrector.as_view(), name="session_corrector"),

    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),

    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path("data/", MasterData.as_view(), name="master_data"),
    path("data/download/<int:format_id>/", DownloadPDF.as_view(), name="download_pdf"),
    path("data/entry/", include(("data_entry.urls", "data_entry"), namespace="data_entry")),
    path("data/decrypt/", include(("data_decrypt.urls", "data_decrypt"), namespace="data_decrypt")),
    path("rsa/encrypt/", include(("rsa_encrypt.urls", "rsa_encrypt"), namespace="rsa_encrypt")),
    path("rsa/decrypt/", include(("rsa_decrypt.urls", "rsa_decrypt"), namespace="rsa_decrypt")),
]
