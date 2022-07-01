from icecream import ic
from rest_framework.permissions import BasePermission


class RoleBasedPrem(BasePermission):
    def has_permission(self, request, view):
        ic('has_permission')
        method = request._request.method
        if method == "GET": method = 'view'
        if method == "POST": method = 'add'
        if method == "DELETE": method = 'delete'
        if method == "UPDATE": method = 'change'
        model = view.serializer_class.Meta.model.__name__.lower()

        if request.user.user_permissions.filter(codename=f"{method}_{model}"):
            return True

        for g in request.user.groups.all():
            if g.permissions.filter(codename=f"{method}_{model.lower()}"):
                return True

        return False
#
#     def has_object_permission(self, request, view, obj):
#         ic('xxxxxxx')
#         return True

