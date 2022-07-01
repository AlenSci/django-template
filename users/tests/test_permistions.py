from django.contrib.auth.models import Permission, Group

from Functions.tests.test_class import TestClass
from users.models import User


class TestBasics(TestClass):
    def perm(self, name, Model):
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Model)
        return Permission.objects.filter(name=name, content_type=content_type).first()

    def add_permition(self, user, permission):
        driver = Group.objects.create(name='driver')
        driver.permissions.add(permission)
        user.groups.add(driver)
        user.save()

    def test_perm(self):
        self.login_as(self.user_2)
        res = self.client.get('/users/')
        assert res.status_code == 403
        self.add_permition(self.user_2, self.perm('Can view user', User))
        res = self.client.get('/users/')
        assert res.status_code == 200

    def test_obj_permissions(self):
        self.login_as(self.user_2)
        res = self.client.get('/users/1/')
        assert res.status_code == 403

        res = self.client.get(f'/users/{self.user_2.id}/')
        assert res.status_code == 200

    def test_obj_permissions_(self):
        self.login_as(self.user_2)
        res = self.client.get('/users/1/')
        assert res.status_code == 403

        self.add_permition(self.user_2, self.perm('Can view user', User))
        res = self.client.get('/users/1/')
        assert res.status_code == 200
