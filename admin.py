from django.contrib import admin
from order365.models import * 
# Register your models here.

admin.site.register(Binder)
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(Configurations)

