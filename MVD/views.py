from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from User.models import *
from Subadmin.models import *
from MVD.models import *
from RTO.models import *
from datetime import date
from django.db.models import Count
from django.http import JsonResponse
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.db.models import Avg

def get_comp_count(request):
    if "mid" in request.session:
        compcount=tbl_Complaint.objects.filter(MVD=request.session['mid'],complaint_status=0).count()
        return JsonResponse({'compcount': compcount})
    return JsonResponse({'compcount': 0})   

def get_violation_count(request):
    if "mid" in request.session:
        compcount=tbl_Complaint.objects.filter(MVD=request.session['mid'],complaint_status=0).count()
        print(compcount)
        return JsonResponse({'compcount': compcount})
    return JsonResponse({'compcount': 0})   
    
def MVDHome(request):
    if "mid" in request.session:
        compcount=tbl_Complaint.objects.filter(MVD=request.session['mid'],complaint_status=0).count()
        print(compcount)
        return render(request,'MVD/MVDHome.html')
    else:
        return redirect("Guest:login") 

def Myprofile(request):
    MVD=tbl_Mvd.objects.get(id=request.session["mid"])
    return render(request,'MVD/MyProfile.html',{"MVD":MVD}) 

def Editprofile(request):
    MVD=tbl_Mvd.objects.get(id=request.session["mid"])
    if request.method=="POST":
         MVD.mvd_name=request.POST.get('txt_name')
         MVD.mvd_email=request.POST.get('txt_email')
         MVD.mvd_contact=request.POST.get('txt_con')
         MVD.mvd_address=request.POST.get('txt-add')
         if request.FILES.get('profile_photo'):
            MVD.mvd_photo = request.FILES.get('profile_photo')
         MVD.save()
         return render(request, 'MVD/MyProfile.html', {"MVD": MVD, "msg": "Profile updated successfully!"})
    else:
        return render(request,'MVD/EditProfile.html',{"MVD":MVD,})

def Changepassword(request):
    MVD = tbl_Mvd.objects.get(id=request.session["mid"])
    dbpass = MVD.mvd_password

    if request.method == "POST":
        oldpassword = request.POST.get('txt_old')
        newpassword = request.POST.get('txt_new')
        retypepassword = request.POST.get('txt_conf')

        if oldpassword == dbpass:
            if newpassword == retypepassword:
                MVD.mvd_password = newpassword
                MVD.save()
                return render(request, 'MVD/MyProfile.html', {'msg': 'Password Changed Successfully'})
            else:
                return render(request, 'MVD/Changepassword.html', {'msg': 'New passwords do not match'})
        else:
            return render(request, 'MVD/Changepassword.html', {'msg': 'Incorrect current password'})

    return render(request, 'MVD/Changepassword.html')


def Viewcomplaints(request):
    if "mid" in request.session:
        complaint=tbl_Complaint.objects.filter(complaint_status=0,MVD=request.session['mid'])
        replycom=tbl_Complaint.objects.filter(complaint_status=1,MVD=request.session['mid'])
        if request.method=='POST':
            return redirect('MVD:Viewcomplaints')
        else:
            return render(request,'MVD/ViewComplaintRequest.html',{"complaint":complaint,"Reply":replycom})
    else:
        return redirect("Guest:login")        

def replycomplaint(request,complaint_id):
    complaint=tbl_Complaint.objects.get(id=complaint_id)
    # user=tbl_User.objects.get(id=request.session['uid'])
    if request.method=='POST':
        complaint.reply_complaint=request.POST.get('txt_reply')
        complaint.complaint_status=1
        complaint.save()
        return redirect('MVD:Viewcomplaints')
    else:
        return render(request,'MVD/Reply.html',{"complaint":complaint})   

def repliedcomplaint(request):
    if "mid" in request.session:
        complaint=tbl_Complaint.objects.filter(complaint_status=0,MVD=request.session['mid'])
        replycom=tbl_Complaint.objects.filter(complaint_status__gt=0,MVD=request.session['mid'])
        if request.method=='POST':

            return redirect('MVD:repliedcomplaint')
        else:
            return render(request,'MVD/RepliedComplaintRequest.html',{"complaint":complaint,"Reply":replycom})
    else:
        return redirect("Guest:login")                     

def ajaxupdateamount(request):
    complaint = tbl_Complaint.objects.get(id=request.GET.get("id"))
    complaint.complaint_amount = request.GET.get("amount")
    complaint.complaint_status = 2
    complaint.save()
    return JsonResponse({"msg":"Amount Updated Sucessfully..."})

def generatechellan(request, id):
    com = tbl_Complaint.objects.get(id=id)
    com.complaint_payment = 1
    com.save()
    return redirect("MVD:repliedcomplaint")

def rtolist(request, id):
    if "mid" in request.session:
        District=tbl_district.objects.all()
        RTO=tbl_rto.objects.filter(rto_status=1)
        return render(request,'MVD/RTOList.html',{'RTO':RTO,'District':District,"id":id}) 
    else:
        return redirect("Guest:login")    

def ajaxsearchrto(request):
    if (request.GET.get("did")!="") and (request.GET.get("pid") !=""):
        RTO=tbl_rto.objects.filter(rto_status=1,place=request.GET.get("pid"))
    elif (request.GET.get("did")!="")  :  
        RTO=tbl_rto.objects.filter(rto_status=1,place__district=request.GET.get("did"))
    return render(request,'MVD/AjaxSearchrto.html',{'RTO':RTO,"id":request.GET.get("id")})


