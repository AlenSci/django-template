from django.db.models import Sum, F, Count
from rest_framework import serializers

from dashboard.models import UserRetention


def get_retention(retention, active):
    validations = ['day', 'week', 'month', 'year']
    for i in [retention, active]:
        if i:
            if i not in validations: raise serializers.ValidationError(f'[{i}] is invalid options please select '
                                                                       f'one of {validations}.')
    stats = {}
    if retention:
        q = (
            UserRetention
                .objects
                .values(f'in_date__{retention}')
                .annotate(
                h=Sum(F('out_date') - F('in_date')),
                n=Count('user_id', distinct=True),
            )
        )
        # formating
        l = [
            {
                f'{retention}': x[f'in_date__{retention}'],
                f'avg_duration_per_{retention}': round(x['h'].total_seconds() / (x['n'] * 3600), 2)
            }
            for x in q
        ]
        stats['retention'] = l

    if active:
        q = (
            UserRetention
                .objects
                .values(f'in_date__{active}')
                .annotate(
                n=Count('user_id', distinct=True),
            )
        )
        l = [{'active_users': x['n'], f'{active}': x[f'in_date__{active}']} for x in q]
        stats['active'] = l
    return stats