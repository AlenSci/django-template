from icecream import ic
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from safedelete import HARD_DELETE

from Functions.analytics.annotation import annotation
from Functions.decode_base64_file import decode_base64_file
from Functions.queryset_filtering import queryset_filtering


def convert_to_list(django_object):
    flat_object = django_object.values_list('codename', flat=True)
    return list(flat_object)


class ItemsView(generics.ListAPIView, APIView):
    def check_permissions(self, request):
        if request.user.is_superuser or request.user.is_staff: return True

        method = request._request.method
        if method == "GET": method = 'view'
        if method == "POST": method = 'add'
        if method == "DELETE": method = 'delete'
        if method == "UPDATE": method = 'change'
        model = self.serializer_class.Meta.model.__name__.lower()

        if request.user.user_permissions.filter(codename=f"{method}_{model}"):
            return True

        for g in request.user.groups.all():
            if g.permissions.filter(codename=f"{method}_{model.lower()}"):
                return True

        # return False
        self.permission_denied(
            request,
            # message=getattr(permission, 'message', None),
            # code=getattr(permission, 'code', None)
        )

    def get_queryset(self, *args, **kwargs):
        objects = queryset_filtering(self.queryset.model, self.request.GET)
        return objects

    def pagination(self, data):
        queries = self.request.GET

        from_ = queries.get('from')
        to_ = queries.get('to')
        if from_: from_ = int(from_)
        if to_: to_ = int(to_)
        data = data[from_:to_]
        return data

    def get(self, request, *args, **kwargs):
        Model = self.queryset.model
        annotate = request.GET.get('annotate')
        count = request.GET.get('count')

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        data = self.pagination(data)

        if annotate: return Response(annotation(annotate, Model), status=status.HTTP_200_OK)
        if str(count).lower() == 'true': return Response({'data': data, "count": len(data)}, status=status.HTTP_200_OK)
        return Response(data)

    def handle_data(self, data):
        data = decode_image_field(data, 'photo')
        # data = get_relational(data, self.queryset.model.__module__)
        return data

    def post(self, request):
        data = self.handle_data(request.data)
        ic(data);
        ic()
        self.check_object_permissions(request, data)

        serializer = self.serializer_class(data={**data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(mixins.CreateModelMixin, generics.GenericAPIView):

    # def get_object(self, pk, *args, **kwargs):
    #     Model = self.serializer_class.Meta.model
    #     try:
    #         obj = Model.objects.get(id=pk)
    #         # if hasattr(self, 'object_perm') and not self.request.user.is_superuser:
    #         #     is_ = True
    #         #     perm = self.object_perm(self.request)
    #         #     for k, v, in perm.items():
    #         #         is_ &= getattr(obj, k) == v
    #         #     if not is_: raise PermissionDenied()
    #         return obj
    #     except Model.DoesNotExist:
    #         raise Http404

    def check_object_permissions(self, request, obj):
        if request.user.is_superuser or request.user.is_staff: return True
        method = request._request.method
        if method == "GET": method = 'view'
        if method == "POST": method = 'add'
        if method == "DELETE": method = 'delete'
        if method == "UPDATE": method = 'change'
        model = self.serializer_class.Meta.model.__name__.lower()

        if request.user.user_permissions.filter(codename=f"{method}_{model}"): return True

        for g in request.user.groups.all():
            if g.permissions.filter(codename=f"{method}_{model.lower()}"): return True

        if hasattr(self, "object_permissions") and self.object_permissions(request, obj): return True

        self.permission_denied(request)

    def get(self, request, pk, format=None):
        context = {'request': request, 'method': 'view', 'pk': pk}
        item = self.get_object()
        serializer = self.serializer_class(item, many=False, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        """
        #Note:
        When you delete an object it will not actually be deleted but instead it will go to the trash pin.
        To delete something for ever add `?hard_delete=true` in the query string.
        Or go to try client.DELETE(`/trash/{app_label}/{model}/{id}/`) after deleting the item.
        """
        hard_delete = request.GET.get('hard_delete', '').title() == 'True'
        item = self.get_object()
        if hard_delete:
            item.delete(force_policy=HARD_DELETE)
        else:
            item.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        data = request.data
        # create_relational(request, pk, self.queryset.model.__module__)
        data = decode_image_field(data, 'photo')
        # data = get_relational(data, self.queryset.model.__module__)
        date = self.get_object()
        serializer = self.serializer_class(date, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def decode_image_field(data, name):
    photo = data.get(name)
    if type(photo) is str:
        return {**data, name: decode_base64_file(photo)}
    return data
