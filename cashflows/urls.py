from django.urls import path
from .views import *


app_name = 'cashflows'


urlpatterns = [
    path('', CashflowsView.as_view(), name='cashflows'), 
    path('edit-cashflow', EditCashflowView.as_view(), name='edit_cashflow'),

    path('api/get_rendered_edit_form/<int:cashflow_id>/', GetRenderedEditForm.as_view(), name='get_rendered_edit_form'),

    path('api/get_categories/<int:cashflow_type_id>/', get_categories, name='get_categories_api'),
    path('api/get_subcategories/<int:cashflow_category_id>/', get_subcategories, name='get_subcategories_api'),

    path('api/test_stats/', test_stats_api.as_view(), name='test_stats'),
]