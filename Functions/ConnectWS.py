from frosty_breeze_25125.asgi import application
from channels.testing import WebsocketCommunicator


async def connectWS(settings, path):
    communicator = WebsocketCommunicator(
        application=application,
        path=path
    )

    connected, _ = await communicator.connect()
    assert connected
    return communicator
