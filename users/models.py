# users/models.py

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class TelegramUser(models.Model):
    """
    Модель для хранения данных каждого Telegram-пользователя бота.
    """
    telegram_id = models.BigIntegerField(
        _("Telegram ID"), primary_key=True
    )
    username = models.CharField(
        _("Username"), max_length=150, blank=True
    )
    first_name = models.CharField(
        _("First name"), max_length=150, blank=True
    )
    last_name = models.CharField(
        _("Last name"), max_length=150, blank=True
    )
    date_joined = models.DateTimeField(
        _("Дата регистрации"), auto_now_add=True
    )

    # Подписка
    paid_until = models.DateField(
        _("Подписка до"), null=True, blank=True
    )
    last_free_recipe = models.DateField(
        _("Последний бесплатный рецепт"), null=True, blank=True
    )

    # Предпочтения
    vegan = models.BooleanField(
        _("Веганское питание"), default=False
    )
    gluten_free = models.BooleanField(
        _("Без глютена"), default=False
    )
    budget = models.DecimalField(
        _("Бюджет, ₽"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Пользователь Telegram")
        verbose_name_plural = _("Пользователи Telegram")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username or str(self.telegram_id)

    def has_active_subscription(self) -> bool:
        """
        Есть ли у пользователя действующая подписка?
        """
        return bool(self.paid_until and self.paid_until >= timezone.now().date())

    def can_get_free_recipe(self) -> bool:
        """
        Можно ли сегодня выдать бесплатный рецепт?
        """
        today = timezone.now().date()
        return not self.last_free_recipe or self.last_free_recipe < today


class Category(models.Model):
    """
    Категории рецептов (например: Завтрак, Обед, Ужин, Веганское, Без глютена и т.д.)
    """
    name = models.CharField(_("Название категории"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]

    def __str__(self):
        return self.name
