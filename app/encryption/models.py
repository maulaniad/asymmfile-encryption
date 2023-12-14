from datetime import date

from django.db import models

from data.models import File, User

# Create your models here.

class Encryption(models.Model):
    id = models.BigAutoField(primary_key=True)
    begin_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=date(2099, 11, 11))

    file = models.ForeignKey(to=File, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        db_table = "tb_encryption"
