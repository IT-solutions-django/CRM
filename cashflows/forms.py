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

class CashflowEditForm(forms.ModelForm):
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