from django.shortcuts import render,redirect
from Administrator.models import *
from Guest.models import *
from User.models import *
from datetime import date,datetime
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.db.models import Count
from datetime import datetime
from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def AdminRegistration(request):
        if "aid" in request.session:
            admin=tbl_admin.objects.all()
            if request.method=='POST':
                tbl_admin.objects.create(admin_name=request.POST.get('txt_name'),
                admin_contact=request.POST.get('txt_con'),
                admin_email=request.POST.get('txt_email'),
                admin_password=request.POST.get('txt_pwd'),
                )
                return redirect('Admin:AdminRegistration')
            else:    
                return render(request,'Administrator/AdminRegistration.html',{'admin':admin})
        else:
            return redirect("Guest:login")        

def deleteadminreg(request,admin_id):
    tbl_admin.objects.get(id=admin_id).delete()
    return redirect('Admin:AdminRegistration')

def editadminreg(request,admin_id):
    reg=tbl_admin.objects.get(id=admin_id)
    if request.method=="POST":
        reg.admin_name=request.POST.get('txt_name')
        reg.admin_contact=request.POST.get('txt_con') 
        reg.admin_email=request.POST.get('txt_email')  
        reg.admin_password=request.POST.get('txt_pwd')
        reg.save()
        return redirect('Admin:AdminRegistration')
    else:
        return render(request,'Administrator/AdminRegistration.html',{'editreg':reg}) 

def District(request):
    if "aid" in request.session:
        District=tbl_district.objects.all()
        if request.method=='POST':
            discount=tbl_district.objects.filter(district_name=request.POST.get('txt_dis')).count()
            if discount>0:
                return render(request,'Administrator/District.html',{'msg':"Already Exisit"})
            else:
                tbl_district.objects.create(district_name=request.POST.get('txt_dis'))
                return render(request,'Administrator/District.html',{'District':District,'msg':"District Registered Sucessfully!"})
        else:
            return render(request,'Administrator/District.html',{'District':District})
    else:
        return redirect("Guest:login")    

def deletedistrict(request,district_id):
    tbl_district.objects.get(id=district_id).delete()
    return render(request,'Administrator/District.html',{'msg':"District Deleted Sucessfully!"})


def editdistrict(request,district_id):
    dist=tbl_district.objects.get(id=district_id)
    if request.method=="POST":
        dist.district_name=request.POST.get('txt_dis')
        dist.save()
        return render(request,'Administrator/District.html',{'msg':"District Edited Sucessfully!"})
    else:
        return render(request,'Administrator/District.html',{'editdist':dist})        

def Category(request):
    if "aid" in request.session:
        Category=tbl_category.objects.all()
        if request.method=='POST':
            tbl_category.objects.create(category_name=request.POST.get('txt_category'),
            )
            return render(request,'Administrator/Category.html',{'msg':"Category Registered Sucessfully!"})

        else:    
            return render(request,'Administrator/Category.html',{'Category':Category})
    else:
        return redirect("Guest:login")

def deletecategory(request,category_id):
    tbl_category.objects.get(id=category_id).delete()
    return render(request,'Administrator/Category.html',{'msg':"Category Deleted Sucessfully!"})

def editcategory(request,category_id):
    cat=tbl_category.objects.get(id=category_id)
    if request.method=="POST":
        cat.category_name=request.POST.get('txt_category')
        cat.save()
        return render(request,'Administrator/Category.html',{'msg':"Category Edited Sucessfully!"})
    else:
        return render(request,'Administrator/Category.html',{'editcat':cat})        

def place(request):
    if "aid" in request.session:
        dis=tbl_district.objects.all()
        place1=tbl_place.objects.all()
        if request.method=="POST":
            placename=request.POST.get("txt_place")
            placepincode=request.POST.get("txt_pincode")
            districtid=tbl_district.objects.get(id=request.POST.get("sel_district"))
            tbl_place.objects.create(place_name=placename,place_pincode=placepincode,district=districtid)
            return render(request,'Administrator/Place.html',{'dis':dis,'place1':place1,'msg':"Place Registered Sucessfully!"})
        else:
            return render(request,'Administrator/Place.html',{'dis':dis,'place1':place1})
    else:
        return redirect("Guest:login")        


