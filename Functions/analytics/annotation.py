from django.db.models import Count
from django.db.models.functions import TruncDay


def annotation(annotate, Model):
    annotate = annotate.split('__')
    date = annotate[1]
    field = annotate[0]

    annotation = Model.objects \
        .values(day=TruncDay(field)) \
        .annotate(total_objects=Count(field)) \
        .order_by(f'-{date}')
    return list(annotation)