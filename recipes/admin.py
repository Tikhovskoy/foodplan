from decimal import Decimal
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from .models import Recipe, Ingredient, RecipeIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    verbose_name = _("Ингредиент блюда")
    verbose_name_plural = _("Ингредиенты блюда")
    fields = ('ingredient', 'amount', 'unit', 'unit_cost')

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display      = ('title', 'display_categories', 'estimated_cost')
    list_filter       = ('categories',)
    search_fields     = ('title',)
    filter_horizontal = ('categories',)
    readonly_fields   = ('estimated_cost',)
    inlines           = [RecipeIngredientInline]
    save_on_top       = True

    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'categories', 'estimated_cost'),
        }),
        (_("Ингредиенты"), {
            'classes': ('collapse',),
            'description': _("Добавьте ингредиенты ниже"),
            'fields': (),
        }),
    )

    def display_categories(self, obj):
        return ", ".join(c.name for c in obj.categories.all())
    display_categories.short_description = _("Категории")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        recipe = form.instance
        total = RecipeIngredient.objects.filter(recipe=recipe).aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('amount') * F('unit_cost'),
                    output_field=DecimalField()
                )
            )
        )['total'] or Decimal('0.00')
        if recipe.estimated_cost != total:
            recipe.estimated_cost = total
            recipe.save(update_fields=['estimated_cost'])

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display  = ('name',)
    search_fields = ('name',)
