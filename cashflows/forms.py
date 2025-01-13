from django import forms 
from .models import (
    Cashflow, 
    CashflowCategory, 
    CashflowStatus,
    CashflowSubcategory, 
    CashflowType
)
from django.utils import timezone


class CashflowForm(forms.ModelForm):
    cashflow_type = forms.ModelChoiceField(
        queryset=CashflowType.objects.all(),
        label='Тип',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cashflow_category = forms.ModelChoiceField(
        queryset=CashflowCategory.objects.all(),
        label='Категория',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cashflow_subcategory = forms.ModelChoiceField(
        queryset=CashflowSubcategory.objects.all(),
        label='Подкатегория',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cashflow_status = forms.ModelChoiceField(
        queryset=CashflowStatus.objects.all(),
        label='Статус',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cashflow
        fields = [
            'amount', 
            'cashflow_status', 
            'cashflow_type', 
            'cashflow_category', 
            'cashflow_subcategory',
            'comment', 
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите сумму...',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 3, 
                'placeholder': 'Введите комментарий...',
            }),
        }


class CashflowFilterForm(forms.Form): 
    SORT_CHOICES = [
        ('default', '---------'),
        ('cashflow_type', 'Тип (А-Я)'),
        ('-cashflow_type', 'Тип (Я-А)'),
        
        ('cashflow_subcategory', 'Подкатегория (А-Я)'),
        ('-cashflow_subcategory', 'Подкатегория (Я-А)'),

        ('cashflow_category', 'Категория (А-Я)'),
        ('-cashflow_category', 'Категория (Я-А)'),

        ('cashflow_status', 'Статус (А-Я)'),
        ('-cashflow_status', 'Статус (Я-А)'),

        ('amount', 'Сумма (по возрастанию)'),
        ('-amount', 'Сумма (по убыванию)'),

        ('-created_at', 'Сначала новые'), 
        ('created_at', 'Сначала старые'),
    ]
    
    cashflow_type_filter = forms.ModelChoiceField(
        queryset=CashflowType.objects.all(),
        required=False,
        label='Тип',
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'min-width: 100px !important;'})
    )
    cashflow_status_filter = forms.ModelChoiceField(
        queryset=CashflowStatus.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select', 'style': 'min-width: 100px !important;'}), 
    )
    cashflow_category_filter = forms.ModelChoiceField(
        queryset=CashflowCategory.objects.all(),
        required=False,
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cashflow_subcategory_filter = forms.ModelChoiceField(
        queryset=CashflowSubcategory.objects.all(),
        required=False,
        label='Подкатегория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    created_at_min = forms.DateField(
        required=False,
        label='От',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    created_at_max = forms.DateField(
        required=False,
        label='До',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES, 
        required=False, 
        label='Сортировка', 
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
