import pytest

class MockApp():
    async def sendMessage(*args, **kwargs):
        return (args, kwargs)

@pytest.fixture
def sender():
    from tlask.helper import Sender
    update = {'message': {'chat': {'id': 'test'}}}
    return Sender(MockApp(), update)

@pytest.mark.async
async def test_sender_send(sender):
    await sender.send("Test")