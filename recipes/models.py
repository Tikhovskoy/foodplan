# recipes/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Category(models.Model):
    """Категории рецептов"""
    name = models.CharField(_("Название категории"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]

    def __str__(self):
        return self.name

class MealTime(models.Model):
    """Время приёма пищи: Завтрак, Обед, Ужин"""
    name = models.CharField(_("Название времени приёма пищи"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("Время приёма пищи")
        verbose_name_plural = _("Времена приёма пищи")
        ordering = ["name"]

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Рецепты"""
    title = models.CharField(_("Название рецепта"), max_length=200)
    description = models.TextField(_("Описание рецепта"))
    image = models.ImageField(_("Изображение"), upload_to="recipes/", blank=True, null=True)

    is_vegan = models.BooleanField(_("Подходит для веганов"), default=False)
    is_gluten_free = models.BooleanField(_("Без глютена"), default=False)
    budget = models.DecimalField(
        _("Ориентировочная стоимость, ₽"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Необязательное поле для указания стоимости приготовления.")
    )
    is_active = models.BooleanField(_("Активен"), default=True)

    categories = models.ManyToManyField(Category, verbose_name=_("Категории"), blank=True)
    meal_times = models.ManyToManyField(MealTime, verbose_name=_("Время приёма пищи"), blank=True)

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Обновлено"), auto_now=True)

    class Meta:
        verbose_name = _("Рецепт")
        verbose_name_plural = _("Рецепты")
        ordering = ["title"]

    def __str__(self):
        return self.title

class RecipeStep(models.Model):
    """Шаги приготовления"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps", verbose_name=_("Рецепт"))
    text = models.TextField(_("Описание шага"))
    image = models.ImageField(_("Изображение к шагу"), upload_to="recipe_steps/", blank=True, null=True)
    order = models.PositiveIntegerField(_("Порядок выполнения"), default=0)

    class Meta:
        verbose_name = _("Шаг приготовления")
        verbose_name_plural = _("Шаги приготовления")
        ordering = ["order"]

    def __str__(self):
        return f"Шаг {self.order} для {self.recipe.title}"

class Ingredient(models.Model):
    """Ингредиенты рецепта"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients", null=True, blank=True)
    name = models.CharField(_("Название"), max_length=255)
    amount = models.FloatField(_("Количество"), default=1)
    unit = models.CharField(_("Единица измерения"), max_length=50, default="шт")

    class Meta:
        verbose_name = _("Ингредиент")
        verbose_name_plural = _("Ингредиенты")

    def __str__(self):
        return f"{self.name} для {self.recipe.title}"
