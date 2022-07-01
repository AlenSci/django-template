from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from safedelete import HARD_DELETE


def get_data(Model, data):
    class ModelSer(serializers.ModelSerializer):
        class Meta:
            model = Model
            fields = '__all__'

    try:
        return ModelSer(data, many=True).data
    except:
        # ic(data)
        return ''


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser and request.user.is_authenticated)


class Views(APIView):
    permission_classes = [IsSuperUser]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        data = {}
        deleted_items = []
        from django.apps import apps
        for Model in apps.get_models():
            try:
                # deleted_items = queryset_filtering(Model, request.GET)
                deleted_items = Model.objects.all_with_deleted().filter(~Q(deleted=None))
            except:
                pass

            if len(deleted_items) > 0:
                delted_data = get_data(Model, deleted_items)
                link = f'{Model._meta.app_label}/{Model.__name__}'
                data[link] = delted_data
        return Response(data, status=status.HTTP_200_OK)


class View(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        from django.apps import apps
        pk = kwargs.get('pk')
        model = kwargs.get('model')
        app_label = kwargs.get('app_label')
        Model = apps.get_model(app_label, model)
        # data = queryset_filtering(Model, request.GET)
        data = Model.objects.all_with_deleted().filter(Q(~Q(deleted=None) and Q(id=pk)))

        if not data.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = get_data(Model, data)
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        delete for ever
        """
        from django.apps import apps

        pk = kwargs.get('pk')
        model = kwargs.get('model')
        app_label = kwargs.get('app_label')
        Model = apps.get_model(app_label, model)
        # ic('delll')

        items = Model.objects.all_with_deleted().filter(Q(~Q(deleted=None) and Q(id=pk)))

        if not items.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        items.delete(force_policy=HARD_DELETE)
        return Response(get_data(Model, items), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        retreve item (undelete)
        """
        from django.apps import apps

        pk = kwargs.get('pk')
        model = kwargs.get('model')
        app_label = kwargs.get('app_label')
        Model = apps.get_model(app_label, model)
        x = 'spleeeling'
        items = Model.objects.all_with_deleted().filter(Q(~Q(deleted=None) and Q(id=pk)))

        if not items.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        items = items.undelete()
        return Response(get_data(Model, items), status=status.HTTP_200_OK)
