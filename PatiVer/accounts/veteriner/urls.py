from django.urls import path
from . import views
urlpatterns=[
    path('',views.liste,name='veteriner'),
    path('<int:pk>/randevu/',views.randevu,name='randevu'),
    path('randevularim/',views.randevularim,name='randevularim'),
]
