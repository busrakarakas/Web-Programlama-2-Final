from django.contrib import admin
from .models import Gonderi,Yorum,Anket,AnketSecenek,Sohbet,Mesaj
for m in [Gonderi,Yorum,Anket,AnketSecenek,Sohbet,Mesaj]: admin.site.register(m)
