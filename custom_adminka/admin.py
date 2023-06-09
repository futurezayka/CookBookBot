from django.contrib import admin
from .models import CurrentUser, Recipe


@admin.register(CurrentUser)
class AdminCurrentUser(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    pass
