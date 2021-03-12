import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, rec):
        self.records.append(rec)

    def get_today_stats(self):
        now = dt.datetime.now().date()
        today = sum([rec.amount for rec in self.records if rec.date == now])
        return today

    def get_week_stats(self):
        now = dt.datetime.now().date()
        week = now - dt.timedelta(weeks=1)
        weekly = sum([r.amount for r in self.records if now >= r.date >= week])
        return weekly


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.datetime.now().date()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today = self.get_today_stats()
        to_eat = self.limit - today
        msg = "Сегодня можно съесть что-нибудь ещё, "
        msg += f"но с общей калорийностью не более {to_eat} кКал"
        if to_eat > 0:
            return msg
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):

    USD_RATE = 73.4
    EURO_RATE = 87.52

    def get_today_cash_remained(self, currency):
        today_cash = self.limit - self.get_today_stats()
        curr = 'руб'
        if currency == 'usd':
            today_cash = round(today_cash / self.USD_RATE, 2)
            curr = "USD"
        elif currency == 'eur':
            today_cash = round(today_cash / self.EURO_RATE, 2)
            curr = "Euro"
        if today_cash > 0:
            return f"На сегодня осталось {today_cash} {curr}"
        elif today_cash == 0:
            return "Денег нет, держись"
        today_cash = abs(today_cash)
        return f"Денег нет, держись: твой долг - {today_cash} {curr}"
