from django.db import models
from Administrator.models import *


class tbl_User(models.Model):
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)
    user_contact=models.CharField(max_length=30)
    user_address=models.CharField(max_length=30)
    user_photo=models.FileField(upload_to="Assets/User/photo/")
    user_proof=models.FileField(upload_to="Assets/User/photo/")
    user_password=models.CharField(max_length=30)
    user_status=models.IntegerField(default=0) 

class tbl_Mvd(models.Model):
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    mvd_name=models.CharField(max_length=30)
    mvd_email=models.CharField(max_length=30)
    mvd_contact=models.CharField(max_length=30)
    mvd_address=models.CharField(max_length=30)
    mvd_photo=models.FileField(upload_to="Assets/Mvd/photo/")
    mvd_proof=models.FileField(upload_to="Assets/Mvd/photo/")
    mvd_password=models.CharField(max_length=30)
    mvd_status=models.IntegerField(default=0)    


class tbl_rto(models.Model):
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    rto_name=models.CharField(max_length=30)
    rto_email=models.CharField(max_length=30)
    rto_contact=models.CharField(max_length=30)
    rto_address=models.CharField(max_length=30)
    rto_photo=models.FileField(upload_to="Assets/Rto/photo/")
    rto_proof=models.FileField(upload_to="Assets/Rto/photo/")
    rto_password=models.CharField(max_length=30)
    rto_status=models.IntegerField(default=0)   

 
