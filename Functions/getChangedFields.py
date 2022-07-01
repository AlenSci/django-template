from icecream import ic


def get_changed_fields(sender, instance):
    from rest_framework import serializers

    olds = {}
    news = {}

    obj = sender.objects.filter(id=instance.id).first()

    class DateSer(serializers.ModelSerializer):
        class Meta:
            model = sender
            fields = '__all__'

    if obj:
        new_data = DateSer(instance, many=False).data
        old_data = DateSer(obj, many=False).data

        for key in old_data.keys():
            new = new_data[key]
            old = old_data[key]
            if new != old:
                olds[key] = old
                news[key] = new
        return {'old data': olds, 'new data': news}
