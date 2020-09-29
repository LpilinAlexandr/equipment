from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='index'),
    path('ajax_form/', views.ajax_form, name='ajax_form')
]

