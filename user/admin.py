from django.contrib import admin
from django.contrib.auth.models import Group
from user import models

class ProfileInline(admin.StackedInline):
    model = models.Profile


class UserAdmin(admin.ModelAdmin):
    model = models.User
    fields = ['username']
    inlines = [ProfileInline]


admin.site.register(models.User, UserAdmin)
admin.site.unregister(Group)