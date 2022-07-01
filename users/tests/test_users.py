from django.contrib.auth.models import Group
from icecream import ic

from Functions.tests.test_class import TestClass
from alerts.models import Alert
from users.models import User


class TestBasics(TestClass):
    # def test_relational(self):
    #     # redis-server
    #     res = self.client.post('/alerts/', {'user__name': self.user_1.name})
    #     # assert res.status_code == 201
    #     self.printJ(res.data)

    def test_relational_dynamic_serializer(self):
        driver = Group.objects.create(name='driver')
        self.user_1.groups.add(driver)
        self.user_1.save()

        res = self.client.get('/users/?query={username, groups}')
        # self.printJ(res.data[0])
        assert res.data[0]['groups'] == [1]

        # res = self.client.get('/users/?query={username, groups{name, id}}')
        # assert res.data[0]['groups'] == {'name': driver, "id": 1}
        # self.printJ(res.data)

    def test_pagination(self):
        res = self.client.get('/users/')
        assert len(res.data) > 2
        res = self.client.get('/users/?from=1&to=3')
        assert len(res.data) == 2

    def test_dynamic_fields(self):
        res = self.client.get('/users/')
        assert res.data[0].get('email') is not None
        res = self.client.get('/users/?query={id,username,first_name}')
        assert res.data[0].get('email') is None

    def test_annotate(self):
        res = self.client.get('/users/?annotate=date_joined__day')
        self.printJ(res.data)
        # ic(res.status_code, res.data)

    def test_number_of_users(self):
        res = self.client.get('/users/')
        assert "count" not in res.data
        res = self.client.get('/users/?count=true')
        assert "count" in res.data
        assert res.data['count'] == 3

    def test_queryset_filtering(self):
        res = self.client.get('/users/')
        assert res.data[0]['id'] == 1
        res = self.client.get('/users/?id__gt=2')
        assert res.data[0]['id'] == 3
        assert res.status_code == 200

    # def test_passing_address_and_phone(self):
    #     params = {
    #         'phone_number': '103049',
    #         'address': {'street': 'ssss', 'city': 'cccc', 'state': 'xxx'},
    #     }
    #     res = self.client.put('/users/1/', params)
    #     assert res.status_code == 200
    #     assert res.data['address']['street'] == 'ssss'

    def test_permissions(self):
        self.login_as(self.user_1)
        res = self.client.get('/users/1/')
        assert res.status_code == 200

        self.login_as(self.user_2)
        res = self.client.get('/users/1/')
        assert res.status_code == 403

    def test_image_decoder(self):
        photo = 'data:image/png;base64,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'

        params = {
            # 'phone_number': '103049',
            # 'address': {'street': 'ssss', 'city': 'cccc', 'state': 'xxx'},
            'photo': photo,
        }
        assert not User.objects.get(id=self.user_1.id).photo
        res = self.client.put('/users/1/', params)
        assert res.status_code == 200
        assert User.objects.get(id=self.user_1.id).photo
        assert res.status_code == 200

    # def test_signup(self):
    # User.objects.create(username=self.user_1.username)
    # User.objects.create(username='ali3')
    # perams = {
    #     'username': 'ali',
    #     'email': 'weplutus.1@gmail.com',
    #     'password': 'Password123',
    # }
    # res = self.client.post('/rest-auth/signup/', perams)
    # assert res.status_code == 201
    #
    # perams = {
    #     'username': 'ali',
    #     'email': 'newemail@gmail.com',
    #     'password': 'Password123',
    # }
    # res = self.client.post('/rest-auth/signup/', perams)
    # ic(res.status_code, res.data)

    # def test_upload_photo(self):
    #     image = Image.new('RGBA', size=(50, 50), color=(256, 0, 0))
    #     image_file = BytesIO()
    #     image.save(image_file, 'PNG')  # or whatever format you prefer
    #     # file = ImageFile(image_file)
    #     # u = User.objects.last()
    #     # u.photo = file
    #     # u.save()
    #     params = {
    #         'photo': image,
    #     }
    #     res = self.client.put('/users/1/', params)
    #     ic(res.status_code, res.data)
    #     # assert res.status_code == 200
