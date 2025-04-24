from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from .models import Recipe, Ingredient, RecipeIngredient, RecipeStep


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    fields = ("ingredient", "amount", "unit", "unit_cost")
    autocomplete_fields = ("ingredient",)


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1


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
            "description": _("Добавьте ингредиенты ниже"),
            "fields": (),
        }),
    )

    def display_categories(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    display_categories.short_description = _("Категории")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recalc_cost()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
