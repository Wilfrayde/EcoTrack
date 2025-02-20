from datetime import datetime

class RecurringCharge:
    def __init__(self, name: str, amount: float, debit_day: int, id: int = None):
        self.id = id
        self.name = name
        self.amount = amount
        self.debit_day = debit_day  # Jour du mois (1-31) 