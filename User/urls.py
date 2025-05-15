from django.urls import path,include
from User import views

app_name='User'
urlpatterns = [
path('UserHome/',views.UserHome,name='UserHome'),

path('Myprofile/',views.Myprofile,name='Myprofile'),

path('Editprofile/',views.Editprofile,name='Editprofile'),

path('Changepassword/',views.Changepassword,name='Changepassword'),

path('postcomplaint/<int:id>',views.postcomplaint,name='postcomplaint'),

path('mvdlist/',views.mvdlist,name='mvdlist'), 
path('ajaxsearch/',views.ajaxsearch,name='ajaxsearch'),

path('feedback/',views.feedback,name='feedback'),

path('repliedcomplaint/',views.repliedcomplaint,name='repliedcomplaint'),


path('contentlist/',views.contentlist,name='contentlist'), 

path('searchdetails/',views.searchdetails,name='searchdetails'), 
path('ajaxsearchvehicle/',views.ajaxsearchvehicle,name='ajaxsearchvehicle'),
path('ajaxchecknumber/',views.ajaxchecknumber,name='ajaxchecknumber'),

path('logout/',views.logout,name='logout'),


path('rating/',views.rating,name="rating"),  
path('ajaxstar/',views.ajaxstar,name="ajaxstar"),
path('starrating/',views.starrating,name="starrating"),

path("payment/<int:id>",views.payment,name="payment"),
path('loader/',views.loader, name='loader'),
path('paymentsuc/',views.paymentsuc, name='paymentsuc'),

path('track/<int:id>',views.track, name='track'),
path('viewchellan/<int:id>',views.viewchellan, name='viewchellan'),
path('get_comp_count/',views.get_comp_count,name='get_comp_count'),
path('Mypoints',views.Mypoints,name="Mypoints"),
path('withdrawpoints/', views.Withdrawpoints, name="Withdrawpoints"),
]