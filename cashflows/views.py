from django.shortcuts import render
from django.http import JsonResponse
from django.views import View 
from django.db.models import Sum
from .forms import CashflowForm
from .models import (
    Cashflow, 
    CashflowStatus, 
    CashflowType, 
    CashflowCategory, 
    CashflowSubcategory
)
from .services import (
    CashflowStats, 
    calculate_percentage_difference, 
    generate_stats,
)


class CashflowsView(View): 
    def get(self, request): 
        form = CashflowForm()
        cashflow_types = CashflowType.objects.all()
        cashflow_statuses = CashflowStatus.objects.all()
        cashflow_categories = CashflowCategory.objects.all() 
        cashflow_subcategories = CashflowSubcategory.objects.all()

        last_cashflows = Cashflow.objects.all()[:10]
        all_cashflows = Cashflow.objects.all()[:100]

        stats = generate_stats()

        context = {
            'segment': 'cashflows', 

            'form': form, 
            'newest_cashflows': last_cashflows,
            'all_cashflows': all_cashflows,

            'cashflow_types': cashflow_types, 
            'cashflow_statuses': cashflow_statuses, 
            'cashflow_categories': cashflow_categories, 
            'cashflow_subcategories': cashflow_subcategories,

            'stats': stats
        }
        return render(request, 'cashflows/cashflows.html', context)
    
    def post(self, request): 
        form = CashflowForm(request.POST) 

        if form.is_valid(): 
            cd = form.cleaned_data

            new_cashflow = Cashflow(
                date = cd.get('date'),
                amount = cd.get('amount'),
                comment = cd.get('comment'), 
                cashflow_status = cd.get('cashflow_status'), 
                cashflow_type = cd.get('cashflow_type'), 
                cashflow_category = cd.get('cashflow_category'), 
                cashflow_subcategory = cd.get('cashflow_subcategory')
            )
            new_cashflow.save()

        return JsonResponse(new_cashflow)


def get_categories(request, cashflow_type_id: int) -> JsonResponse: 
    if cashflow_type_id:
        categories = CashflowCategory.objects.filter(cashflow_type_id=cashflow_type_id).values('id', 'name')
        return JsonResponse(list(categories), safe=False)
    return JsonResponse({'error': 'Отсутствует параметр cashflow_type_id'}, status=400)


def get_subcategories(request, cashflow_category_id: int) -> JsonResponse: 
    if cashflow_category_id:
        subcategories = CashflowSubcategory.objects.filter(cashflow_category_id=cashflow_category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse({'error': 'Отсутствует параметр cashflow_category_id'}, status=400)