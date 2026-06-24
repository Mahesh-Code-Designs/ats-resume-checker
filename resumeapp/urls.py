from django.urls import path
from . import views

urlpatterns = [
    path('',views.upload_resume ),
    path ('dashboard/', views.dashboard,name='dashboard'),
    path('download/', views.download_csv, name='download_csv'),
    
]
