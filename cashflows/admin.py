from django.contrib import admin
from .models import (
    Cashflow, 
    CashflowStatus, 
    CashflowType, 
    CashflowCategory, 
    CashflowSubcategory
)


class CashflowCategoryInline(admin.TabularInline):
    model = CashflowCategory
    extra = 1  
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'


class CashflowSubcategoryInline(admin.TabularInline):
    model = CashflowSubcategory
    extra = 1  
    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'


@admin.register(Cashflow)
class CashflowAdmin(admin.ModelAdmin): 
    list_display = [
        'cashflow_subcategory', 
        'cashflow_category', 
        'date', 
        'amount',
        'comment'
    ]


@admin.register(CashflowStatus)
class CashflowStatusAdmin(admin.ModelAdmin): 
    list_display = ['name']


@admin.register(CashflowType)
class CashflowTypeAdmin(admin.ModelAdmin): 
    list_display = ['name']
    inlines = [CashflowCategoryInline]


@admin.register(CashflowCategory)
class CashflowCategoryAdmin(admin.ModelAdmin): 
    list_display = ['name']
    inlines = [CashflowSubcategoryInline]


# @admin.register(CashflowSubcategory)
# class CashflowSubcategoryAdmin(admin.ModelAdmin): 
#     list_display = ['name']