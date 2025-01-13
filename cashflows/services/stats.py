from decimal import Decimal
from django.db.models import Sum
from django.db.models import QuerySet
from django.db.models.query import QuerySet

from ..models import (
    Cashflow, 
    CashflowType, 
    CashflowCategory, 
    CashflowSubcategory
)
from ..config import CASHFLOWS_NAMES


class CashflowStats: 
    """Подсчитывает сумму ДДС по разным критериям за текущий или прошлый месяц"""
    class CurrentMonth: 
        def get_incomes() -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_type__name=CASHFLOWS_NAMES.Types.INCOMES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        def get_expenses() -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        def get_business_incomes() -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.BUSINESS, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.INCOMES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_business_expenses() -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.BUSINESS, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_tax_expenses() -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.TAX, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_personal_expenses() -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.PERSONAL, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)

        def get_category_amount(category: QuerySet) -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_category=category, 
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)   

        def get_subcategory_amount(subcategory: QuerySet) -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                cashflow_subcategory=subcategory, 
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)  

    class PreviousMonth: 
        def get_incomes() -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_type__name=CASHFLOWS_NAMES.Types.INCOMES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        def get_expenses() -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        def get_business_incomes() -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.BUSINESS, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.INCOMES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_business_expenses() -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.BUSINESS, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_tax_expenses() -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.TAX, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_personal_expenses() -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_status__name=CASHFLOWS_NAMES.Statuses.PERSONAL, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0)  
        
        def get_category_amount(category: QuerySet) -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_category=category, 
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_subcategory_amount(subcategory: QuerySet) -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                cashflow_subcategory=subcategory, 
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 


def calculate_percentage_difference(old_amount, new_amount) -> float: 
    """Считает, на сколько процентов новая сумма отличается от старой"""
    old_amount = Decimal(old_amount)
    new_amount = Decimal(new_amount)

    if old_amount  == 0:
        if new_amount  == 0:
            return 0
        else:
            return 100
    percentage = ((new_amount - old_amount) / old_amount) * 100
    return percentage if percentage > 0 else percentage


def generate_stats() -> dict: 
    """Генерирует общую статистику"""
    cashflow_types = CashflowType.objects.all()
    cashflow_categories = CashflowCategory.objects.all()
    cashflow_subcategories = CashflowSubcategory.objects.all()

    curr = CashflowStats.CurrentMonth
    prev = CashflowStats.PreviousMonth

    curr_business_incomes = curr.get_business_incomes()
    prev_business_incomes = prev.get_business_incomes()

    curr_business_expenses = curr.get_business_expenses()
    prev_business_expenses = prev.get_business_expenses()

    curr_tax_expenses = curr.get_tax_expenses()
    prev_tax_expenses = prev.get_tax_expenses()

    curr_personal_expenses = curr.get_personal_expenses()
    prev_personal_expenses = prev.get_personal_expenses()

    category_cache = {
        category.pk: {
            'curr': curr.get_category_amount(category.pk),
            'prev': prev.get_category_amount(category.pk)
        }
        for category in cashflow_categories
    }
    subcategory_cache = {
        subcategory.pk: {
            'curr': curr.get_subcategory_amount(subcategory.pk),
            'prev': prev.get_subcategory_amount(subcategory.pk)
        }
        for subcategory in cashflow_subcategories
    }
    type_cache = {
        'incomes': {
            'curr': curr.get_incomes(), 
            'prev': prev.get_incomes(),
        },
        'expenses': {
            'curr': curr.get_expenses(), 
            'prev': prev.get_expenses(),
        }
    }

    stats = {
        'business_incomes': {
            'absolute': curr_business_incomes,
            'relative': calculate_percentage_difference(prev_business_incomes, curr_business_incomes),
            'prev_month': prev_business_incomes,
        },
        'business_expenses': {
            'absolute': curr_business_expenses, 
            'relative': calculate_percentage_difference(prev_business_expenses, curr_business_expenses),
            'prev_month': prev_business_expenses,
        },
        'tax_expenses': {
            'absolute': curr_tax_expenses, 
            'relative': calculate_percentage_difference(prev_tax_expenses, curr_tax_expenses),
            'prev_month': prev_tax_expenses,
        },
        'personal_expenses': {
            'absolute': curr_personal_expenses, 
            'relative': calculate_percentage_difference(prev_personal_expenses, curr_personal_expenses),
            'prev_month': prev_personal_expenses,
        },
        'types': [
            {
                'name': CASHFLOWS_NAMES.Types.INCOMES, 
                'absolute': type_cache['incomes']['curr'], 
                'relative': calculate_percentage_difference(
                    old_amount=type_cache['incomes']['prev'], 
                    new_amount=type_cache['incomes']['curr'],
                ), 
                'prev_month': type_cache['incomes']['prev']
            },
            {
                'name': CASHFLOWS_NAMES.Types.EXPENSES, 
                'absolute': type_cache['expenses']['curr'], 
                'relative': calculate_percentage_difference(
                    old_amount=type_cache['expenses']['prev'], 
                    new_amount=type_cache['expenses']['curr'],
                ), 
                'prev_month': type_cache['expenses']['prev']
            },
        ], 
        'categories': [
            {
                'name': cashflow_category.name,
                'absolute': category_cache[cashflow_category.pk]['curr'], 
                'relative': calculate_percentage_difference(
                    old_amount=category_cache[cashflow_category.pk]['prev'], 
                    new_amount=category_cache[cashflow_category.pk]['curr']
                ), 
                'prev_month': category_cache[cashflow_category.pk]['prev'],
            }   
            for cashflow_category in cashflow_categories
        ],
        'subcategories': [
            {
                'name': cashflow_subcategory.name,
                'absolute': subcategory_cache[cashflow_subcategory.pk]['curr'], 
                'relative': calculate_percentage_difference(
                    old_amount=subcategory_cache[cashflow_subcategory.pk]['prev'], 
                    new_amount=subcategory_cache[cashflow_subcategory.pk]['curr']
                ), 
                'prev_month': subcategory_cache[cashflow_subcategory.pk]['prev'],
            } for cashflow_subcategory in cashflow_subcategories
        ],
    }
    return stats