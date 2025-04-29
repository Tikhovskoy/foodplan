from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import TelegramUser 


class SubscriptionPlan(models.Model):
    """
    Вариант подписки.
    """
    name = models.CharField(
        _("Название тарифа"),
        max_length=100,
        unique=True
    )
    price = models.DecimalField(
        _("Цена (₽)"),
        max_digits=8,
        decimal_places=2
    )
    duration = models.PositiveIntegerField(
        _("Длительность (дней)"),
        help_text=_("Число дней, на которые даётся подписка")
    )
    description = models.TextField(
        _("Описание"),
        blank=True
    )

    class Meta:
        verbose_name = _("Тариф")
        verbose_name_plural = _("Тарифы")

    def __str__(self):
        return f"{self.name} — {self.price}₽/{self.duration} дн."


class Subscription(models.Model):
    """
    Активная подписка пользователя.
    """
    user = models.ForeignKey(
    TelegramUser,
    on_delete=models.CASCADE,
    verbose_name=_("Пользователь")
)
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        verbose_name=_("Тариф"),
        null=True,
        blank=True
    )
    start_date = models.DateField(
        _("Дата начала"),
        auto_now_add=True
    )
    end_date = models.DateField(
        _("Дата окончания")
    )
    amount = models.DecimalField(
        _("Сумма платежа"),
        max_digits=8,
        decimal_places=2
    )

    class Meta:
        verbose_name = _("Подписка")
        verbose_name_plural = _("Подписки")

    def save(self, *args, **kwargs):
        if not self.pk and self.plan:
            today = date.today()
            self.start_date = today
            self.end_date = today + timedelta(days=self.plan.duration)
            self.amount = self.plan.price
        super().save(*args, **kwargs)

    def __str__(self):
        plan_name = self.plan.name if self.plan else _("(не указан)")
        return f"{self.user.username}: {plan_name} ({self.start_date}–{self.end_date})"


class PaymentRecord(models.Model):
    """
    История транзакций Telegram.
    """
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        verbose_name=_("Подписка")
    )
    telegram_payment_id = models.CharField(
        _("ID платежа Telegram"),
        max_length=100,
        unique=True
    )
    status = models.CharField(
        _("Статус"),
        max_length=30
    ) 
    created_at = models.DateTimeField(
        _("Дата транзакции"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Запись платежа")
        verbose_name_plural = _("Записи платежей")

    def __str__(self):
        return f"{self.telegram_payment_id} ({self.status})"
