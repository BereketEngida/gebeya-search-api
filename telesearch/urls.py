from django.urls import path
from . import views

app_name = 'telesearch'

urlpatterns = [
    path('', views.index, name='index'),
]
