from django.urls import path
from . import views

app_name = 'scraps'
urlpatterns = [
    path('', views.index, name='index'),
    path('crud/', views.crud, name='crud')
]