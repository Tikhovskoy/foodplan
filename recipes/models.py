from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.html import mark_safe
from django.db.models import F, Sum, ExpressionWrapper, DecimalField


class Ingredient(models.Model):
    name = models.CharField(_("Название ингредиента"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Ингредиент")
        verbose_name_plural = _("Ингредиенты")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(_("Название блюда"), max_length=200)
    image = models.ImageField(
        _("Изображение блюда"),
        upload_to="recipes/%Y/%m/%d/",
        blank=True,
        null=True
    )
    estimated_cost = models.DecimalField(
        _("Ориентировочная стоимость"),
        max_digits=10, decimal_places=2,
        default=Decimal("0.00"),
        editable=False
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
        help_text=_("Отображается ли рецепт пользователям")
    )
    categories = models.ManyToManyField(
        "users.Category",
        verbose_name=_("Категории"),
        blank=True
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredient",
        related_name="recipes",
        verbose_name=_("Ингредиенты")
    )

    class Meta:
        verbose_name = _("Рецепт")
        verbose_name_plural = _("Рецепты")
        ordering = ["title"]

    def __str__(self):
        return self.title

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height:50px;" />')
        return "-"
    image_preview.short_description = _("Фото")

    def recalc_cost(self):
        total = (
            self.recipeingredient_set
                .aggregate(
                    total=Sum(
                        ExpressionWrapper(
                            F("amount") * F("unit_cost"),
                            output_field=DecimalField()
                        )
                    )
                )
                .get("total") or Decimal("0.00")
        )
        if self.estimated_cost != total:
            self.estimated_cost = total
            self.save(update_fields=["estimated_cost"])

    def get_shopping_lines(self):
        lines = []
        total = Decimal("0.00")
        for ri in self.recipeingredient_set.all():
            cost = ri.unit_cost or Decimal("0.00")
            lines.append(
                f"• {ri.ingredient.name} — {ri.amount} {ri.get_unit_display()}"
            )
            total += ri.amount * cost
        return lines, total

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="steps", verbose_name=_("Рецепт"))
    order = models.PositiveIntegerField(_("Порядок шага"))
    text = models.TextField(_("Описание шага"))
    image = models.ImageField(_("Изображение шага"), upload_to="recipes/steps/", blank=True, null=True)

    class Meta:
        ordering = ["order"]
        verbose_name = _("Шаг рецепта")
        verbose_name_plural = _("Шаги рецепта")

    def __str__(self):
        return f"{self.order}. {self.text[:50]}"

class RecipeIngredient(models.Model):
    UNIT_CHOICES = [
        ("pcs",  _("шт.")),
        ("g",    _("г")),
        ("kg",   _("кг")),
        ("tsp",  _("ч. л.")),
        ("tbsp", _("ст. л.")),
        ("cup",  _("стакан")),
    ]

    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name=_("Блюдо")
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name=_("Ингредиент")
    )
    amount = models.DecimalField(
        _("Количество"),
        max_digits=6, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    unit = models.CharField(
        _("Единица измерения"),
        max_length=10,
        choices=UNIT_CHOICES,
        default="pcs"
    )
    unit_cost = models.DecimalField(
        _("Цена за единицу"),
        max_digits=10, decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    class Meta:
        verbose_name = _("Ингредиент рецепта")
        verbose_name_plural = _("Ингредиенты рецептов")
        unique_together = ("recipe", "ingredient")
        ordering = ["ingredient__name"]

    def __str__(self):
        return f"{self.ingredient.name}: {self.amount} {self.get_unit_display()}"
