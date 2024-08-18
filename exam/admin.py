from django.contrib import admin
from .models import Sst, Sstuseranswer, Ro, Rouseranswer

# Register your models here.
admin.site.register(Sst)
admin.site.register(Sstuseranswer)
admin.site.register(Ro)
admin.site.register(Rouseranswer)
