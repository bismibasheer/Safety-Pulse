from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Administrator.models import *
from Guest.models import *
from User.models import *
from MVD.models import *
import time


# Create your views here.

def index(request):
    ar=[1,2,3,4,5]
    parry=[]
    avg=0
    tot=0
    ratecount=tbl_rating.objects.all().count()
    if ratecount>0:
        ratedata=tbl_rating.objects.all()
        for j in ratedata:
            tot=tot+j.rating_data
            avg=tot//ratecount
            #print(avg)
        parry.append(avg)
    else:
        parry.append(0)
    # print(parry)
    return render(request,'Guest/index.html',{'datas':parry,'ar':ar})

    
def UserRegister(request):
    District = tbl_district.objects.all()
    if request.method == 'POST':
        useremail = request.POST.get("txt_email")
        emailcount = tbl_User.objects.filter(user_email=useremail).count()
        
        if emailcount >= 1:
            return render(request, 'Guest/UserRegistration.html', {
                'District': District,
                'msg1': "Email Already Exists"
            })
        else:
            username = request.POST.get("txt_name")
            usercontact = request.POST.get("txt_con")
            useraddress = request.POST.get("txt_address")
            userpwd = request.POST.get("txt_pass")
            userrepwd = request.POST.get("txt_repass")
            userphoto = request.FILES.get('txt_file')
            userproof = request.FILES.get('txt_proof')
            plceid = tbl_place.objects.get(id=request.POST.get("sel_place"))
            
            if userpwd == userrepwd:
                tbl_User.objects.create(
                    user_name=username,
                    user_email=useremail,
                    user_contact=usercontact,
                    user_address=useraddress,
                    user_password=userpwd,
                    user_photo=userphoto,
                    place=plceid,
                    user_proof=userproof
                )
                return render(request, 'Guest/UserRegistration.html', {
                    'District': District,
                    'success': True
                })
            else:
                return render(request, 'Guest/UserRegistration.html', {
                    'District': District,
                    'msg': "Password mismatch"
                })    
    return render(request, 'Guest/UserRegistration.html', {'District': District})



@csrf_exempt
def check_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        exists = tbl_User.objects.filter(user_email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)   

def ajaxplace(request):
    place=tbl_place.objects.filter(district=request.GET.get('did'))
    return render(request,'Guest/Ajaxplace.html',{'place':place})

def login(request):
    if request.method=='POST':
        admincount=tbl_admin.objects.filter(admin_email=request.POST.get('txt_email'),admin_password=request.POST.get('txt_pass')).count()
        userlogin=tbl_User.objects.filter(user_email=request.POST.get('txt_email'),user_password=request.POST.get('txt_pass')).count()
        mvdcount=tbl_Mvd.objects.filter(mvd_email=request.POST.get('txt_email'),mvd_password=request.POST.get('txt_pass')).count()
        subcount=tbl_subadmin.objects.filter(subadmin_email=request.POST.get('txt_email'),subadmin_password=request.POST.get('txt_pass')).count()
        rtocount=tbl_rto.objects.filter(rto_email=request.POST.get('txt_email'),rto_password=request.POST.get('txt_pass')).count()

        if admincount>0:
            admin=tbl_admin.objects.get(admin_email=request.POST.get('txt_email'),admin_password=request.POST.get('txt_pass'))
            request.session['aid']=admin.id
            return redirect('Admin:AdminHome')
            
        elif userlogin>0:
            user=tbl_User.objects.get(user_email=request.POST.get('txt_email'),user_password=request.POST.get('txt_pass'))
            if user.user_status==1:
                request.session['uid']=user.id
                return redirect('User:UserHome')
            elif user.user_status==2:
                return render(request,'Guest/Login.html',{'msg':'Rejected'})
            else:
                return render(request,'Guest/Login.html',{'msg':'Pending'})     


        elif subcount>0:
            Subadmin=tbl_subadmin.objects.get(subadmin_email=request.POST.get('txt_email'),subadmin_password=request.POST.get('txt_pass'))
            request.session['sid']=Subadmin.id
            request.session['districtid']=Subadmin.district.id
            return redirect('Subadmin:SubadminHome')
            
        
        elif mvdcount>0:
            mvd=tbl_Mvd.objects.get(mvd_email=request.POST.get('txt_email'),mvd_password=request.POST.get('txt_pass'))
            if mvd.mvd_status==1:
                request.session['mid']=mvd.id
                return redirect('MVD:MVDHome')
            elif mvd.mvd_status==2:
                return render(request,'Guest/Login.html',{'msg':'Rejected'})
            else:
                return render(request,'Guest/Login.html',{'msg':'Pending'})

        elif rtocount>0:
            RTO=tbl_rto.objects.get(rto_email=request.POST.get('txt_email'),rto_password=request.POST.get('txt_pass'))
            if RTO.rto_status==1:
                request.session['rid']=RTO.id
                return redirect('RTO:RTOHome')
            elif RTO.rto_status==2:
                return render(request,'Guest/Login.html',{'msg':'Rejected'})
            else:
                return render(request,'Guest/Login.html',{'msg':'Pending'})        

            
        else:
            return render(request,'Guest/Login.html',{'msg':'invalid'})
    else:
        return render(request,'Guest/Login.html')

