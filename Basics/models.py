from django.db import models
from Basics.models import *
from Administrator.models import *


# Create your models here.
class tbl_Rgister(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_address=models.CharField(max_length=30)
    user_password=models.CharField(max_length=30)
    user_photo=models.FileField(upload_to="Assets/User/photo/")
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)


class tbl_ano(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_address=models.CharField(max_length=30)
    user_password=models.CharField(max_length=30)
    user_photo=models.FileField(upload_to="Assets/User/photo/")
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)    