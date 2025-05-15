from django.db import models
from Guest.models import *


class tbl_Video(models.Model):
    RTO=models.ForeignKey(tbl_rto,on_delete=models.CASCADE)
    video_file=models.FileField(upload_to="Assets/Videofile/photo/")
    video_date=models.DateField(auto_now_add=True)
    video_description=models.CharField(max_length=30)

class tbl_Article(models.Model):
    RTO=models.ForeignKey(tbl_rto,on_delete=models.CASCADE)
    article_file=models.FileField(upload_to="Assets/Articlefile/photo/")
    article_date=models.DateField(auto_now_add=True)
    article_description=models.CharField(max_length=30)  

class tbl_Vehicledetails(models.Model):
    RTO=models.ForeignKey(tbl_rto,on_delete=models.CASCADE)
    vehicle_number=models.CharField(max_length=30)
    vehicleuser_name=models.CharField(max_length=30)
    vehicle_date=models.DateField(auto_now_add=True)
    