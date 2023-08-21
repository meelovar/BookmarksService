from django.contrib import admin

from api_auth.models.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
