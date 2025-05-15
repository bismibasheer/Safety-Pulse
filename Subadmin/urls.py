from django.urls import path,include
from Guest import views
from Subadmin import views

app_name='Subadmin'
urlpatterns = [
path('SubadminHome/',views.SubadminHome,name='SubadminHome'),

path('mvdlist/',views.mvdlist,name='mvdlist'), 

path('mvdverification/',views.mvdverification,name='mvdverification'),
path('accept/<int:mid>',views.accept,name='accept'),
path('reject/<int:mid>',views.reject,name='reject'),

path('userlist/',views.userlist,name='userlist'), 

path('userverification/',views.userverification,name='userverification'),
path('useraccept/<int:uid>',views.useraccept,name='useraccept'),
path('userreject/<int:uid>',views.userreject,name='userreject'),

path('rtolist/',views.rtolist,name='rtolist'), 

path('rtoverification/',views.rtoverification,name='rtoverification'),
path('rtoaccept/<int:rid>',views.rtoaccept,name='rtoaccept'),
path('rtoreject/<int:rid>',views.rtoreject,name='rtoreject'),

path('logout/',views.logout,name='logout'),
path('report/',views.report,name='report'),
  
]