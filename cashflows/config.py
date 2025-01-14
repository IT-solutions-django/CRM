from enum import Enum


class CASHFLOWS_NAMES: 
    class Statuses:
        BUSINESS = 'Бизнес'
        PERSONAL = 'Личное' 
        TAX = 'Налог'

    class Types: 
        INCOMES = 'Пополнение'
        EXPENSES = 'Списание'

    class Categories: 
        PERSONAL_FROM_STATEMENT = 'Из банковской выписки (физлицо)'
        BUSINESS_FROM_STATEMENT = 'Из банковской выписки (ИП)'

    class Subcategories: 
        BUSINESS_FROM_STATEMENT = 'Из банковской выписки (ИП)'