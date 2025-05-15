from django.urls import path,include
from Administrator import views

app_name='Admin'
urlpatterns = [
path('AdminHome/',views.AdminHome,name='AdminHome'),

path('AdminRegistration/',views.AdminRegistration,name='AdminRegistration'),
path('deleteadminreg/<int:admin_id>',views.deleteadminreg,name='deleteadminreg'),
path('editadminreg/<int:admin_id>',views.editadminreg,name='editadminreg'),

path('District/',views.District,name='District'),
path('deletedistrict/<int:district_id>',views.deletedistrict,name='deletedistrict'),
path('editdistrict/<int:district_id>',views.editdistrict,name='editdistrict'),

path('Category/',views.Category,name='Category'),
path('deletecategory/<int:category_id>',views.deletecategory,name='deletecategory'),
path('editcategory/<int:category_id>',views.editcategory,name='editcategory'),

path('place/',views.place,name='place'),
path('deleteplace/<int:place_id>',views.deleteplace,name='deleteplace'),
path('editplace/<int:place_id>',views.editplace,name='editplace'),
path('ajaxsearchdistrict/',views.ajaxsearchdistrict,name='ajaxsearchdistrict'), 

path('subcategory/',views.subcategory,name='subcategory'),
path('deletesubcategory/<int:subcategory_id>',views.deletesub,name='deletesubcategory'),
path('editsubcategory/<int:subcategory_id>',views.editsub,name='editsubcategory'),

path('department/',views.department,name='department'),
path('deletedept/<int:department_id>',views.deletedept,name='deletedept'),
path('editdept/<int:department_id>',views.editdept,name='editdept'),

path('designation/',views.designation,name='designation'),
path('deletedsgn/<int:designation_id>',views.deletedsgn,name='deletedsgn'),
path('editdsgn/<int:designation_id>',views.editdsgn,name='editdsgn'),

path('employee/',views.employeereg,name='employee'),
path('deleteemployee/<int:eid>',views.deleteemployee,name='deleteemployee'),
path('editemployee/<int:eid>',views.editemployee,name='editemployee'),

path('Viewcomplaints/',views.Viewcomplaints,name='Viewcomplaints'),
path('replycomplaint/<int:complaint_id>',views.replycomplaint,name='replycomplaint'),

path('subadminreg/',views.subadminreg,name='subadminreg'),
path('deletesubadmin/<int:subadmin_id>',views.deletesubadmin,name='deletesubadmin'),
path('editsubadmin/<int:subadmin_id>',views.editsubadmin,name='editsubadmin'),

path('Viewfeedback/',views.Viewfeedback,name='Viewfeedback'),
path('viewrating/',views.viewrating,name='viewrating'),

path('Doughnutchart/', views.Doughnutchart, name='Doughnutchart'),
path('logout/',views.logout,name='logout'),
path('report/',views.report,name='report'),
path('barchart/',views.barchart,name='barchart'),
path('linechart/',views.linechart,name='linechart'),
path('horizontalchart/',views.horizontalchart,name='horizontalchart'),
]
