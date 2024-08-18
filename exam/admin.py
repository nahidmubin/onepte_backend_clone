from django.contrib import admin
from .models import Sst, Sstuseranswer, Ro, Rouseranswer, Mcq, Mcquseranswer

# Register your models here.
admin.site.register(Sst)
admin.site.register(Sstuseranswer)
admin.site.register(Ro)
admin.site.register(Rouseranswer)
admin.site.register(Mcq)
admin.site.register(Mcquseranswer)