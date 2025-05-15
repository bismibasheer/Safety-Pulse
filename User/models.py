from django.db import models
from Guest.models import *
from User.models import *
from RTO.models import *

class tbl_Complaint(models.Model):
    Category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
    User=models.ForeignKey(tbl_User,on_delete=models.CASCADE)
    MVD=models.ForeignKey(tbl_Mvd,on_delete=models.CASCADE)
    complaint_description=models.CharField(max_length=30)
    complaint_photo=models.FileField(upload_to="Assets/Complaint/photo/")
    complaint_status=models.IntegerField(default=0)
    complaint_date=models.DateField(auto_now_add=True)
    reply_complaint=models.CharField(max_length=30)
    complaint_amount=models.CharField(max_length=30)
    vehicle_number=models.ForeignKey(tbl_Vehicledetails, on_delete=models.CASCADE)
    complaint_payment = models.IntegerField(default=0)

class tbl_multipleviolation(models.Model):
    complaint=models.ForeignKey(tbl_Complaint,on_delete=models.CASCADE)
    status=models.IntegerField(default=0)

class tbl_Feedback(models.Model):
    User=models.ForeignKey(tbl_User,on_delete=models.CASCADE)
    feedback_content=models.CharField(max_length=30)

class tbl_rating(models.Model):
    rating_data=models.IntegerField()
    user_review=models.CharField(max_length=500)
    user=models.ForeignKey(tbl_User,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)

class tbl_points(models.Model):
    point_credited=models.IntegerField(default=0)
    point_widthdrawed=models.IntegerField(default=0)
    user=models.ForeignKey(tbl_User,on_delete=models.CASCADE)
    point_date=models.DateField(auto_now_add=True)