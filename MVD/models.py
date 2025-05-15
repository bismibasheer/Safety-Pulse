from django.db import models
from Guest.models import *
from RTO.models import *

# Create your models here.
  
     
class tbl_Request(models.Model):
    RTO=models.ForeignKey(tbl_rto,on_delete=models.CASCADE)
    MVD=models.ForeignKey(tbl_Mvd,on_delete=models.CASCADE)
    request_date=models.DateField(auto_now_add=True)
    request_description=models.CharField(max_length=30) 
    Vehicle = models.ForeignKey(tbl_Vehicledetails, on_delete=models.CASCADE)
    request_status=models.IntegerField(default=0) 
    
         