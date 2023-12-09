from datetime import date

from django.db import models

from helpers.types import ALLOWED_FILETYPES, USER_ACTION

# Create your models here.

class User(models.Model):
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    email = models.CharField(max_length=256)
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=256)

    class Meta:
        db_table = "tb_user"


class File(models.Model):
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    file_name = models.CharField(max_length=50)
    file_path = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=5, decimal_places=2)
    extension = models.CharField(max_length=5, choices=ALLOWED_FILETYPES)

    class Meta:
        db_table = "tb_file"


class RSAKeyPair(models.Model):
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    private_key = models.TextField()
    public_key = models.TextField()
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = "tb_rsa_keypair"


class Log(models.Model):
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file = models.ForeignKey(to=File, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=USER_ACTION)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_log"
