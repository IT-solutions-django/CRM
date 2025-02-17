from django.db import models
from datetime import date, timedelta
import calendar
from datetime import datetime
from .config import CASHFLOWS_NAMES


class CashflowStatus(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return f'{self.name}'
    
    def get_business_status(): 
        return CashflowStatus.objects.get(name=CASHFLOWS_NAMES.Statuses.BUSINESS) 
    
    def get_tax_status(): 
        return CashflowStatus.objects.get(name=CASHFLOWS_NAMES.Statuses.TAX) 
    
    def get_personal_status(): 
        return CashflowStatus.objects.get(name=CASHFLOWS_NAMES.Statuses.PERSONAL) 


class CashflowType(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Тип'
        verbose_name_plural = 'Тип'

    def __str__(self):
        return f'{self.name}'
    
    def get_income_type(): 
        return CashflowType.objects.get(name=CASHFLOWS_NAMES.Types.INCOMES) 
    
    def get_expense_type(): 
        return CashflowType.objects.get(name=CASHFLOWS_NAMES.Types.EXPENSES)



class CashflowCategory(models.Model): 
    cashflow_type = models.ForeignKey(verbose_name='Тип ДДС', to=CashflowType, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'


class CashflowSubcategory(models.Model): 
    cashflow_category = models.ForeignKey(verbose_name='Категория ДДС', to=CashflowCategory, on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return f'{self.name}'
    

class CashflowManager(models.Manager):    
    def for_current_month(self): 
        date_range = self._get_date_range_for_current_month() 
        return self.filter(created_at__range=date_range)
    
    def for_previous_month(self): 
        date_range = self._get_date_range_for_previous_month() 
        return self.filter(created_at__range=date_range)

    def _get_date_range_for_current_month(self):
        today = date.today()
        first_day = today.replace(day=1)  
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1]) 
        return first_day, last_day
    
    def _get_date_range_for_previous_month(self):
        today = date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        return first_day_of_previous_month, last_day_of_previous_month



class Cashflow(models.Model): 
    created_at = models.DateTimeField('Дата', default=datetime.now) 
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2) 
    comment = models.TextField('Комментарий', null=True, blank=True, max_length=100)
    cashflow_status = models.ForeignKey(verbose_name='Статус', to=CashflowStatus, on_delete=models.CASCADE)
    cashflow_type = models.ForeignKey(verbose_name='Тип', to=CashflowType, on_delete=models.CASCADE)
    cashflow_category = models.ForeignKey(verbose_name='Категория', to=CashflowCategory, on_delete=models.CASCADE)
    cashflow_subcategory = models.ForeignKey(verbose_name='Подкатегория', to=CashflowSubcategory, on_delete=models.CASCADE)

    objects = CashflowManager()

    def is_income(self): 
        return self.cashflow_type.name == CASHFLOWS_NAMES.Types.INCOMES 
    
    def is_expense(self): 
        return self.cashflow_type.name == CASHFLOWS_NAMES.Types.EXPENSES 

    class Meta: 
        verbose_name = 'Движение денежных средств'
        verbose_name_plural = 'ДДС'
        ordering = ['-created_at']

    def __str__(self): 
        return f'{self.cashflow_subcategory.name} | {self.amount}₽ | {self.created_at.strftime("%d.%m.%Y")}'