def requestsend(request,id,vid):
    MVD=tbl_Mvd.objects.get(id=request.session["mid"])
    if request.method == "POST":
        # file=request.FILES.get("txt_file")
        description=request.POST.get("txt_des")
        tbl_Request.objects.create(
            # request_file=file,
            request_description=description,
            RTO=tbl_rto.objects.get(id=id),
            MVD=MVD,
            Vehicle=tbl_Vehicledetails.objects.get(id=vid))
        comp = tbl_Complaint.objects.filter(vehicle_number=vid,complaint_status=2,MVD=MVD)
        for i in comp:
            c = tbl_Complaint.objects.get(id=i.id)
            c.complaint_status=3
            c.save()
            tbl_multipleviolation.objects.create(complaint=c)
        return render(request,'MVD/Request.html',{"msg":"Request Send Sucessfully"}) 
    else:
        return render(request,'MVD/Request.html')  


def vehiclelist(request):
    if "mid" in request.session:
        vehicle=tbl_Vehicledetails.objects.all()
        return render(request,'MVD/VehicleList.html',{'vehicle':vehicle})
    else:
        return redirect("Guest:login")     

def ajaxsearchnumber(request):
    name=request.GET.get("name")
    vehicle=tbl_Vehicledetails.objects.filter(vehicle_number__istartswith=name)
    return render(request,"MVD/AjaxVehicleList.html",{'data':vehicle})

def multiple_violations(request):
    # Get all vehicles
    vehicle = tbl_Vehicledetails.objects.all()
    cmp = []
    
    # Identify vehicles with more than 3 complaints with complaint_status=2
    for i in vehicle:
        repeat = tbl_Complaint.objects.filter(vehicle_number=i.id, complaint_status=2,MVD=request.session['mid']).count()
        if repeat > 3:
            cmp.append(i.id)
    
    # Get the filtered vehicle data
    vehicledata = tbl_Vehicledetails.objects.filter(id__in=cmp)
    
    # Prepare data with filtered complaints
    vehicle_data_with_complaints = []
    for vehicle in vehicledata:
        # Filter complaints with complaint_status <= 2
        complaints = tbl_Complaint.objects.filter(vehicle_number=vehicle.id, complaint_status__lte=2,MVD=request.session['mid'])
        vehicle_data_with_complaints.append({
            'vehicle': vehicle,
            'complaints': complaints
        })

    # req=tbl_Request.objects.filter(MVD=request.session["mid"],request_status=1)
    # for i in req:
    #     for j in i.Vehicle.tbl_Complaint.set.all():
    #         if j.complaint_status == 3:
    #             verfiedlist +=1
    #         else:
    #             verifiedlist=0
    # print(verifiedlist)


    
    
    return render(request, "MVD/MultipleViolations.html", {"data": vehicle_data_with_complaints})

    

def logout(request):
    del request.session["mid"]
    return redirect("Guest:login")    

def resolvedcomplaint(request):
    if "mid" in request.session:
        req=tbl_Request.objects.filter(MVD=request.session["mid"],request_status=1)     
        return render(request,"MVD/ResolvedViolation.html",{"req":req})
    else:
        return redirect("Guest:login") 

def viewchellan(request, id):
    com = tbl_Complaint.objects.get(id=id)
    return render(request,"MVD/ViewChellan.html",{"complaint":com})


def report(request):
    # Get distinct years and months from complaints
    data=tbl_Mvd.objects.get(id=request.session['mid'])
    placeid=data.place.id
    

    all_complaints = tbl_Complaint.objects.filter(MVD=request.session['mid']).order_by('complaint_date')
    
    # Generate years from 2024 onwards up to current year
    current_year = datetime.now().year
    years = list(range(2024, current_year + 1))
    
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    selected_year = request.GET.get('year')
    selected_month = request.GET.get('month')
    
    # Filter complaints based on selection
    if selected_year and selected_month:
        complaints = all_complaints.filter(
            complaint_date__year=selected_year,
            complaint_date__month=selected_month,
            User__place__id=placeid
        )
    elif selected_year:
        complaints = all_complaints.filter(complaint_date__year=selected_year,User__place__id=placeid)
    else:
        complaints = all_complaints
    
    # Generate report data
    report_data = {}
    for complaint in complaints:
        month_year = complaint.complaint_date.strftime("%B %Y")
        
        if month_year not in report_data:
            report_data[month_year] = {
                'total_complaints': 0,
                'solved_complaints': 0,
                'pending_complaints': 0,
                'payment_pending': 0
            }
        
        report_data[month_year]['total_complaints'] += 1
        
        if complaint.complaint_status == 1:
            report_data[month_year]['solved_complaints'] += 1
        else:
            report_data[month_year]['pending_complaints'] += 1
            
        if complaint.complaint_payment == 0:
            report_data[month_year]['payment_pending'] += 1
    
    # Calculate resolution rate
    for month, data in report_data.items():
        data['resolution_rate'] = (data['solved_complaints'] / data['total_complaints']) * 100 if data['total_complaints'] > 0 else 0
    
    # Sort the report data
    sorted_report = sorted(
        [(month, data) for month, data in report_data.items()],
        key=lambda x: datetime.strptime(x[0], "%B %Y")
    )
    
    context = {
        'report_data': sorted_report,   
        'title': 'Monthly Complaint Report',
        'years': years,
        'months': months,
        'selected_year': int(selected_year) if selected_year else '',
        'selected_month': int(selected_month) if selected_month else '',
    }
    
    return render(request, 'MVD/Report.html', context)
