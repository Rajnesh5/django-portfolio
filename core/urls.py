"""
URL configuration for the core portfolio app.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',                                       views.home,            name='home'),
    path('projects/',                              views.projects,        name='projects'),
    path('contact/',                               views.contact,         name='contact'),
    path('resume/Rajnesh_Kr_Ranjan_Resume.pdf',   views.download_resume, name='download_resume'),
]
