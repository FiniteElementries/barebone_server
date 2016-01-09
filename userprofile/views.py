from django.shortcuts import render
from rest_framework import viewsets
from models import UserProfile
import api_userprofile
# Create your views here.

def OverView(request):
    return api_userprofile.get_userprofile_detail(request)

