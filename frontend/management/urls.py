from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('insurance/', views.view_insurance, name='view_insurance'),
    path('patient/', views.view_patient, name='view_patient'),
    path('report/', views.view_report, name='view_report'),
    #Facility Views
    path('facility/', views.view_facility, name='view_facility'),
    path('facility/ob', views.view_ob, name='view_ob'),
    path('facility/ops', views.view_ops, name='view_ops'),
    path('facility/add', views.create_facility, name='create_facility'),
    #Employee Views
    path('emp/doctor/', views.view_doctor, name='view_doctor'),
    path('emp/nurse/', views.view_nurse, name='view_nurse'),
    path('emp/admin_staff/', views.view_admin_staff, name='view_admin_staff'),
    path('emp/hcp/', views.view_hcp, name='view_hcp'),
    path('emp/add_employee/', views.add_employee, name='add_employee'),
    path('emp/edit_employee/', views.edit_employee, name='edit_employee'),
    path('emp/', views.view_employee, name='view_employee'),
]
