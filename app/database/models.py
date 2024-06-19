from datetime import date
from json import dumps

from django.db import models

from helpers.types import ALLOWED_FILETYPES, USER_ACTION, FileStatus

# Create your models here.

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    email = models.CharField(max_length=256)
    fullname = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=256)

    class Meta:
        db_table = "tb_user"


class File(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    file = models.FileField()
    filename = models.CharField(max_length=50)
    size = models.DecimalField(max_digits=5, decimal_places=2)
    extension = models.CharField(max_length=5, choices=ALLOWED_FILETYPES)
    aes_key = models.CharField(max_length=255, blank=True)
    vector = models.CharField(max_length=255, blank=True)
    secret_key = models.CharField(max_length=255, blank=True)
    format = models.ForeignKey(to="FormatData", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = self.file.name
        if not self.size:
            self.size = self.file.size
        if not self.extension:
            self.extension = self.filename.split('.')[-1]
        if isinstance(self.status, FileStatus):
            self.status = self.status.value
        super(File, self).save(*args, **kwargs)

    class Meta:
        db_table = "tb_file"


class RSAKeyPair(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    private_key = models.TextField()
    public_key = models.TextField()
    file = models.ForeignKey(to=File, on_delete=models.CASCADE)

    class Meta:
        db_table = "tb_rsa_keypair"


class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    file = models.ForeignKey(to=File, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=USER_ACTION)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_log"


class FormatData(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    format_name = models.CharField(max_length=50)
    fields = models.JSONField()

    def save(self, *args, **kwargs):
        if isinstance(self.fields, (dict, list)):
            self.fields = dumps(self.fields)

        return super(FormatData, self).save(*args, **kwargs)

    class Meta:
        db_table = "tb_format_data"


class Data(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    data = models.JSONField()
    format = models.ForeignKey(to=FormatData, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if isinstance(self.data, (dict, list)):
            self.data = dumps(self.data)

        return super(Data, self).save(*args, **kwargs)

    class Meta:
        db_table = "tb_data"
