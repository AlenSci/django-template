import datetime

from django.utils import timezone

from Functions.analytics.annotation import annotation
from Functions.get_users_joinings import GetUsersJoins
from users.models import User


def get_analytics():
    registrations = {
        'day': annotation('date_joined__day', User),
        'week': [],
        'month': []
    }
    try:
        registrations['week'] = annotation('date_joined__week', User)
    except:
        pass
    try:
        registrations['month'] = annotation('date_joined__month', User)
    except:
        pass

    date = timezone.now() + datetime.timedelta(days=7)
    avg_registrations = GetUsersJoins()
    data = {
        "total_users": User.objects.count(),
        "total_new_users": int(User.objects.filter(date_joined__gte=date).count()),
        "registrations": registrations,
        "avg_registrations": avg_registrations,

    }

    return data
