import pytest

import tempfile
import os
import json
from random import choice

#local import
import config


@pytest.fixture
def api():
    from tlask.api import Api
    return Api(choice(config.token))


@pytest.mark.asyncio
async def test_getMe(api):
    assert await api.getMe() is not None

@pytest.mark.asyncio
async def test_sendMessage(api):
    message = await api.sendMessage(
        config.testuser,
        'If you receive this *message* the framework is working. https://google.com',
        parse_mode='markdown', disable_web_page_preview=True, reply_markup={'keyboard': [['/start']]}, disable_notification=True)
    assert message[
        'text'] == 'If you receive this message the framework is working. https://google.com'


@pytest.mark.asyncio
async def test_reply_to_message(api):
    message = await api.sendMessage(
        config.testuser,
        'This is a test reply',
        reply_to_message_id=1, parse_mode='markdown', disable_web_page_preview=True, reply_markup={'keyboard': [['/start']]},
        disable_notification=True)
    assert message['text'] == 'This is a test reply'


@pytest.mark.asyncio
async def test_forwardMessage(api):
    forwardmessage = await api.forwardMessage(
        config.testuser, config.testuser, 1, disable_notification=True
    )
    assert forwardmessage['text'] == '/start'


@pytest.mark.asyncio
async def test_sendLocation(api):
    message = await api.sendLocation(
        config.testuser, 38.8886882, -77.0069077, disable_notification=True)
    assert message['location']['latitude'] == 38.88868  # Telegram rounds this


@pytest.mark.asyncio
async def test_sendVenue(api):
    message = await api.sendVenue(
        config.testuser,
        38.8886882,
        -77.0069077,
        'Read books',
        '101 Independence Ave SE, Washington, DC 20540, United States',
        disable_notification=True, reply_markup={'keyboard': [['/start']]},)
    assert message['venue']['title'] == 'Read books'


@pytest.mark.asyncio
async def test_sendContact(api):
    message = await api.sendContact(
        config.testuser,
        '0612345678',
        'Jelle',
        'Besseling',
        disable_notification=True, reply_markup={'keyboard': [['/start']]},)
    assert message['contact']['last_name'] == 'Besseling'


@pytest.mark.asyncio
async def test_sendChatAction(api):
    await api.sendChatAction(config.testuser, 'upload_photo')


@pytest.mark.asyncio
async def test_send_profile_photo_by_id(api):
    photos = await api.getUserProfilePhotos(config.testuser, limit=1)
    assert photos['photos']
    message = await api.sendPhoto(
        config.testuser,
        photo=photos['photos'][0][-1]['file_id'], caption="Your profile photo", reply_markup={'keyboard': [['/start']]},
        disable_notification=True)


@pytest.mark.asyncio
async def test_send_profile_photo_by_file(api):
    photos = await api.getUserProfilePhotos(config.testuser, limit=1)
    assert photos['photos']

    filename = 'tempfile.jpg'

    with open(filename, 'w+b') as f:
        await api.download_file(photos['photos'][0][-1]['file_id'], f)

    with open(filename, 'rb') as f:
        await api.sendPhoto(
            chat_id=str(config.testuser),
            photo=f,
            caption="I downloaded your profile photo", reply_markup={'keyboard': [['/start']]},
            disable_notification=True)

    try:
        os.remove(filename)
    except OSError:
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occured

@pytest.mark.asyncio
async def test_get_updates(api):
    assert await api.getUpdates(timeout=1) is not None

@pytest.mark.asyncio
async def test_sendAudio(api):
    with open(os.path.join('tests', 'assets', 'sample_sound.mp3'), 'rb') as f:
        assert await api.sendAudio(chat_id=config.testuser, audio=f, disable_notification=True, reply_markup={'keyboard': [['/start']]}) is not None

@pytest.mark.asyncio
async def test_sendDocument(api):
    with open(os.path.join('tests', 'assets', 'sample_sound.mp3'), 'rb') as f:
        assert await api.sendDocument(chat_id=config.testuser, document=f, disable_notification=True, reply_markup={'keyboard': [['/start']]}) is not None

@pytest.mark.asyncio
async def test_sendSticker(api):
    with open(os.path.join('tests', 'assets', 'sample_sticker.webp'), 'rb') as f:
        assert await api.sendSticker(chat_id=config.testuser, sticker=f, disable_notification=True) is not None

@pytest.mark.asyncio
async def test_sendVideo(api):
    with open(os.path.join('tests', 'assets', 'sample_video.mp4'), 'rb') as f:
        assert await api.sendVideo(chat_id=config.testuser, video=f, disable_notification=True) is not None