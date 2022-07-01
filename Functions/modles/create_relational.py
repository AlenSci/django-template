def create_relational(request, pk, path):
    from django.apps import apps
    data = request.data.copy()
    path = path.split('.')
    app_label = path[0]
    model_name = path[2]
    Model = apps.get_model(app_label=app_label, model_name=model_name.title())

    for key, i in data.items():
        field = getattr(Model, key)
        if type(i) is dict and hasattr(field, 'related'):
            object = Model.objects.get(id=pk)
            relation = {model_name: object}

            relational = request.data.pop(key)
            RelationLModel = apps.get_model(app_label=app_label, model_name=key.title())
            obj, created = RelationLModel.objects.get_or_create(**relation)
            for k, i in relational.items():
                setattr(obj, k, i)
            obj.save()