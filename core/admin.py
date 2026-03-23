from django.contrib import admin
from .models import Component, Build, Order, Profile

admin.site.register(Component)
admin.site.register(Build)
admin.site.register(Order)
admin.site.register(Profile)