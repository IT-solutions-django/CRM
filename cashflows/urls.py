from django.urls import path
from .views import *


app_name = 'cashflows'


urlpatterns = [
    path('', CashflowsView.as_view(), name='cashflows'), 

    path('api/get_categories/<int:cashflow_type_id>/', get_categories, name='get_categories_api'),
    path('api/get_subcategories/<int:cashflow_category_id>/', get_subcategories, name='get_subcategories_api'),
]