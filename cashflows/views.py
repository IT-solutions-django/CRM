from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View 
from django.template.loader import render_to_string

from cashflows.services.xlsx_parser import load_cashflows_from_file 
from .forms import (
    CashflowForm, 
    CashflowFilterForm,
    BankStatementForm,
)
from .models import (
    Cashflow, 
    CashflowStatus, 
    CashflowType, 
    CashflowCategory, 
    CashflowSubcategory
)
from .services.pagination import get_paginated_collection
from .services.stats import generate_stats


class CashflowsView(View): 
    def get(self, request): 
        create_cashflow_form = CashflowForm()
        filter_form = CashflowFilterForm(request.GET)
        bank_statement_form = BankStatementForm()
        cashflow_types = CashflowType.objects.all()
        cashflow_statuses = CashflowStatus.objects.all()
        cashflow_categories = CashflowCategory.objects.all() 
        cashflow_subcategories = CashflowSubcategory.objects.all()
        stats = generate_stats()

        cashflows = Cashflow.objects.all()
        if filter_form.is_valid():
            cd = filter_form.cleaned_data
            if cd['cashflow_type_filter']:
                cashflows = cashflows.filter(cashflow_type=cd['cashflow_type_filter'])
            if cd['cashflow_status_filter']:
                cashflows = cashflows.filter(cashflow_status=cd['cashflow_status_filter'])
            if cd['cashflow_category_filter']:
                cashflows = cashflows.filter(cashflow_category=cd['cashflow_category_filter'])
            if cd['cashflow_subcategory_filter']:
                cashflows = cashflows.filter(cashflow_subcategory=cd['cashflow_subcategory_filter'])
            if cd['created_at_min']:
                cashflows = cashflows.filter(created_at__gte=cd['created_at_min'])
            if cd['created_at_max']:
                cashflows = cashflows.filter(created_at__lte=cd['created_at_max'])
            if cd['sort_by']: 
                if cd['sort_by'] != 'default':
                    cashflows = cashflows.order_by(cd['sort_by'])
                    print(cashflows)


        cashflows = get_paginated_collection(
            request=request, collection=cashflows, 
            count_per_page=5
        )

        context = {
            'segment': 'cashflows', 

            'form': create_cashflow_form,
            'filter_form': filter_form, 
            'bank_statement_form': bank_statement_form,

            'all_cashflows': cashflows,

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
            create_cashflow_form = CashflowForm()
            filter_form = CashflowFilterForm(request.GET)
            bank_statement_form = BankStatementForm()
            cashflow_types = CashflowType.objects.all()
            cashflow_statuses = CashflowStatus.objects.all()
            cashflow_categories = CashflowCategory.objects.all() 
            cashflow_subcategories = CashflowSubcategory.objects.all()

            stats = generate_stats()

            cashflows = get_paginated_collection(
                request=request, collection=cashflows, 
                count_per_page=5
            )

            context = {
                'segment': 'cashflows', 

                'form': create_cashflow_form,
                'filter_form': filter_form, 
                'bank_statement_form': bank_statement_form,

                'all_cashflows': cashflows,

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

        print(request.POST)

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

            query_params = request.GET.urlencode()
            redirect_url = reverse('cashflows:cashflows')  
            full_redirect_url = f"{redirect_url}?{query_params}" if query_params else redirect_url

            return HttpResponseRedirect(full_redirect_url)
        else: 
            return redirect('cashflows:cashflows')
        

class LoadBankStatementView(View): 
    def post(self, request): 
        xlsx_file = request.FILES['xlsx_file'] 
        
        load_cashflows_from_file(xlsx_file)

        return redirect('cashflows:cashflows')



class GetRenderedEditForm(View): 
    def get(self, request, cashflow_id: int): 
        cashflow = Cashflow.objects.get(id=cashflow_id)

        rendered_edit_form = render_to_string(
            template_name = 'cashflows/includes/rendered/edit_form.html', 
            context = {
                'form': CashflowForm(instance=cashflow),
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




class StatsAPIView(View): 
    def get(self, request): 
        stats = generate_stats()

        return JsonResponse(data=stats)