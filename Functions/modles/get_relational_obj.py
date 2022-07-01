from icecream import ic
from rest_framework import serializers


def get_relational(data, app_label):
    from django.apps import apps
    # request.data._mutable = True
    new_dict = {}
    for key, item in data.items():
        if '__' in key:
            x = key.split('.')
            query = x[-1]
            x = x[0]
            query = {query: item}
            x = x.split('__')
            x = x[::-1]
            current_model = apps.get_model(app_label=app_label, model_name=x[0].title())
            try:
                obj = current_model.objects.get(**query)
            except Exception as e:
                raise serializers.ValidationError(f"{e}")
            for i in x[1:]:
                try:
                    obj = getattr(obj, i)
                except Exception as e:
                    raise serializers.ValidationError(f"{e}")
            new_dict[x[-1]] = obj.id
            # request.data.pop(x[-1])
    # for key, item in new_dict.items():
    #     data[key] = item
    return {**data, **new_dict}
    # request.data._mutable = False
