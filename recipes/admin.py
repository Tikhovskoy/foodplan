# recipes/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from .models import Recipe, Ingredient, RecipeStep, Category, MealTime

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1
    fields = ("name", "amount", "unit")
    verbose_name = _("Ингредиент")
    verbose_name_plural = _("Ингредиенты")

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1
    fields = ("order", "text", "image")
    ordering = ("order",)
    verbose_name = _("Шаг приготовления")
    verbose_name_plural = _("Шаги приготовления")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(MealTime)
class MealTimeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title", "image_preview",
        "is_vegan", "is_gluten_free", "budget", "is_active",
        "display_categories", "display_meal_times",
    )
    list_filter = ("is_vegan", "is_gluten_free", "is_active", "categories", "meal_times")
    search_fields = ("title",)
    filter_horizontal = ("categories", "meal_times")
    readonly_fields = ("created_at", "updated_at", "image_preview")
    inlines = [IngredientInline, RecipeStepInline]
    save_on_top = True

    fieldsets = (
        (None, {
            "fields": (
                "title", "description", "image", "image_preview",
                "is_vegan", "is_gluten_free",
                "budget", "is_active", "categories", "meal_times",
            ),
        }),
        (_("Ингредиенты и шаги"), {
            "classes": ("collapse",),
            "description": _("Добавьте ингредиенты и шаги ниже"),
            "fields": (),
        }),
    )

    def display_categories(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    display_categories.short_description = _("Категории")

    def display_meal_times(self, obj):
        return ", ".join(m.name for m in obj.meal_times.all())
    display_meal_times.short_description = _("Время приёма пищи")

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')
        return _("Нет изображения")
    image_preview.short_description = _("Превью изображения")
