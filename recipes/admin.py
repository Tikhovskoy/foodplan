from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe

from .models import Recipe, Ingredient, RecipeIngredient, RecipeStep

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    fields = ("ingredient", "amount", "unit")
    autocomplete_fields = ("ingredient",)
    verbose_name = _("Ингредиент")
    verbose_name_plural = _("Ингредиенты")

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1
    fields = ("order", "text", "image")
    ordering = ("order",)
    verbose_name = _("Шаг приготовления")
    verbose_name_plural = _("Шаги приготовления")

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "display_categories", "estimated_cost")
    list_filter = ("categories",)
    search_fields = ("title",)
    filter_horizontal = ("categories",)
    readonly_fields = ("estimated_cost", "image_preview")
    inlines = [RecipeIngredientInline, RecipeStepInline]
    save_on_top = True

    fieldsets = (
        (None, {
            "fields": ("title", "image", "image_preview", "categories", "estimated_cost"),
        }),
        (_("Ингредиенты"), {
            "classes": ("collapse",),
            "description": _("Добавьте ингредиенты в блоке ниже"),
            "fields": (),
        }),
        (_("Шаги приготовления"), {
            "classes": ("collapse",),
            "description": _("Добавьте пошаговое описание рецепта"),
            "fields": (),
        }),
    )

    def display_categories(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    display_categories.short_description = _("Категории")

    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')
        return _("Нет изображения")
    image_preview.short_description = _("Превью изображения")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recalc_cost()

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
