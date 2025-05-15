from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from User.models import *
from Subadmin.models import *
from MVD.models import *
from RTO.models import *
from datetime import date



def RTOHome(request):
    if "rid" in request.session:
        return render(request,'RTO/RTOHome.html')
    else:
        return redirect("Guest:login") 

def Myprofile(request):
    RTO=tbl_rto.objects.get(id=request.session["rid"])
    return render(request,'RTO/MyProfile.html',{"RTO":RTO}) 

from django.shortcuts import render, redirect
from .models import tbl_rto  # Assuming tbl_rto is your model

def Editprofile(request):
    RTO = tbl_rto.objects.get(id=request.session["rid"])
    if request.method == "POST":
        RTO.rto_name = request.POST.get('txt_name')
        RTO.rto_email = request.POST.get('txt_email')
        RTO.rto_contact = request.POST.get('txt_con')
        RTO.rto_address = request.POST.get('txt_add')  # Fixed typo
        if request.FILES.get('txt_file'):
            RTO.rto_photo = request.FILES.get('txt_file')
        RTO.save()  # Save all changes
        return render(request,'RTO/MyProfile.html',{'msg':'Profile Updated Successfully'}) 

    return render(request, 'RTO/EditProfile.html', {"RTO": RTO})

def Changepassword(request):
    RTO=tbl_rto.objects.get(id=request.session["rid"])
    dbpass=RTO.rto_password
    if request.method=="POST":
        oldpassword=request.POST.get('txt_old')
        newpassword=request.POST.get('txt_new')
        retypepassword=request.POST.get('txt_conf')
        if oldpassword==dbpass:
            if newpassword==retypepassword:
                RTO.rto_password=newpassword
                RTO.save()
                return render(request,'RTO/MyProfile.html',{'msg':'Password Changed Successfully'}) 
            else:
                return render(request,'RTO/Changepassword.html',{'msg':'New passwords do not match'}) 
        else:
            return render(request,'RTO/Changepassword.html',{'msg':'Incorrect current password'}) 
    else:
        return render(request,'RTO/Changepassword.html')   


def addvideo(request):
    RTO=tbl_rto.objects.get(id=request.session["rid"])
    videos=tbl_Video.objects.filter(RTO=RTO)
    if request.method=="POST":
        videofile=request.FILES.get('txt_file')
        videodescription=request.POST.get("txt_des")
        tbl_Video.objects.create(video_file=videofile,video_description=videodescription,RTO=RTO)
        return redirect('RTO:addvideo')
    else:
        return render(request,'RTO/AddVideo.html',{'RTO':RTO,'videos':videos})

def videodelete(request,did):
    tbl_Video.objects.get(id=did).delete()
    return redirect('RTO:addvideo')

def addarticle(request):
    RTO=tbl_rto.objects.get(id=request.session["rid"])
    articles=tbl_Article.objects.filter(RTO=RTO)
    if request.method=="POST":
        articlefile=request.FILES.get('txt_file')
        articledescription=request.POST.get("txt_des")
        tbl_Article.objects.create(article_file=articlefile,article_description=articledescription,RTO=RTO)
        return redirect('RTO:addarticle')
    else:
        return render(request,'RTO/AddArticle.html',{'RTO':RTO,'articles':articles}) 

def deletearticle(request,did):
    tbl_Article.objects.get(id=did).delete()
    return redirect('RTO:addarticle')  


def vehicledetails(request):
    RTO=tbl_rto.objects.get(id=request.session["rid"])
    vehicle=tbl_Vehicledetails.objects.filter(RTO=RTO)
    if request.method=="POST":
        vehicleuser=request.POST.get('txt_user')
        vehiclenumber=request.POST.get("txt_vehicle")
        tbl_Vehicledetails.objects.create(vehicleuser_name=vehicleuser,vehicle_number=vehiclenumber,RTO=RTO)
        return redirect('RTO:vehicledetails')
    else:
        return render(request,'RTO/VehicleDetails.html',{'RTO':RTO,'vehicle':vehicle})  


def deletevehicles(request,vehicle_id):
    tbl_Vehicledetails.objects.get(id=vehicle_id).delete()
    return redirect('RTO:vehicledetails')

def editvehicles(request,vehicle_id):
    vehicles=tbl_Vehicledetails.objects.get(id=vehicle_id)
    if request.method=="POST":
        vehicles.vehicleuser_name=request.POST.get('txt_user')
        vehicles.vehicle_number=request.POST.get('txt_vehicle')
        vehicles.save()
        return redirect('RTO:vehicledetails')
    else:
        return render(request,'RTO/VehicleDetails.html',{'vehicles':vehicles})

def Viewrequest(request):
    if "rid" in request.session:
        req=tbl_Request.objects.filter(RTO=request.session["rid"],request_status=0)
        return render(request,'RTO/Viewrequest.html',{'req':req})
    else:
        return redirect("Guest:login")

def resolvedrequest(request):
    if "rid" in request.session:
        req=tbl_Request.objects.filter(RTO=request.session["rid"],request_status=1)
        return render(request,'RTO/ResolvedViolation.html',{'req':req})
    else:
        return redirect("Guest:login")                

def logout(request):
    del request.session["rid"]
    return redirect("Guest:login")                                         

def verifymultiplerequest(request, id):
    req = tbl_Request.objects.get(id=id)
    req.request_status = 1
    req.save()
    return redirect("RTO:Viewrequest")

def get_comp_count(request):
    compcount=tbl_Complaint.objects.filter(User=request.session['uid'],complaint_status=1).count()
    print(compcount)
    return JsonResponse({'compcount': compcount})