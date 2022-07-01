from django.db.models import Avg, Count
from django.db.models.functions import ExtractYear, ExtractWeek, ExtractMonth

from users.models.user import User


def GetUsersJoins():
    key = 'date_joined'
    cals = {}

    stats = (User.objects
             .annotate(week=ExtractWeek(key))
             .values('week')
             .annotate(number=Count('id'))
             .aggregate(Avg('number'))
             )
    avg = dict(stats)['number__avg']
    cals['weekly'] = avg

    stats = (User.objects
             .annotate(month=ExtractMonth(key))
             .values('month')
             .annotate(number=Count('id'))
             .aggregate(Avg('number'))
             )
    avg = dict(stats)['number__avg']
    cals['monthly'] = avg

    stats = (User.objects
             .annotate(year=ExtractYear(key))
             .values('year')
             .annotate(number=Count('id'))
             .aggregate(Avg('number'))
             )
    avg = dict(stats)['number__avg']
    cals['yearly'] = avg
    return cals
