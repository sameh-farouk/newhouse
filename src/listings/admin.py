from django.contrib import admin
from .models import Destrict, Governorate, Picture, Listing, Propty, Fav
# Register your models here.
admin.site.register(Governorate)
admin.site.register(Destrict)
admin.site.register(Listing)
admin.site.register(Picture)
admin.site.register(Propty)
admin.site.register(Fav)