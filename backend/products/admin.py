from django.contrib import admin
from products import models

admin.site.register(models.MyUser)
admin.site.register(models.Product)

# Register your models here.
