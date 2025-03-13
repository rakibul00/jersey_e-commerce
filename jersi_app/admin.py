from django.contrib import admin
from .models import Cart,Category,Jersi,Address
# Register your models here.
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Jersi)
admin.site.register(Address)