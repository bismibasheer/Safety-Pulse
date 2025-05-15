from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from User.models import *
from Subadmin.models import *
from Administrator import *
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
from django.db.models import Avg


def SubadminHome(request):
    if "sid" in request.session:

        Subadmin=tbl_subadmin.objects.get(id=request.session['sid'])
        distid=Subadmin.district.id

        total_solved = tbl_Complaint.objects.filter(complaint_status__in=[1, 3]).count()
        total_pending = tbl_Complaint.objects.filter(complaint_status=0).count()
        total_complaint = tbl_Complaint.objects.all().count()
        totalusers=tbl_User.objects.filter(user_status=0).count()

        totalusers=tbl_User.objects.filter(place__district=distid).count()
        verifiedusers=tbl_User.objects.filter(user_status=1,place__district=distid).count()
        rejectedusers=tbl_User.objects.filter(user_status=2,place__district=distid).count()
        
        totalmvd=tbl_Mvd.objects.filter(place__district=distid).count()
        verifiedmvd=tbl_Mvd.objects.filter(mvd_status=1,place__district=distid).count()
        rejectedmvd=tbl_Mvd.objects.filter(mvd_status=2,place__district=distid).count()

        totalrto=tbl_rto.objects.filter(place__district=distid).count()
        verifiedrto=tbl_rto.objects.filter(rto_status=1,place__district=distid).count()
        rejectedrto=tbl_rto.objects.filter(rto_status=2,place__district=distid).count()

        #line data
        rating_monthly_data = (
            tbl_rating.objects
            .annotate(month=TruncMonth('datetime'))
            .values('month')
            .annotate(avg_rating=Avg('rating_data'))
            .order_by('month')
        )   
        # Format for template (e.g., "April 2025")
        formatted_rating_data = [
            {'month': entry['month'].strftime('%B %Y'), 'avg_rating': round(entry['avg_rating'], 2)}
            for entry in rating_monthly_data
        ]

        datalist=[
            {'label':'Total MVD','values':totalmvd},
            {'label':'Verified MVD','values':verifiedmvd},
            {'label':'Rejected MVD','values':rejectedmvd},

            {'label':'Total RTO','values':totalrto},
            {'label':'Verified RTO','values':verifiedrto},
            {'label':'Rejected RTO','values':rejectedrto},

            {'label':'Total User','values':totalusers},
            {'label':'Verified User','values':verifiedusers},
            {'label':'Rejected User','values':rejectedusers},
        ]

        # Group complaints by month
        month_wise_data = (
            tbl_Complaint.objects
            .annotate(month=TruncMonth('complaint_date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        

        # Format the data for the template (optional: format month as string)
        formatted_month_data = [
            {'month': month['month'].strftime('%B %Y'), 'count': month['count']}
            for month in month_wise_data
        ]
        users=[
            {'label':'Total Users','value':totalusers},
            {'label':'Verified Users','value':verifiedusers}
        ]

        data = [
            {'label': 'Solved Complaints', 'value': total_solved},
            {'label': 'Pending Complaints', 'value': total_pending},
        ]

        data2 = [
            {'label': item['month'], 'value': item['count']}
            for item in formatted_month_data
        ]


        return render(
            request,
            'Subadmin/SubadminHome.html',
            {'rating_data': formatted_rating_data,'data': data, 'month_data': formatted_month_data,'data2':data2,'users':users,'datalist':datalist}
        )
    else:
        return redirect("Guest:login")
    

def mvdlist(request):
    if "sid" in request.session:
        mvd=tbl_Mvd.objects.filter(mvd_status=0,place__district=request.session['districtid'])
        if request.method=='POST':
            return redirect('Subadmin:mvdlist')
        else:
            return render(request,'Subadmin/MVDList.html',{'mvd':mvd})
    else:
        return redirect("Guest:login")        


def mvdverification(request):
    if "sid" in request.session:
        mvd=tbl_Mvd.objects.filter(mvd_status=0,place__district=request.session['districtid'])
        accept=tbl_Mvd.objects.filter(mvd_status=1,place__district=request.session['districtid'])
        reject=tbl_Mvd.objects.filter(mvd_status=2,place__district=request.session['districtid'])
        return render(request,'Subadmin/MVDVerifications.html',{'mvd':mvd,'accept':accept,'reject':reject})
    else:
        return redirect("Guest:login")    

def accept(request,mid):
    mvd=tbl_Mvd.objects.get(id=mid)
    mvd.mvd_status=1
    email = mvd.mvd_email
    mvd_name = mvd.mvd_name  
    mvd.save()

    send_mail(
        'MVD Data Accepted',  # Subject
        f"\rDear {mvd_name},"
        "\r\n\nWe are pleased to inform you that your MVD (Modified/Verified Data) has been successfully accepted."
        "\r\n\nHere are your updated registration details:"
        f"\r\n\nName: {mvd_name}"  # Include the user's name
        f"\r\nEmail: {email}"  # Include the user's email
        "\r\n\nThank you for your cooperation in updating the necessary information."
        "\r\n\nIf you have any questions or concerns, feel free to contact us."
        "\r\n\nBest regards,"
        "\r\nSafety Pulse",  # Body content
        settings.EMAIL_HOST_USER,
        [email],  # Recipient email address
)


    

    return redirect('Subadmin:mvdverification')

def reject(request,mid):
    mvd=tbl_Mvd.objects.get(id=mid)
    mvd.mvd_status=2
    email = mvd.mvd_email
    mvd_name = mvd.mvd_name  
    mvd.save()

    send_mail(
        'MVD Data Rejected',  # Subject
        f"\rDear {mvd_name},"
        "\r\n\nWe regret to inform you that your MVD (Modified/Verified Data) submission has been rejected."
        "\r\n\nHere are your registration details:"
        f"\r\n\nName: {mvd_name}"  # Include the user's name
        f"\r\nEmail: {email}"  # Include the user's email
        "\r\n\nThe reason for rejection could be due to missing, incorrect, or insufficient information."
        "\r\n\nPlease review your submission and provide the necessary updates."
        "\r\n\nIf you have any questions or concerns, feel free to contact us."
        "\r\n\nBest regards,"
        "\r\nSafety Pulse",  # Body content
        settings.EMAIL_HOST_USER,
        [email],  # Recipient email address
)

    return redirect('Subadmin:mvdverification')   

def userlist(request):
    if "sid" in request.session:
        user=tbl_User.objects.filter(user_status=0,place__district=request.session['districtid'])
        if request.method=='POST':
            return redirect('Subadmin:userlist')
        else:
            return render(request,'Subadmin/UserList.html',{'user':user})
    else:
        return redirect("Guest:login")        



def userverification(request):
    if "sid" in request.session:
        user=tbl_User.objects.filter(user_status=0,place__district=request.session['districtid'])
        accept=tbl_User.objects.filter(user_status=1,place__district=request.session['districtid'])
        reject=tbl_User.objects.filter(user_status=2,place__district=request.session['districtid'])
        return render(request,'Subadmin/UserVerifications.html',{'user':user,'accept':accept,'reject':reject})
    else:
        return redirect("Guest:login")    

def useraccept(request, uid):
    user = tbl_User.objects.get(id=uid)
    user.user_status = 1  
    email = user.user_email
    user_name = user.user_name  
    user.save()

    send_mail(
        'User Registration Verified',  
        f"\rDear {user_name}," 
        "\r\n\nYour account has been successfully verified."
        "\r\n\nHere are your registration details:"
        f"\r\n\nName: {user_name}" 
        f"\r\nEmail: {email}"  
        "\r\n\nThank you for completing the registration process."
        "\r\n\nIf you have any questions or concerns, feel free to contact us."
        "\r\n\nBest regards,"
        "\r\nSafety Pulse", 
        settings.EMAIL_HOST_USER,
        [email], 
    )
    return redirect('Subadmin:userverification')

def userreject(request,uid):
    user=tbl_User.objects.get(id=uid)
    user.user_status=2
    email = user.user_email
    user_name = user.user_name 
    user.save()

    send_mail(
        'User Registration Verification Rejected',  # Subject
        f"\rDear {user_name},"
        "\r\n\nWe regret to inform you that your account verification has been rejected."
        "\r\n\nHere are your registration details:"
        f"\r\n\nName: {user_name}"  # Include the user's name
        f"\r\nEmail: {email}"  # Include the user's email
        "\r\n\nThe reason for rejection could be due to missing or incorrect information."
        "\r\n\nPlease review your registration details and submit a valid application if necessary."
        "\r\n\nIf you have any questions or concerns, feel free to contact us."
        "\r\n\nBest regards,"
        "\r\nSafety Pulse",  # Body content
        settings.EMAIL_HOST_USER,
        [email],  # Recipient email address
)

    return redirect('Subadmin:userverification') 


def rtolist(request):
    if "sid" in request.session:
        RTO=tbl_rto.objects.filter(rto_status=0,place__district=request.session['districtid'])
        if request.method=='POST':
            return redirect('Subadmin:rtolist')
        else:
            return render(request,'Subadmin/RTOList.html',{'RTO':RTO})
    else:
        return redirect("Guest:login")            


def rtoverification(request):
    if "sid" in request.session:
        RTO=tbl_rto.objects.filter(rto_status=0,place__district=request.session['districtid'])
        accept=tbl_rto.objects.filter(rto_status=1,place__district=request.session['districtid'])
        reject=tbl_rto.objects.filter(rto_status=2,place__district=request.session['districtid'])
        return render(request,'Subadmin/RTOverifications.html',{'RTO':RTO,'accept':accept,'reject':reject})
    else:
        return redirect("Guest:login")    

def rtoaccept(request,rid):
    RTO=tbl_rto.objects.get(id=rid)
    RTO.rto_status=1
    email = RTO.rto_email
    rto_name = RTO.rto_name
    RTO.save()

    send_mail(
        'RTO Data Accepted',  # Subject
        f"\rDear {rto_name},"
        "\r\n\nWe are pleased to inform you that your RTO (Modified/Verified Data) has been successfully accepted."
        "\r\n\nHere are your updated registration details:"
        f"\r\n\nName: {rto_name}"  # Include the user's name
        f"\r\nEmail: {email}"  # Include the user's email
        "\r\n\nThank you for your cooperation in updating the necessary information."
        "\r\n\nIf you have any questions or concerns, feel free to contact us."
        "\r\n\nBest regards,"
        "\r\nSafety Pulse",  # Body content
        settings.EMAIL_HOST_USER,
        [email],  # Recipient email address
    )


    return redirect('Subadmin:rtoverification')

def rtoreject(request,rid):
    RTO=tbl_rto.objects.get(id=rid)
    RTO.rto_status=2
    email = RTO.rto_email
    rto_name = RTO.rto_name
    RTO.save()

    send_mail(
        'RTO Data Rejected',  # Subject
        f"\rDear {rto_name},"
        "\r\n\nWe regret to inform you that your RTO (Modified/Verified Data) submission has been rejected."
        "\r\n\nHere are your registration details:"
        f"\r\n\nName: {rto_name}"  # Include the user's name
        f"\r\nEmail: {email}"  # Include the user's email
        "\r\n\nThe reason for rejection could be due to missing, incorrect, or insufficient information."
        "\r\n\nPlease review your submission and provide the necessary updates."
        "\r\n\nIf you have any questions or concerns, feel free to contact us."
        "\r\n\nBest regards,"
        "\r\n Safety Pulse",  # Body content
        settings.EMAIL_HOST_USER,
        [email],  # Recipient email address
)
    return redirect('Subadmin:rtoverification')


def report(request):
    if "sid" in request.session:

        total_solved = tbl_Complaint.objects.filter(complaint_status__in=[1, 3]).count()
        total_pending = tbl_Complaint.objects.filter(complaint_status=0).count()
        total_complaint = tbl_Complaint.objects.all().count()
        totalusers=tbl_User.objects.filter(user_status=0).count()

        totalusers=tbl_User.objects.all().count()
        verifiedusers=tbl_User.objects.filter(user_status=1).count()
        rejectedusers=tbl_User.objects.filter(user_status=2).count()
        
        totalmvd=tbl_Mvd.objects.all().count()
        verifiedmvd=tbl_Mvd.objects.filter(mvd_status=1).count()
        rejectedmvd=tbl_Mvd.objects.filter(mvd_status=2).count()

        totalrto=tbl_rto.objects.all().count()
        verifiedrto=tbl_rto.objects.filter(rto_status=1).count()
        rejectedrto=tbl_rto.objects.filter(rto_status=2).count()

        #line data
        rating_monthly_data = (
            tbl_rating.objects
            .annotate(month=TruncMonth('datetime'))
            .values('month')
            .annotate(avg_rating=Avg('rating_data'))
            .order_by('month')
        )   
        # Format for template (e.g., "April 2025")
        formatted_rating_data = [
            {'month': entry['month'].strftime('%B %Y'), 'avg_rating': round(entry['avg_rating'], 2)}
            for entry in rating_monthly_data
        ]

        datalist=[
            {'label':'Total MVD','values':totalmvd},
            {'label':'Verified MVD','values':verifiedmvd},
            {'label':'Rejected MVD','values':rejectedmvd},

            {'label':'Total RTO','values':totalrto},
            {'label':'Verified RTO','values':verifiedrto},
            {'label':'Rejected RTO','values':rejectedrto},

            {'label':'Total User','values':totalusers},
            {'label':'Verified User','values':verifiedusers},
            {'label':'Rejected User','values':rejectedusers},
        ]

        # Group complaints by month
        month_wise_data = (
            tbl_Complaint.objects
            .annotate(month=TruncMonth('complaint_date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        

        # Format the data for the template (optional: format month as string)
        formatted_month_data = [
            {'month': month['month'].strftime('%B %Y'), 'count': month['count']}
            for month in month_wise_data
        ]
        users=[
            {'label':'Total Users','value':totalusers},
            {'label':'Verified Users','value':verifiedusers}
        ]

        data = [
            {'label': 'Solved Complaints', 'value': total_solved},
            {'label': 'Pending Complaints', 'value': total_pending},
        ]

        data2 = [
            {'label': item['month'], 'value': item['count']}
            for item in formatted_month_data
        ]


        return render(
            request,
            'Subadmin/Report.html',
            {'rating_data': formatted_rating_data,'data': data, 'month_data': formatted_month_data,'data2':data2,'users':users,'datalist':datalist}
        )
    else:
        return redirect("Guest:login")    

def logout(request):
    del request.session["sid"]
    return redirect("Guest:login")                 
        
