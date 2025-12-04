from django.contrib import admin
from .models import Apt, Amounts, Info, Coords, Images

# Register your models here.
admin.site.register(Apt)
admin.site.register(Amounts)
admin.site.register(Info)
admin.site.register(Coords)
admin.site.register(Images)