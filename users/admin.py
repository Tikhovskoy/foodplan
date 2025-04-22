from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Profile, Category

User = get_user_model()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _("Профили")
    filter_horizontal = ('categories', 'liked', 'disliked')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display      = ('user', 'get_categories', 'is_active_subscriber')
    list_filter       = ('categories',)
    search_fields     = ('user__username', 'user__email')
    filter_horizontal = ('categories', 'liked', 'disliked')
    readonly_fields   = ('paid_until', 'last_free_recipe', 'swap_count')

    def get_categories(self, obj: Profile) -> str:
        return ", ".join(c.name for c in obj.categories.all())
    get_categories.short_description = _("Категории")


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
