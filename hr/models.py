from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime


class TimezoneDifference(models.Model): 
    difference = models.SmallIntegerField('Разница во времени')

    class Meta: 
        verbose_name = 'Разница во времени'
        verbose_name_plural = 'Разница во времени'

    def __str__(self): 
        return f'{self.difference} часов'
    

class HR_Status(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return f'{self.name}'
    

class HR_Position(models.Model): 
    name = models.CharField('Название', max_length=100)

    class Meta: 
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return f'{self.name}'



class HR_Candidate(models.Model): 
    name = models.CharField('Имя', max_length=100) 
    time_difference = models.ForeignKey(verbose_name='Разница во времени', to=TimezoneDifference, on_delete=models.CASCADE) 
    age = models.SmallIntegerField('Возраст', validators=[MinValueValidator(0)])
    position = models.ForeignKey(verbose_name='Позиция', to=HR_Position, on_delete=models.CASCADE) 
    portfolio_link = models.URLField(verbose_name='Ссылка на портфолио', max_length=500, null=True, blank=True) 
    requested_datetime = models.DateTimeField('Дата отклика', default=datetime.now)
    completed_test_task_link = models.URLField(verbose_name='Ссылка на выполненное тестовое задание', null=True, blank=True, max_length=500)
    test_task_given_datetime = models.DateTimeField('Дата, когда кандидату было дано тестовое задание')
    test_task_completed_datetime = models.DateTimeField('Дата выполнения тестового задания', null=True, blank=True) 
    status = models.ForeignKey(verbose_name='Статус', to=HR_Status, on_delete=models.CASCADE)

    class Meta: 
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'

    def __str__(self):
        return f'{self.name} | {self.status}'