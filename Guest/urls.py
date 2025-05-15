from django.urls import path,include
from Administrator import views
from Guest import views
app_name='Guest'

urlpatterns = [
    path('UserRegister/',views.UserRegister,name='UserRegister'),
    path('check-email/', views.check_email, name='check_email'),
    path('ajaxplace/',views.ajaxplace,name='ajaxplace'),
    path('login/',views.login,name='login'),
    path('mvdregistration/',views.mvdregistration,name='mvdregistration'),
    path('check_mvd_email/', views.check_mvd_email, name='check_mvd_email'),
    path('check_rto_email/', views.check_rto_email, name='check_rto_email'),
    path('GuestHome/',views.GuestHome,name='GuestHome'),
    path('RtoRegister/',views.RtoRegister,name='RtoRegister'),
    path('',views.index,name='index'),
    
]