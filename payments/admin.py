from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import SubscriptionPlan, Subscription, PaymentRecord


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display  = ("name", "price", "duration")
    search_fields = ("name",)
    fieldsets = (
        (None, {
            "fields": ("name", "price", "duration", "description"),
            "description": _(
                "Создавайте тарифы: задавайте название, цену, длительность и описание."
            ),
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display    = ("user", "plan", "start_date", "end_date", "amount")
    list_filter     = ("plan", "start_date", "end_date")
    search_fields   = ("user__username", "plan__name")
    readonly_fields = ("start_date", "amount")

    fieldsets = (
        (None, {
            "fields": ("user", "plan", "start_date", "end_date", "amount"),
        }),
    )


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display    = ("telegram_payment_id", "subscription", "status", "created_at")
    list_filter     = ("status", "created_at")
    search_fields   = ("telegram_payment_id",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": ("subscription", "telegram_payment_id", "status", "created_at"),
        }),
    )
