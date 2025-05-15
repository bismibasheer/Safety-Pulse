from django.urls import path,include
from Guest import views
from MVD import views

app_name='MVD'
urlpatterns = [
path('MVDHome/',views.MVDHome,name='MVDHome'),

path('Myprofile/',views.Myprofile,name='Myprofile'),

path('Editprofile/',views.Editprofile,name='Editprofile'),

path('Changepassword/',views.Changepassword,name='Changepassword'),

path('Viewcomplaints/',views.Viewcomplaints,name='Viewcomplaints'),

path('replycomplaint/<int:complaint_id>',views.replycomplaint,name='replycomplaint'),

path('repliedcomplaint/',views.repliedcomplaint,name='repliedcomplaint'),

path('rtolist/<int:id>',views.rtolist,name='rtolist'), 
path('ajaxsearchrto/',views.ajaxsearchrto,name='ajaxsearchrto'),

path('requestsend/<int:id>/<int:vid>',views.requestsend,name='requestsend'),

path('vehiclelist/',views.vehiclelist,name='vehiclelist'), 
path('ajaxsearchnumber/',views.ajaxsearchnumber,name='ajaxsearchnumber'), 
path('resolvedcomplaint/',views.resolvedcomplaint,name='resolvedcomplaint'), 

path('multiple_violations/',views.multiple_violations,name='multiple_violations'), 
path('ajaxupdateamount/',views.ajaxupdateamount,name='ajaxupdateamount'),

path('logout/',views.logout,name='logout'),
path('generatechellan/<int:id>',views.generatechellan,name='generatechellan'),
path('viewchellan/<int:id>',views.viewchellan, name='viewchellan'),


path('report/',views.report,name='report'),
path('get_comp_count/',views.get_comp_count,name='get_comp_count'),
path('get_violation_count/',views.get_violation_count,name='get_violation_count'),




]