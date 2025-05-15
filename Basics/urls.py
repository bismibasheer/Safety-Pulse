from django.urls import path,include
from Basics import views

app_name = 'Basics'
urlpatterns = [
   path('calculator/',views.calculator,name='calculator'),
   path('largestsmallest/',views.largestsmallest,name='largestsmallest'),
   path('marklist/',views.marklist,name='marklist'),
   path('Userregistration/', views.userreg, name='userreg'),
   path('check-email/', views.check_email, name='check_email'),
]
