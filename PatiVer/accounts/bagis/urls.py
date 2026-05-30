from django.urls import path
from . import views
urlpatterns=[path('',views.bagis_view,name='bagis')]
