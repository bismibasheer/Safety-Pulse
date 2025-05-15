from django.urls import path,include
from RTO import views

app_name='RTO'
urlpatterns = [

path('RTOHome/',views.RTOHome,name='RTOHome'),

path('Myprofile/',views.Myprofile,name='Myprofile'),

path('Editprofile/',views.Editprofile,name='Editprofile'),

path('Changepassword/',views.Changepassword,name='Changepassword'),

path('addvideo/',views.addvideo,name='addvideo'),
path('videodelete/<int:did>',views.videodelete,name='videodelete'),  

path('addarticle/',views.addarticle,name='addarticle'),
path('deletearticle/<int:did>',views.deletearticle,name='deletearticle'), 

path('vehicledetails/',views.vehicledetails,name='vehicledetails'),
path('deletevehicles/<int:vehicle_id>',views.deletevehicles,name='deletevehicles'),
path('editvehicles/<int:vehicle_id>',views.editvehicles,name='editvehicles'),

path('Viewrequest/',views.Viewrequest,name='Viewrequest'),
path('resolvedrequest/',views.resolvedrequest,name='resolvedrequest'),


path('verifymultiplerequest/<int:id>',views.verifymultiplerequest,name='verifymultiplerequest'),

path('logout/',views.logout,name='logout'),

]