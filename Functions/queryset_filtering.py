from django.db.models import Q


def queryset_filtering(model, queries, and_=True):
    from copy import deepcopy
    queries = deepcopy(queries)
    search = queries.get('search')

    ordering = queries.get("ordering")

    latest = queries.get('latest') == 'true'
    earliest = queries.get('earliest') == 'true'
    abs_latest = queries.get('abs_latest') == 'true'
    abs_earliest = queries.get('abs_earliest') == 'true'

    # TODO make statistics .
    # AllDataStr.objects.annotate(search=SearchVector('name', 'codename')).filter(search='add event')
    filters = Q()
    all_fields = [x.name for x in model._meta.get_fields()]
    fields = [x.name for x in model._meta.fields]
    objects = model.objects.all()
    for k, i in queries.items():
        if i.lower() == 'none':
            queries[k] = None
        if "F('" in str(i):
            queries[k] = eval(i)
        if str(k).title() in ['True', 'False']:
            queries[k] = eval(i.title())
        # if "F('" in str(queries[field]):
        #     queries[field] = eval(queries[field])
        # elif ('gt' or 'lt') in field:
        #     queries[field] = int(queries[field])

        # TODO search by regular expresion
        # if regex in field and  "r('" in queries[field]:
        #     queries[field] = eval(queries[field])

    queries_fields = []
    for field in queries.keys():

        for x in all_fields:
            if x in field:
                queries_fields.append(field)
    for key in queries_fields:
        q = Q(**{key: queries.get(key)})
        if and_:
            filters &= q
        else:
            filters |= q

    if search:
        for key in [x.name for x in model._meta.fields]:
            q = Q(**{f'{key}__icontains': search})
            filters |= q

    objects = objects.filter(Q(filters))

    if ordering:
        objects = objects.order_by(ordering)

    if latest:
        objects = [objects.latest()]

    if earliest:
        objects = [objects.earliest()]

    if abs_latest:
        latest_obj = model.objects.latest()
        if latest_obj in objects:
            objects = [latest_obj]
        else:
            objects = []

    if abs_earliest:
        earliest_obj = model.objects.earliest()
        if earliest_obj in objects:
            objects = [earliest_obj]
        else:
            objects = []

    # for i in objects:
    #     for f in fields:
    #         if getattr(i, f):
    #             delattr(i, f)

    return objects
