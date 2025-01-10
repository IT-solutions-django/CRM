from decimal import Decimal
from django.db.models import Sum
from django.db.models import QuerySet
from datetime import date, timedelta
import calendar

from .models import (
    Cashflow, 
    CashflowCategory, 
    CashflowStatus, 
    CashflowType, 
    CashflowSubcategory
)
from .config import CASHFLOWS_NAMES


class CashflowStats: 
    """Подсчитывает сумму ДДС по разным критериям за текущий или прошлый месяц"""
    class CurrentMonth: 
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
        
        def get_category_incomes(category: QuerySet) -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                category=category, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.INCOMES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_category_expenses(category: QuerySet) -> Decimal: 
            return Cashflow.objects.for_current_month().filter(
                category=category, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 

    class PreviousMonth: 
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
        
        def get_category_incomes(category: QuerySet) -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                category=category, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.INCOMES,
            ).aggregate(Sum('amount')).get('amount__sum') or Decimal(0) 
        
        def get_category_expenses(category: QuerySet) -> Decimal: 
            return Cashflow.objects.for_previous_month().filter(
                category=category, 
                cashflow_type__name=CASHFLOWS_NAMES.Types.EXPENSES,
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

    stats = {
        'curr_month': {
            'business_incomes': {
                'absolute': curr_business_incomes,
                'relative': calculate_percentage_difference(prev_business_incomes, curr_business_incomes),
            },
            'business_expenses': {
                'absolute': curr_business_expenses, 
                'relative': calculate_percentage_difference(prev_business_expenses, curr_business_expenses),
            },
            'tax_expenses': {
                'absolute': curr_tax_expenses, 
                'relative': calculate_percentage_difference(prev_tax_expenses, curr_tax_expenses),
            },
            'personal_expenses': {
                'absolute': curr_personal_expenses, 
                'relative': calculate_percentage_difference(prev_personal_expenses, curr_personal_expenses)
            }
        }
    }
    return stats