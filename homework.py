import datetime as dt


class Record:

    date_pattern = '%d.%m.%Y'

    def __init__(self, amount: float, comment: str, date: str = None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, self.date_pattern).date()
        else:
            self.date = dt.date.today()


class Calculator:

    def __init__(self, limit: int):
        self.limit = limit
        self.records = []

    def add_record(self, rec: Record) -> None:
        self.records.append(rec)

    def get_today_stats(self) -> float:
        now = dt.date.today()
        today_stats = sum(r.amount for r in self.records if r.date == now)
        return today_stats

    def get_week_stats(self) -> float:
        now = dt.date.today()
        week = now - dt.timedelta(weeks=1)
        week_stat = sum(r.amount for r in self.records if now >= r.date > week)
        return week_stat

    def get_today_remainder(self) -> float:
        remainder = self.limit - self.get_today_stats()
        return remainder


class CaloriesCalculator(Calculator):

    def get_calories_remained(self) -> str:
        to_eat = self.get_today_remainder()
        msg = ("Сегодня можно съесть что-нибудь ещё, "
               f"но с общей калорийностью не более {to_eat} кКал")
        if to_eat > 0:
            return msg
        return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = 73.4
    EURO_RATE = 87.52

    def get_today_cash_remained(self, currency: str) -> str:
        to_spend = self.get_today_remainder()
        cash_rates = {'rub': [1.0, 'руб'], 'eur': [self.EURO_RATE, 'Euro'],
                      'usd': [self.USD_RATE, 'USD']}
        to_spend = round(to_spend / cash_rates[currency][0], 2)
        curr = cash_rates[currency][1]
        if to_spend == 0:
            return 'Денег нет, держись'
        elif to_spend > 0:
            return f'На сегодня осталось {to_spend} {curr}'
        to_spend = abs(to_spend)
        return f'Денег нет, держись: твой долг - {to_spend} {curr}'
