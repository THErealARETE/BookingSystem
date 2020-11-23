from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User

from .forms import AdminUserChangeForm


class UserAdmin(BaseUserAdmin):

    #model to be used
    model = User

    #the forms to be used instead of the default
    form = AdminUserChangeForm
    add_form = AdminUserChangeForm

    #the field to be used in displaying the User Model
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    list_filter = ('username', 'first_name','last_name', 'email')

    fieldsets = (
        (None , {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name', 'photo')}),
        ('permission', {'fields':('is_admin', 'is_staff', 'is_active', 'is_superuser')})
    )

    add_fieldsets = ( 
        (None , {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )

    search_fields = ('username' , 'first_name', 'last_name'),
    ordering = ('username', 'first_name', 'last_name'),
    filer_horizontal = ()

    def get_inline_instances(self, request, obj = None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
    
# Register your models here.


admin.site.register(User)

admin.site.unregister(Group)