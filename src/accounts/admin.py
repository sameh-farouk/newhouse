from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import Profile

admin.AdminSite.site_header = 'NEWHouse administration'
admin.site.site_header = 'NEWHouse Admin Panel'
admin.site.site_title = 'NEWHouse'




admin.site.register(Profile)