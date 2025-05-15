from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from User.models import *
from RTO.models import *
from django.http import JsonResponse
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage


def UserHome(request):
    if "uid" in request.session: 
        return render(request,'User/UserHome.html')
    else:
        return redirect("Guest:login")

def Myprofile(request):
    user=tbl_User.objects.get(id=request.session["uid"])
    return render(request,'User/MyProfile.html',{"user":user})

def Editprofile(request):
    user = tbl_User.objects.get(id=request.session["uid"])
    if request.method == "POST":
        user.user_name = request.POST.get('txt_name')
        user.user_email = request.POST.get('txt_email')
        user.user_contact = request.POST.get('txt_con')
        user.user_address = request.POST.get('txt-add')
        if request.FILES.get('profile_photo'):
            user.user_photo = request.FILES.get('profile_photo')
        user.save()
        return render(request, 'User/EditProfile.html', {"user": user, "msg": "Profile updated successfully!"})
    else:
        return render(request, 'User/EditProfile.html', {"user": user})

from django.shortcuts import render, redirect
from User.models import tbl_User

def Changepassword(request):
    user = tbl_User.objects.get(id=request.session["uid"])
    dbpass = user.user_password

    if request.method == "POST":
        oldpassword = request.POST.get('txt_old')
        newpassword = request.POST.get('txt_new')
        retypepassword = request.POST.get('txt_conf')

        if oldpassword == dbpass:
            if newpassword == retypepassword:
                user.user_password = newpassword
                user.save()
                return render(request, 'User/MyProfile.html', {'msg': 'Password Changed Successfully'})
            else:
                return render(request, 'User/Changepassword.html', {'msg': 'New passwords do not match'})
        else:
            return render(request, 'User/Changepassword.html', {'msg': 'Incorrect current password'})
    
    return render(request, 'User/Changepassword.html')


def postcomplaint(request,id):
    Category=tbl_category.objects.all()
    user=tbl_User.objects.get(id=request.session["uid"])
    complaint=tbl_Complaint.objects.filter(User=user,complaint_status=0)
    MVD=tbl_Mvd.objects.get(id=id)
    if request.method=='POST':
        description=request.POST.get("txt_com")
        file=request.FILES.get("txt_file")
        category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        tbl_Complaint.objects.create(complaint_description=description,complaint_photo=file,vehicle_number=tbl_Vehicledetails.objects.get(vehicle_number=request.POST.get("txt_vehicle")),User=user,MVD=MVD,Category=category)
        # return redirect('User:postcomplaint',id)
        return render(request,'User/PostComplaint.html',{'id':id,'msg': 'Successfully post complaint'})
    else:
        return render(request,'User/PostComplaint.html',{'user':user,'complaint':complaint,'MVD':MVD,'Category':Category})


        

def ajaxchecknumber(request):
    detailscount = tbl_Vehicledetails.objects.filter(vehicle_number=request.GET.get("did")).count()
    if detailscount == 0:
        return JsonResponse({"msg":"The Vehicle Number Is Incorrect..","status":True})
    else:
        return JsonResponse({"msg":"The Vehicle Number Is Valid..","status":False})


def mvdlist(request):
    if "uid" in request.session:

        District=tbl_district.objects.all()
        mvd=tbl_Mvd.objects.filter(mvd_status=1)
        return render(request,'User/ViewMVD.html',{'mvd':mvd,'District':District})
    else:
        return redirect("Guest:login")     

def ajaxsearch(request):
    if (request.GET.get("did")!="") and (request.GET.get("pid") !=""):
        mvd=tbl_Mvd.objects.filter(mvd_status=1,place=request.GET.get("pid"))
    elif (request.GET.get("did")!="")  :  
        mvd=tbl_Mvd.objects.filter(mvd_status=1,place__district=request.GET.get("did"))
    return render(request,'User/AjaxSearch.html',{'mvd':mvd})

def feedback(request):
    if "uid" in request.session:
        feedback=tbl_Feedback.objects.all()
        user=tbl_User.objects.get(id=request.session["uid"])
        if request.method=='POST':
            content=request.POST.get("txt_content")
            tbl_Feedback.objects.create(feedback_content=content,User=user)
            return redirect('User:feedback')
        else:    
            return render(request,'User/Feedback.html',{'feedback':feedback,'user':user})
    else:
        return redirect("Guest:login")        

def repliedcomplaint(request):
    user=tbl_User.objects.get(id=request.session["uid"])
    # MVD=tbl_Mvd.objects.get(id=request.session["mid"])
    complaint=tbl_Complaint.objects.filter(User=user)
    if request.method=='POST':
        return redirect('User:repliedcomplaint')
    else:
        return render(request,'User/RepliedComplaint.html',{'user':user,'complaint':complaint})   


def contentlist(request):
    if "uid" in request.session:
        articles=tbl_Article.objects.all()
        videos=tbl_Video.objects.all()
        return render(request,'User/Viewcontent.html',{'articles':articles,'videos':videos})
    else:
        return redirect("Guest:login")     

def searchdetails(request):
    if "uid" in request.session:
        vehicle=tbl_Vehicledetails.objects.all()
        complaint_vehicles = tbl_Complaint.objects.values_list('vehicle_number', flat=True)  
        matched_vehicles = vehicle.filter(vehicle_number__in=complaint_vehicles)
        return render(request,'User/Searchvehicle.html',{'vehicle':vehicle})
    else:
        return redirect("Guest:login")     

