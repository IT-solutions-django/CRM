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
        PERSONAL = 'Личные потребности'
        BUSINESS = 'Бизнес'