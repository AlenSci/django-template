from django.db import models
from django.utils import timezone
# from safedelete.managers import SafeDeleteManager


# class BaseModelManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_deleted=False)
from safedelete.managers import SafeDeleteManager


class BaseModelQueryset(models.QuerySet):
    def actives(self):
        return self.filter(is_active=True)


class BaseModel(models.Model, SafeDeleteManager):
    created_by = models.ForeignKey('users.User', on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    # deleted_at = models.DateTimeField(null=True, blank=True)
    # is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    # objects = BaseModelManager.from_queryset(BaseModelQueryset)()

    @classmethod
    def get_by_owner(cls, request):
        query = request.GET.get("q")
        if query:
            return cls.objects.filter(owner=query)
        elif request.user.is_authenticated():
            return cls.objects.all()

    class Meta:
        get_latest_by = 'created_at'
        abstract = True

    # def delete(self, using=None, keep_parents=False):
    #     self.deleted_at = timezone.now()
    #     self.is_deleted = True
    #     self.save(update_fields=['deleted_at', 'is_deleted'])
    #     return 1
