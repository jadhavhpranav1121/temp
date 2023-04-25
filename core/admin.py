from django.contrib import admin
from .models import Convict, Block, ConvictValidate
# Register your models here.
admin.site.register(Convict)
admin.site.register(ConvictValidate)
admin.site.register(Block)