from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views import View 
from django.template.loader import render_to_string 
from .forms import CashflowForm, CashflowEditForm
from .models import (
    Cashflow, 
    CashflowStatus, 
    CashflowType, 
    CashflowCategory, 
    CashflowSubcategory
)
from .services import (
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
                amount = cd.get('amount'),
                comment = cd.get('comment'), 
                cashflow_status = cd.get('cashflow_status'), 
                cashflow_type = cd.get('cashflow_type'), 
                cashflow_category = cd.get('cashflow_category'), 
                cashflow_subcategory = cd.get('cashflow_subcategory')
            )
            new_cashflow.save()
            return redirect('cashflows:cashflows')
        else: 
            form = CashflowForm()
            cashflow_types = CashflowType.objects.all()
            cashflow_statuses = CashflowStatus.objects.all()
            cashflow_categories = CashflowCategory.objects.all() 
            cashflow_subcategories = CashflowSubcategory.objects.all()

            last_cashflows = Cashflow.objects.all()[:10]
            all_cashflows = Cashflow.objects.all()[:100].order_by('-date')

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
    

class EditCashflowView(View): 
    def post(self, request): 
        cashflow_id = request.POST.get('cashflow_id')
        form = CashflowForm(request.POST) 

        if form.is_valid(): 
            cd = form.cleaned_data

            edited_cashflow = Cashflow.objects.get(pk=cashflow_id)

            edited_cashflow.amount = cd.get('amount')
            edited_cashflow.comment = cd.get('comment')

            edited_cashflow.cashflow_status = cd.get('cashflow_status')
            edited_cashflow.cashflow_type = cd.get('cashflow_type')
            edited_cashflow.cashflow_category = cd.get('cashflow_category')
            edited_cashflow.cashflow_subcategory = cd.get('cashflow_subcategory')
            
            edited_cashflow.save()
            return redirect('cashflows:cashflows')
        else: 
            return redirect('cashflows:cashflows')
    


class GetRenderedEditForm(View): 
    def get(self, request, cashflow_id: int): 
        cashflow = Cashflow.objects.get(id=cashflow_id)

        rendered_edit_form = render_to_string(
            template_name = 'cashflows/includes/rendered/edit_form.html', 
            context = {
                'form': CashflowEditForm(instance=cashflow),
                'cashflow_id': cashflow_id
            },
            request=request
        )
        return JsonResponse(rendered_edit_form, safe=False)


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