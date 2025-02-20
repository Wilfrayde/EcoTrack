from datetime import date

class PeriodController:
    @staticmethod
    def get_current_period_start():
        today = date.today()
        if today.day >= 25:
            return date(today.year, today.month, 25)
        if today.month == 1:
            return date(today.year - 1, 12, 25)
        return date(today.year, today.month - 1, 25)

    @staticmethod
    def get_period_end(start_date):
        if start_date.month == 12:
            return date(start_date.year + 1, 1, 24)
        return date(start_date.year, start_date.month + 1, 24)

    @staticmethod
    def get_previous_period_start(current_start):
        if current_start.month == 1:
            return date(current_start.year - 1, 12, 25)
        return date(current_start.year, current_start.month - 1, 25) 