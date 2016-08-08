import pytest

#local import
import config

@pytest.fixture
def api():
    from tlask.api import Api
    return Api(config.token)

@pytest.mark.asyncio
async def test_getMe(api):
    assert await api.getMe() == {'username': 'PingiunTestingBot', 'id': 255364908, 'first_name': 'Pingiun Testing Bot'}

@pytest.mark.asyncio
async def test_sendMessage(api):
    message = await api.sendMessage(config.testuser, 'If you receive this message the framework is working.')
    assert message['text'] == 'If you receive this message the framework is working.'