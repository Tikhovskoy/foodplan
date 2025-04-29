from django.contrib import admin
from users.models import TelegramUser, Category

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "first_name", "last_name", "paid_until", "has_active_subscription_display")
    list_filter = ("paid_until",)
    search_fields = ("telegram_id", "username", "first_name", "last_name")
    ordering = ("-date_joined",) 
    @admin.display(description="Активная подписка")
    def has_active_subscription_display(self, obj):
        return obj.has_active_subscription()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