def ajaxsearchvehicle(request):
    name=request.GET.get("name")
    complaintvehicles=tbl_Complaint.objects.filter(vehicle_number__vehicle_number__istartswith=name,complaint_payment=1)
    if complaintvehicles.exists():
        return render(request, "User/Ajaxnumber.html", {'data': complaintvehicles})
    else:
        return render(request, "User/Ajaxnumber.html", {'data': None}) 

def logout(request):
    del request.session["uid"]
    return redirect("Guest:login")          



def rating(request):
    parray=[1,2,3,4,5]
    counts=0
    counts=stardata=tbl_rating.objects.all().count()
    if counts>0:
        res=0
        stardata=tbl_rating.objects.all().order_by('-datetime')
        for i in stardata:
            res=res+i.rating_data
        avg=res//counts
        return render(request,"User/Rating.html",{'data':stardata,'ar':parray,'avg':avg,'count':counts})
    else:
         return render(request,"User/Rating.html")

def ajaxstar(request):
    parray=[1,2,3,4,5]
    rating_data=request.GET.get('rating_data')
    user=tbl_User.objects.get(id=request.session['uid'])
    user_review=request.GET.get('user_review')
    tbl_rating.objects.create(user=user,user_review=user_review,rating_data=rating_data)
    stardata=tbl_rating.objects.all().order_by('-datetime')
    return render(request,"User/AjaxRating.html",{'data':stardata,'ar':parray})

def starrating(request):
    r_len = 0
    five = four = three = two = one = 0
    rate = tbl_rating.objects.all()
    ratecount = tbl_rating.objects.all().count()
    for i in rate:
        if int(i.rating_data) == 5:
            five = five + 1
        elif int(i.rating_data) == 4:
            four = four + 1
        elif int(i.rating_data) == 3:
            three = three + 1
        elif int(i.rating_data) == 2:
            two = two + 1
        elif int(i.rating_data) == 1:
            one = one + 1
        else:
            five = four = three = two = one = 0
    result = {"five":five,"four":four,"three":three,"two":two,"one":one,"total_review":ratecount}
    return JsonResponse(result)

def get_available_points(user):
    points = tbl_points.objects.filter(user=user).aggregate(
        total_credited=Sum('point_credited'), 
        total_withdrawed=Sum('point_widthdrawed')
    )
    credited = points['total_credited'] or 0
    withdrawed = points['total_withdrawed'] or 0
    available = credited - withdrawed
    return available

def payment(request, id):
    user = tbl_User.objects.get(id=request.session['uid'])
    com = tbl_Complaint.objects.get(id=id)
    amount = int(com.complaint_amount)
    rate = (amount * 20) / 100

    available_points = get_available_points(user)

    if request.method == "POST":
        redeem = request.POST.get('redeem')  # 'on' if checked

        final_amount = amount  # Default

        if redeem == "on" and available_points > 0:
            # How much the user can redeem
            if available_points >= amount:
                redeem_points = amount
            else:
                redeem_points = available_points

            final_amount = amount - redeem_points

            # Insert redeem points ONLY into point_widthdrawed (withdrawed points)
            tbl_points.objects.create(point_widthdrawed=redeem_points, user=user)

        # Update complaint status as paid
        com.complaint_payment = 2
        com.save()

        # Now, credit new points (only from what user actually paid)
        if final_amount > 0:
            # Only credit points for the final paid amount (after redemption)
            new_rate = (final_amount * 20) / 100
            tbl_points.objects.create(point_credited=new_rate, user=user)

        return redirect("User:loader")

    else:
        return render(request, "User/Payment.html", {"amount": amount, "available": available_points})


def Mypoints(request):
    # Fetch points history for the logged-in user
    points_history = tbl_points.objects.filter(user=request.session['uid']).order_by('point_date')

    # Calculate available points
    total_credited = sum(item.point_credited for item in points_history)
    total_withdrawn = sum(item.point_widthdrawed for item in points_history)
    available_points = total_credited - total_withdrawn

    context = {
        'points_history': points_history,
        'available_points': available_points,
    }
    return render(request,"User/Mypoints.html", context)

def Withdrawpoints(request):
    user_id = request.session['uid']
    points_history = tbl_points.objects.filter(user=user_id)

    total_credited = sum(item.point_credited for item in points_history)
    total_withdrawn = sum(item.point_widthdrawed for item in points_history)
    available_points = total_credited - total_withdrawn

    if request.method == "POST":
        amount = int(request.POST.get('amount'))
        upi = request.POST.get('upi')

        if amount > available_points:
            # Error: Trying to withdraw more than available
            context = {
                'available_points': available_points,
                'error': 'Withdrawal amount exceeds available points.'
            }
            return render(request, "User/Withdrawpoints.html", context)
        else:
            # Save the withdrawal request (you can create a withdrawal table if needed)
            # For now, deduct points directly:
            tbl_points.objects.create(
                user_id=user_id,
                point_widthdrawed=amount,
            )
            return redirect('User:Mypoints')

    context = {
        'available_points': available_points
    }
    return render(request, "User/Withdrawpoints.html", context)


def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Paymentsuc.html")

def track(request, id):
    complaint = tbl_Complaint.objects.get(id=id)
    return render(request,"User/Track.html",{"complaint":complaint})

def viewchellan(request, id):
    com = tbl_Complaint.objects.get(id=id)
    return render(request,"User/ViewChellan.html",{"complaint":com})

def get_comp_count(request):
    compcount=tbl_Complaint.objects.filter(User=request.session['uid'],complaint_status=1).count()
    return JsonResponse({'compcount': compcount})