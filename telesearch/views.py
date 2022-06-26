from django.shortcuts import render
from .models import Category, Product
from rest_framework import generics
from api.serializers import ProductSerializer, CategorySerializer, ChannelSerializer
# Create your views here.


def index(request):
    return render(request, 'index.html')
