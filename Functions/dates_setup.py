import datetime

from django.utils import timezone



def create_before_date(self, n):
    date_format = '%Y-%m-%d'

    x = timezone.now() - datetime.timedelta(days=n)
    x = x.strftime(date_format)
    setattr(self, f'before_{n}_d', x)


def create_date(self, n):
    date_format = '%Y-%m-%d'

    x = timezone.now() + datetime.timedelta(days=n)
    x = x.strftime(date_format)
    setattr(self, f'after_{n}_d', x)


def create_before_time(self, n):
    time_format = '%H:%M:%S'
    x = timezone.now() - datetime.timedelta(hours=n)
    x = x.strftime(time_format)
    setattr(self, f'before_{n}_h', x)


def create_time(self, n):
    time_format = '%H:%M:%S'
    x = timezone.now() + datetime.timedelta(hours=n)
    x = x.strftime(time_format)
    setattr(self, f'after_{n}_h', x)


def dates_setup(self):
    for i in range(1, 100):
        create_time(self, i)
        create_before_time(self, i)

    for i in range(1, 100):
        create_date(self, i)
        create_before_date(self, i)