def ajaxsearchdistrict(request):
    name=request.GET.get("name","").strip()
    Place=tbl_place.objects.filter(
        Q(district__district_name__istartswith=name) | Q(place_name__istartswith=name)
    )
    return render(request,"Administrator/Ajaxdistrict.html",{'data':Place})

def deleteplace(request,place_id):
    tbl_place.objects.get(id=place_id).delete()
    return render(request,'Administrator/Place.html',{'msg':"Place Deleted Sucessfully!"})

def editplace(request,place_id):
    dis=tbl_district.objects.all()
    place1=tbl_place.objects.get(id=place_id)
    if request.method=="POST":
        place1.place_name=request.POST.get('txt_place')
        place1.place_pincode=request.POST.get('txt_pincode')
        place1.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        place1.save()
        return render(request,'Administrator/Place.html',{'editplace':place1,'dis':dis,'msg':"Place Edited Sucessfully!"})
    else:
        return render(request,'Administrator/Place.html',{'editplace':place1,'dis':dis})

def subcategory(request):
    if "aid" in request.session:
        cat=tbl_category.objects.all()
        sub=tbl_subcategory.objects.all()
        if request.method=="POST":
            subname=request.POST.get("txt_sub")
            categoryid=tbl_category.objects.get(id=request.POST.get("sel_category"))
            tbl_subcategory.objects.create(subcategory_name=subname,category=categoryid)
            return redirect('Admin:subcategory')
        else:
            return render(request,'Administrator/Subcategory.html',{'cat':cat,'sub':sub})
    else:
        return redirect("Guest:login")

def deletesub(request,subcategory_id):
    tbl_subcategory.objects.get(id=subcategory_id).delete()
    return redirect('Admin:subcategory')

def editsub(request,subcategory_id):
    cat=tbl_category.objects.all()
    sub=tbl_subcategory.objects.get(id=subcategory_id)
    if request.method=="POST":
        sub.subcategory_name=request.POST.get('txt_sub')
        sub.category=tbl_category.objects.get(id=request.POST.get('sel_category'))
        sub.save()
        return redirect('Admin:subcategory')
    else:
        return render(request,'Administrator/Subcategory.html',{'editsub':sub,'cat':cat})    

def department(request):
    department=tbl_department.objects.all()
    if request.method=='POST':
        tbl_department.objects.create(department_name=request.POST.get('txt_dept'),
        )
        return redirect('Admin:department')
    else:    
        return render(request,'Administrator/Department.html',{'department':department})

def deletedept(request,department_id):
    tbl_department.objects.get(id=department_id).delete()
    return redirect('Admin:department') 

def editdept(request,department_id):
    depts=tbl_department.objects.get(id=department_id)
    if request.method=="POST":
        depts.department_name=request.POST.get('txt_dept')
        depts.save()
        return redirect('Admin:department')
    else:
        return render(request,'Administrator/Department.html',{'editdepts':depts}) 

def designation(request):
    desig=tbl_designation.objects.all()
    if request.method=='POST':
        tbl_designation.objects.create(designation_name=request.POST.get('txt_desg'),
        )
        return redirect('Admin:designation')
    else:
        return render(request,'Administrator/Designation.html',{'desig':desig})

def deletedsgn(request,designation_id):
    tbl_designation.objects.get(id=designation_id).delete()
    return redirect('Admin:designation') 

def editdsgn(request,designation_id):
    dsgn=tbl_designation.objects.get(id=designation_id)
    if request.method=="POST":
        dsgn.designation_name=request.POST.get('txt_desg')
        dsgn.save()
        return redirect('Admin:designation')
    else:
        return render(request,'Administrator/Designation.html',{'editdsgns':dsgn}) 

