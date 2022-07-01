# from Functions.TestClass import TestClass
# from Functions.login_as import login_as

from Functions.tests.test_class import TestClass
from users.models import User


class TestTrashPerm(TestClass):
    def test_soft_delete(self):
        res = self.client.delete("/users/2/")
        res = self.client.get("/trash/")
        assert res.data["users/User"][0]['id'] == 2

    def test_hard_delete(self):
        res = self.client.delete("/users/2/?hard_delete=true")
        res = self.client.get("/trash/")
        assert len(res.data) == 0

    def test_permissions_retrieve(self):
        User.objects.get(id=3).delete()
        self.login_as()
        prev = User.objects.count()
        res = self.client.post("/trash/users/User/3/")
        assert User.objects.count() == prev
        assert res.status_code == 401

        self.login_as(self.user_1)
        prev = User.objects.count()
        res = self.client.post("/trash/users/User/3/")
        assert User.objects.count() == prev + 1
        assert res.status_code == 200

    def test_permissions(self):
        res = self.client.get("/trash/")
        assert res.status_code == 200

        self.login_as()
        res = self.client.get("/trash/")
        assert res.status_code == 401
