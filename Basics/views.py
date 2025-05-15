from django.shortcuts import render
from Administrator.models import *
from Guest.models import *
from Basics.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def calculator(request):
    if request.method=='POST':
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        btn=request.POST.get('btn_submit')
        if btn =='+':
            result = a+b
        elif btn =='-':
            result = a-b 
        elif btn =='*':
            result = a*b
        elif btn =='/':
            result = a/b           
        return render(request,'Basics/Calculator.html',{'result':result})
    else:
        return render(request,'Basics/Calculator.html')


def largestsmallest(request):
    if request.method=='POST':
        a=int(request.POST.get('txt_num1'))
        b=int(request.POST.get('txt_num2'))
        c=int(request.POST.get('txt_num3'))
        btn=request.POST.get('btn_check')
        if a > b and a > c:
            largest = a
        elif b > c:
            largest = b
        else:
            largest = c
        if a < b and a < c:
            smallest = a
        elif b < c:
            smallest = b
        else:
            smallest = c

        return render(request,'Basics/Largest&Smallest.html',{'largest':largest,'smallest':smallest})
    else:
        return render(request,'Basics/Largest&Smallest.html')
def marklist(request):
    if request.method=='POST':
        fname=request.POST.get('txt_fname')
        lname=request.POST.get('txt_lname')
        dept=request.POST.get('txt_dept')
        gender=request.POST.get('txt_gender')
        m1=int(request.POST.get('txt_mark1'))
        m2=int(request.POST.get('txt_mark2'))
        m3=int(request.POST.get('txt_mark3'))
       
        total=m1+m2+m3
        percentage=total/3
        if percentage>=90:
            grade="A"
        elif percentage >= 75:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "D"
        if gender=="Male":
            fname= f"Mr. {fname}"
        else:
            fname=f"Ms. {fname}"

        return render(request,'Basics/Marklist.html',{'fname':fname,'lname':lname,'dept':dept,'total':total,'percentage':percentage,'grade':grade})
    else:
        return render(request,'Basics/Marklist.html')

def userreg(request):
    district = tbl_district.objects.all()
    place = tbl_place.objects.all()
    userdata = tbl_ano.objects.all()
    
    if request.method == 'POST':
        email = request.POST.get('txt_email')
        emailcount = tbl_ano.objects.filter(user_email=email).count()
        
        if emailcount >= 1:
            return render(request, 'Basics/Userregistration.html', {
                'district': district,
                'msg1': "Email Already Exists"
            })
        else:    
            name = request.POST.get('txt_name')
            contact = request.POST.get('txt_contact')
            address = request.POST.get('txt_address')
            photo = request.FILES.get('photo')
            password = request.POST.get('txt_password')
            retypepassword = request.POST.get('txt_repassword')
            placeid = tbl_place.objects.get(id=request.POST.get("selplace"))

            if password == retypepassword:
                tbl_ano.objects.create(
                    user_name=name,
                    place=placeid,
                    user_email=email,
                    user_contact=contact,
                    user_address=address,
                    user_password=password,
                    user_photo=photo
                )
                # Add a hidden input to indicate success for AJAX
                return render(request, 'Basics/Userregistration.html', {
                    'district': district,
                    'success': True,
                    'extra_content': '<input type="hidden" id="success-flag" value="true">'
                })
            else:
                return render(request, 'Basics/Userregistration.html', {
                    'district': district,
                    'msg': "Password Mismatch"
                })
    else:
        return render(request, 'Basics/Userregistration.html', {
            'district': district,
            'place': place,
            'userdata': userdata
        })

@csrf_exempt
def check_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        exists = tbl_ano.objects.filter(user_email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)
  