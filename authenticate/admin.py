from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authenticate.models import User

class myUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_admin', 'is_staff', 'date_joined', 'last_login')
    search_fields = ('username', 'email')
    readonly_fields = ('id','date_joined', 'last_login')

    filter_horizontal = ()
    list_filter=()
    fieldsets = ()

admin.site.register(User, myUserAdmin)
# Register your models here.