def employeereg(request):
    department=tbl_department.objects.all()
    designation=tbl_designation.objects.all()
    employeedata=tbl_employee.objects.all()
    if request.method=='POST':
        name=request.POST.get("txt_name")
        contact=request.POST.get("txt_contact")
        email=request.POST.get("txt_email")
        address=request.POST.get("txt_address")
        salary=request.POST.get('txt_salary')
        departmentid=tbl_department.objects.get(id=request.POST.get("sel_dept"))
        designationid=tbl_designation.objects.get(id=request.POST.get("sel_desi"))
        tbl_employee.objects.create(employee_name=name,department=departmentid,designation=designationid,employee_contact=contact,employee_email=email,employee_address=address,employee_salary=salary)
        return redirect('Admin:employee')
    else:
        return render(request,'Administrator/Employee.html',{'department':department,'designation':designation,'employeedata':employeedata})

def deleteemployee(request,eid):
    tbl_employee.objects.get(id=eid).delete()
    return redirect('Admin:employee')

def editemployee(request,eid):
    employee=tbl_employee.objects.get(id=eid)
    department=tbl_department.objects.all()
    designation=tbl_designation.objects.all()
    if request.method=='POST':
        employee.employee_name=request.POST.get('txt_name')
        employee.employee_contact=request.POST.get('txt_contact')
        employee.employee_email=request.POST.get('txt_email')
        employee.employee_address=request.POST.get('txt_address')
        employee.employee_salary=request.POST.get('txt_salary')
        employee.department=tbl_department.objects.get(id=request.POST.get("sel_dept"))
        employee.designation=tbl_designation.objects.get(id=request.POST.get("sel_desi"))
        employee.save()
        return redirect('Admin:employee')
    else:
        return render(request,'Administrator/Employee.html',{'department':department,'designation':designation,'editemployee':employee}) 



def AdminHome(request):
    if "aid" in request.session:
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
            'Administrator/AdminHome.html',
            {'rating_data': formatted_rating_data,'data': data, 'month_data': formatted_month_data,'data2':data2,'users':users,'datalist':datalist}
        )
    else:
        return redirect("Guest:login")


def Viewcomplaints(request):
    if "aid" in request.session:
        complaint=tbl_Complaint.objects.filter(com_status=0)
        replycom=tbl_Complaint.objects.filter(com_status=1)
        if request.method=='POST':
            return redirect('Admin:Viewcomplaints')
        else:
            return render(request,'Administrator/ViewUserComplaint.html',{"complaint":complaint,"Reply":replycom})
    else:
        return redirect("Guest:login")        

def replycomplaint(request,complaint_id):
    complaint=tbl_Complaint.objects.get(id=complaint_id)
    user=tbl_User.objects.get(id=request.session['uid'])
    if request.method=='POST':
        complaint.reply_complaint=request.POST.get('txt_reply')
        complaint.com_status=1
        complaint.reply_date=date.today()
        complaint.save()
        return redirect('Admin:Viewcomplaints')
    else:
        return render(request,'Administrator/ReplyComplaint.html',{"complaint":complaint,"user":user})
           

from django.core.mail import send_mail
from django.conf import settings

def subadminreg(request):
    if "aid" in request.session:
        District = tbl_district.objects.all()
        subadmin = tbl_subadmin.objects.all()
        if request.method == 'POST':
            subadminname = request.POST.get("txt_name")
            subadminmail = request.POST.get("txt_email")
            subadminpassword = request.POST.get("txt_pwd")
            districtid = tbl_district.objects.get(id=request.POST.get("sel_district"))
            emailcount = tbl_subadmin.objects.filter(subadmin_email=subadminmail).count()
            discount = tbl_subadmin.objects.filter(district=districtid).count()

            if emailcount > 0:
                return render(request, 'Administrator/SubAdmin.html', {
                    'District': District,
                    'subadmin': subadmin,
                    'msg': "Email Already Exists!"
                })
            elif discount > 0:
                return render(request, 'Administrator/SubAdmin.html', {
                    'District': District,
                    'subadmin': subadmin,
                    'msg': "District Already Assigned!"
                })
            else:
                tbl_subadmin.objects.create(
                    subadmin_name=subadminname,
                    subadmin_email=subadminmail,
                    subadmin_password=subadminpassword,
                    district=districtid
                )

                # ✅ Send confirmation email
                subject = "Subadmin Registration - Safety Pulse"
                message = f"""
Dear {subadminname},

You have been successfully registered as a Subadmin on **Safety Pulse**.

Your login credentials are:
Username: {subadminmail}
Password: {subadminpassword}

Please sign in and start overseeing your assigned district for verification.

If you need any support, feel free to reach out.

Best regards,  
Team Safety Pulse
"""
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [subadminmail],
                )

                return render(request, 'Administrator/SubAdmin.html', {
                    'District': District,
                    'subadmin': subadmin,
                    'msg': "Subadmin Registered Successfully"
                })
        else:
            return render(request, 'Administrator/SubAdmin.html', {
                'District': District,
                'subadmin': subadmin
            })
    else:
        return redirect("Guest:login")
    

