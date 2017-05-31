from django.contrib import admin

# Register your models here.
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
admin.site.register(Account, AccountAdmin)

