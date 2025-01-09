from django.db import models


class CashflowStatus(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return f'{self.name}'


class CashflowType(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Тип'
        verbose_name_plural = 'Тип'

    def __str__(self):
        return f'{self.name}'


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


class Cashflow(models.Model): 
    date = models.DateField('Дата') 
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2) 
    comment = models.TextField('Комментарий', null=True, blank=True)
    cashflow_status = models.ForeignKey(verbose_name='Статус', to=CashflowStatus, on_delete=models.CASCADE)
    cashflow_type = models.ForeignKey(verbose_name='Тип', to=CashflowType, on_delete=models.CASCADE)
    cashflow_category = models.ForeignKey(verbose_name='Категория', to=CashflowCategory, on_delete=models.CASCADE)
    cashflow_subcategory = models.ForeignKey(verbose_name='Подкатегория', to=CashflowSubcategory, on_delete=models.CASCADE)

    class Meta: 
        verbose_name = 'Движение денежных средств'
        verbose_name_plural = 'ДДС'
        ordering = ['-date']