def mvdregistration(request):
    District = tbl_district.objects.all()
    if request.method == 'POST':
        mvdemail = request.POST.get("txt_email")
        emailcount = tbl_Mvd.objects.filter(mvd_email=mvdemail).count()
        
        if emailcount >= 1:
            return render(request, 'Guest/MVD.html', {
                'District': District,
                'msg1': "Email Already Exists"
            })
        else:
            mvdname = request.POST.get("txt_name")
            mvdcontact = request.POST.get("txt_contact")
            mvdaddress = request.POST.get("txt_address")
            mvdpwd = request.POST.get("txt_pwd")
            remvdpwd = request.POST.get("txt_repass")
            mvdphoto = request.FILES.get('txt_file')
            mvdproof = request.FILES.get('txt_proof')
            plceid = tbl_place.objects.get(id=request.POST.get("sel_place"))
            
            if mvdpwd == remvdpwd:
                tbl_Mvd.objects.create(
                    mvd_name=mvdname,
                    mvd_email=mvdemail,
                    mvd_contact=mvdcontact,
                    mvd_address=mvdaddress,
                    mvd_password=mvdpwd,
                    mvd_photo=mvdphoto,
                    mvd_proof=mvdproof,
                    place=plceid
                )
                return render(request, 'Guest/MVD.html', {
                    'District': District,
                    'success': True
                })
            else:
                return render(request, 'Guest/MVD.html', {
                    'District': District,
                    'msg': "Password mismatch"
                })
    return render(request, 'Guest/MVD.html', {'District': District})

@csrf_exempt
def check_mvd_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        exists = tbl_Mvd.objects.filter(mvd_email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def GuestHome(request):
    return render(request,'Guest/GuestHome.html')   

def RtoRegister(request):
    District = tbl_district.objects.all()
    if request.method == 'POST':
        rtoemail = request.POST.get("txt_email")
        emailcount = tbl_rto.objects.filter(rto_email=rtoemail).count()
        
        if emailcount >= 1:
            return render(request, 'Guest/RTORegistration.html', {
                'District': District,
                'msg1': "Email Already Exists"
            })
        else:
            rtoname = request.POST.get("txt_name")
            rtocontact = request.POST.get("txt_con")
            rtoaddress = request.POST.get("txt_address")
            rtopwd = request.POST.get("txt_pass")
            rtorepwd = request.POST.get("txt_repass")
            rtophoto = request.FILES.get('txt_file')
            rtoproof = request.FILES.get('txt_proof')
            plceid = tbl_place.objects.get(id=request.POST.get("sel_place"))
            
            if rtopwd == rtorepwd:
                tbl_rto.objects.create(
                    rto_name=rtoname,
                    rto_email=rtoemail,
                    rto_contact=rtocontact,
                    rto_address=rtoaddress,
                    rto_password=rtopwd,
                    rto_photo=rtophoto,
                    place=plceid,
                    rto_proof=rtoproof
                )
                return render(request, 'Guest/RTORegistration.html', {
                    'District': District,
                    'success': True
                })
            else:
                return render(request, 'Guest/RTORegistration.html', {
                    'District': District,
                    'msg': "Password mismatch"
                })
    return render(request, 'Guest/RTORegistration.html', {'District': District})

@csrf_exempt
def check_rto_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        exists = tbl_rto.objects.filter(rto_email=email).exists()
        return JsonResponse({'exists': exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)

              
  


