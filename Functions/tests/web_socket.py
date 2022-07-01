import json
import unittest
from unittest.async_case import IsolatedAsyncioTestCase

import pytest
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from pytest_django.fixtures import SettingsWrapper
from pytest_django.lazy_django import skip_if_no_django

from Functions.tests.test_class import makeUsers
from spesific_app_name.asgi import application
from chat.models import Chat


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
class SocketTestClass:
    def settings(self):
        """A Django settings object which restores changes after the testrun"""
        skip_if_no_django()

        wrapper = SettingsWrapper()
        yield wrapper
        wrapper.finalize()

    @database_sync_to_async
    def makeData(self, function, args):
        if type(args) == tuple:
            function(*args)
        elif type(args) == dict:
            function(**args)

    def connect_socket(self, path):
        # settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        # settings.CHANNEL_LAYERS = DATABASES
        communicator = WebsocketCommunicator(
            application=application,
            path=path
        )
        return communicator

    async def receive_socket(self, communicator, attribute='receive_from', r=1):
        x = []
        for i in range(r):
            m = None
            try:
                m = await getattr(communicator, attribute)()
            except Exception as e:
                m = e

            try:
                m = json.loads(m)
            except:
                pass

            x.append(m)

        if len(x) == 1:
            return x[0]
        else:
            return x
