from asgiref.sync import sync_to_async
from icecream import ic

from Functions.tests.test_class import makeUsers
from Functions.tests.web_socket import SocketTestClass
from chat.models import Message, Chat


def makeChat(self):
    c = Chat.objects.create(**{"created_by": self.user_1})
    c.users.add(1)
    c.users.add(2)
    c.save()


class TestChat(SocketTestClass):
    async def test_not_in_chat(self):
        await self.makeData(makeUsers, (self,))
        await self.makeData(makeChat, (self,))
        communicator = self.connect_socket(f'chat/1/?token={self.token_3}')
        connected, _ = await communicator.connect()

        res = await self.receive_socket(communicator)
        assert "You are not in this chat room." in str(res)
        await communicator.disconnect()
        ic(res)

    async def test_MessageConsumer_receive(self):
        await self.makeData(makeUsers, (self,))
        await self.makeData(makeChat, (self,))

        communicator_2 = self.connect_socket(f'chat/1/?token={self.token_2}')
        connected, _ = await communicator_2.connect()

        communicator = self.connect_socket(f'chat/1/?token={self.token_1}')
        connected, _ = await communicator.connect()
        await communicator.send_json_to({"message": 'How are you?'})

        res = await self.receive_socket(communicator_2)
        assert 'How are you?' in str(res)
        await communicator.disconnect()
        await communicator_2.disconnect()
        ic('test ok')

    async def test_MessageConsumer_not_receive(self):
        await self.makeData(makeUsers, (self,))
        await self.makeData(Chat.objects.create, {"created_by": self.user_1})
        # 1. connect user 1
        communicator = self.connect_socket(f'chat/1/?token={self.token_1}')
        connected, _ = await communicator.connect()
        assert connected
        m = await sync_to_async(Message.objects.count)()
        assert m == 0

        # user send
        await communicator.send_json_to({"message": 'How are you?'})
        res = await self.receive_socket(communicator)
        assert 'How are you?' not in str(res)

        m = await sync_to_async(Message.objects.count)()
        assert m == 1
        await communicator.disconnect()
