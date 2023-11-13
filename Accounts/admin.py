from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'firstname', 'lastname', 'is_admin', 'is_staff', 'is_superuser', 'is_instructor', 'is_student')
    search_fields = ('email', )
    readonly_fields = ['id']
    ordering = ('email',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)