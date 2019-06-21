from django.contrib import admin

from .models import SocialProvider

@admin.register(SocialProvider)
class SocialProviderAdmin(admin.ModelAdmin):
    pass
