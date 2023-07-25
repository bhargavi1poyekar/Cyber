from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('launch_vm_request',views.launch_vm_request,name='launch_vm'),
    path('launch_vm_request/new_vm',views.new_vm, name='new_vm'),
]