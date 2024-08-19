from django.contrib import admin
from .models import Sst, Sstanswer, Ro, Roanswer, Mcq, Mcqanswer

admin.site.register(Sst)
admin.site.register(Sstanswer)
admin.site.register(Ro)
admin.site.register(Roanswer)
admin.site.register(Mcq)
admin.site.register(Mcqanswer)