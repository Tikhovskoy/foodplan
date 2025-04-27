from decimal import Decimal, InvalidOperation
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.html import mark_safe
from django.db.models import F, Sum, ExpressionWrapper, DecimalField


class Ingredient(models.Model):
    name = models.CharField(_("Название"), max_length=100)
    unit_cost = models.DecimalField(
        _("Цена за единицу"),
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text=_("Цена за одну единицу ингредиента"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ингредиент")
        verbose_name_plural = _("Ингредиенты")


class RecipeIngredient(models.Model):
    class UnitChoices(models.TextChoices):
        GRAM = 'g', _('грамм')
        MILLILITER = 'ml', _('миллилитр')
        PIECE = 'pcs', _('штука')
        TABLESPOON = 'tbsp', _('столовая ложка')
        TEASPOON = 'tsp', _('чайная ложка')

    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipe_ingredients', verbose_name=_('Рецепт'))
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, verbose_name=_('Ингредиент'))
    amount = models.DecimalField(
        _("Количество"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    unit = models.CharField(_("Единица"), max_length=20, choices=UnitChoices.choices, blank=True)

    class Meta:
        verbose_name = _('Ингредиент в рецепте')
        verbose_name_plural = _('Ингредиенты в рецепте')

    def __str__(self):
        return f"{self.ingredient.name}: {self.amount} {self.get_unit_display()}"

    def get_ingredient_info(self):
        return {
            "name": self.ingredient.name,
            "amount": self.amount,
            "unit": self.get_unit_display()
        }



class Recipe(models.Model):
    title = models.CharField(_("Название блюда"), max_length=200)
    image = models.ImageField(
        _("Изображение блюда"),
        upload_to="recipes/%Y/%m/%d/",
        blank=True,
        null=True,
    )
    estimated_cost = models.DecimalField(
        _("Ориентировочная стоимость"),
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        editable=False,
    )

    is_vegan = models.BooleanField(
        _("Веганское блюдо"),
        default=False,
        help_text=_("Подходит ли блюдо для веганов"),
    )
    is_gluten_free = models.BooleanField(
        _("Без глютена"),
        default=False,
        help_text=_("Не содержит ли блюдо глютен"),
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
        help_text=_("Отображается ли рецепт пользователям"),
    )
    categories = models.ManyToManyField(
        "users.Category",
        verbose_name=_("Категории"),
        blank=True,
    )
    ingredients = models.ManyToManyField(
        "recipes.Ingredient",
        through="recipes.RecipeIngredient",
        related_name="recipes",
        verbose_name=_("Ингредиенты"),
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
        total_cost = Decimal("0.00")

        for recipe_ingredient in self.recipe_ingredients.select_related("ingredient"):
            if recipe_ingredient.ingredient.unit_cost and recipe_ingredient.amount:
                try:
                    total_cost += recipe_ingredient.ingredient.unit_cost * recipe_ingredient.amount
                except (ValueError, TypeError, InvalidOperation):
                    pass

        self.estimated_cost = total_cost
        self.save()

    def get_shopping_lines(self):
        lines = []
        total = Decimal("0.00")
        for ri in self.recipe_ingredients.all():
            cost = ri.ingredient.unit_cost or Decimal("0.00")
            lines.append(f"• {ri.ingredient.name} — {ri.amount} {ri.get_unit_display()}")
            total += ri.amount * cost if ri.amount else Decimal("0.00")
        return lines, total


class RecipeStep(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="steps",
        verbose_name=_("Рецепт"),
    )
    order = models.PositiveIntegerField(_("Порядок шага"))
    text = models.TextField(_("Описание шага"))
    image = models.ImageField(
        _("Изображение шага"), upload_to="recipes/steps/", blank=True, null=True
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("Шаг рецепта")
        verbose_name_plural = _("Шаги рецепта")

    def __str__(self):
        return f"{self.recipe.title}: шаг {self.order}"
