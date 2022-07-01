from channels.db import database_sync_to_async
from icecream import ic

from Functions.tests.test_class import makeUsers
from Functions.tests.web_socket import SocketTestClass
from alerts.models.alert import Alert
from chat.models import Chat


# @database_sync_to_async
# def asset_is_read(id, val):
#     assert Alert.objects.get(id=id).is_read == val


class TestNotifications(SocketTestClass):
    async def test_receive_notifications(self):
        await self.makeData(makeUsers, (self,))
        await self.makeData(Chat.objects.create, {"created_by": self.user_1})

        communicator = self.connect_socket(f'alerts/?token={self.token_1}')
        connected, _ = await communicator.connect()
        assert connected
        await self.makeData(Alert.objects.create, {"user": self.user_1, "is_read": False})

        res = await self.receive_socket(communicator, 'receive_from', 1)
        assert res['user'] == self.user_1.id
        assert res['is_read'] is False
        ic('it is working')
        await communicator.disconnect()

    # async def test_is_read(self, settings):
    #     await createTestData(self)
    #
    #     communicator = connect_socket(settings, f'alerts/?token={self.token_1}')
    #     connected, _ = await communicator.connect()
    #     assert connected
    #     await make_alert(self)
    #     res = await receive_socket(communicator, 'receive_from', 1)
    #     await asset_is_read(res['id'], False)
    #     await communicator.send_json_to({"is_read": 'true', 'id': res['id']})
    #     res_2 = await receive_socket(communicator, 'receive_from', 1)
    #     assert "is read by user with id" in str(res_2)
    #     await asset_is_read(res['id'], True)
    #
    #     await communicator.disconnect()
    #
    # async def test_invalid_token(self, settings):
    #     await createTestData(self)
    #
    #     communicator = connect_socket(settings, f'alerts/?token=abcd')
    #     connected, _ = await communicator.connect()
    #     assert connected
    #     res = await receive_socket(communicator, 'receive_from', 1)
    #     assert 'Invalid token.' in str(res)
    #     await communicator.disconnect()
