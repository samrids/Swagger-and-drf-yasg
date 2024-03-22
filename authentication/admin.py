from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    
    add_form_template='add_form.html'

    list_display = ('first_name','last_name','email','is_staff', 'is_active',)
    list_filter = ('first_name','email', 'is_staff', 'is_active','is_verified')

    search_fields = ('username', 'email','first_name', 'last_name', 'nick_name', 'bio','mobile', 'facebook', 'instagram', 'youtube')
    ordering = ('first_name',)

    add_fieldsets = (
        ('Personal Information', {
            'description': "",
            'classes': ('wide',),  
            'fields': (('first_name','last_name'), ('username','email'), 'nick_name', 'bio', 'mobile', 'facebook', 'instagram', 'youtube', 'profile',
                       'password1', 'password2',)}
        ),
        ('Permissions',{
            'description': "",
            'classes': ('wide', 'collapse'),
            'fields':( 'is_staff', 'is_active', 'is_verified')}
        ),
    )

    fieldsets = (
        ('Personal Information', {
            'classes': ('wide',),
            'fields': (('first_name','last_name'), ('username','email'), 'nick_name', 'bio','mobile', 'facebook', 'instagram', 'youtube', 'profile', 'password')}),
        ('Permissions', {'fields': ('is_superuser','is_staff', 'is_active','is_verified',)}),
    )

admin.site.register(User, CustomUserAdmin)