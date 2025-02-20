from datetime import datetime

class Income:
    def __init__(self, amount: float, description: str, date: datetime, id: int = None):
        self.id = id
        self.amount = amount
        self.description = description
        self.date = date 