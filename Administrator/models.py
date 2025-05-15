from django.db import models

# Create your models here.
class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=30)
    admin_contact=models.CharField(max_length=30)
    admin_email=models.CharField(max_length=30)
    admin_password=models.CharField(max_length=30)
class tbl_district(models.Model):
    district_name=models.CharField(max_length=30)
class tbl_category(models.Model):
    category_name=models.CharField(max_length=30)
class tbl_place(models.Model):
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    place_name=models.CharField(max_length=30)
    place_pincode=models.CharField(max_length=30) 
class tbl_subcategory(models.Model):
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)
    subcategory_name=models.CharField(max_length=30)
class tbl_department(models.Model):
    department_name=models.CharField(max_length=30)
class tbl_designation(models.Model):
    designation_name=models.CharField(max_length=30) 
class tbl_employee(models.Model):
    department=models.ForeignKey(tbl_department,on_delete=models.CASCADE)
    designation=models.ForeignKey(tbl_designation,on_delete=models.CASCADE)
    employee_name=models.CharField(max_length=30)
    employee_contact=models.CharField(max_length=30)
    employee_email=models.CharField(max_length=30)
    employee_address=models.CharField(max_length=30)
    employee_salary=models.CharField(max_length=30)    

class tbl_subadmin(models.Model):
    district=models.ForeignKey(tbl_district,on_delete=models.CASCADE)
    subadmin_name=models.CharField(max_length=30)
    subadmin_email=models.CharField(max_length=30)
    subadmin_password=models.CharField(max_length=30)