def deletesubadmin(request,subadmin_id):
    tbl_subadmin.objects.get(id=subadmin_id).delete()
    return render(request,'Administrator/SubAdmin.html',{'msg':"SubAdmin Deleted Successfully!"})

def editsubadmin(request,subadmin_id):
    District=tbl_district.objects.all()
    subadmin=tbl_subadmin.objects.get(id=subadmin_id)
    if request.method=="POST":
        subadmin.subadmin_name=request.POST.get('txt_name')
        subadmin.subadmin_email=request.POST.get('txt_email')
        subadmin.subadmin_password=request.POST.get('txt_pwd')
        subadmin.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        subadmin.save()
        return render(request,'Administrator/SubAdmin.html',{'msg':"SubAdmin Updated Successfully!"})
    else:
        return render(request,'Administrator/SubAdmin.html',{'editsubadmin':subadmin,'District':District})









    
def Viewfeedback(request):
    if "aid" in request.session:
        feedback=tbl_Feedback.objects.all()
        user=tbl_User.objects.all()
        return render(request,'Administrator/ViewFeedback.html',{'feedback':feedback,'user':user})
    else:
        return redirect("Guest:login")

def viewrating(request):
    if "aid" in request.session:
        data=tbl_rating.objects.all()
        return render(request,'Administrator/Rating.html',{'data':data})
    else:
        return redirect("Guest:login")    

def logout(request):
    del request.session["aid"]
    return redirect("Guest:login")



def report(request):
    # Get distinct years and months from complaints
    all_complaints = tbl_Complaint.objects.all().order_by('complaint_date')
    
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
            complaint_date__month=selected_month
        )
    elif selected_year:
        complaints = all_complaints.filter(complaint_date__year=selected_year)
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
    
    return render(request, 'Administrator/Report.html', context)

from django.shortcuts import render
from datetime import datetime
from User.models import tbl_Complaint
from django.db.models import Count, Q

def Doughnutchart(request):
   
    # Solved: status 1 or 3
    total_solved = tbl_Complaint.objects.filter(complaint_status__in=[1, 3]).count()

    # Pending: status 0
    total_pending = tbl_Complaint.objects.filter(complaint_status=0).count()

    # Final data format
    data = [
        {'label': 'Solved Complaints', 'value': total_solved},
        {'label': 'Pending Complaints', 'value': total_pending}
    ]

    return render(request, 'Administrator/Doughnutchart.html', {'data':data})

def barchart(request):
    if "aid" in request.session:
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
            'Administrator/Barchart.html',
            {'rating_data': formatted_rating_data,'data': data, 'month_data': formatted_month_data,'data2':data2,'users':users,'datalist':datalist}
        )
    else:
        return redirect("Guest:login")    

def linechart(request):
    if "aid" in request.session:
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
            'Administrator/Linechart.html',
            {'rating_data': formatted_rating_data,'data': data, 'month_data': formatted_month_data,'data2':data2,'users':users,'datalist':datalist}
        )
    else:
        return redirect("Guest:login")    

def horizontalchart(request):
    if "aid" in request.session:
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
            'Administrator/Horizontalchart.html',
            {'rating_data': formatted_rating_data,'data': data, 'month_data': formatted_month_data,'data2':data2,'users':users,'datalist':datalist}
        )
    else:
        return redirect("Guest:login")    


