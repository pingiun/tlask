import aiohttp
import asyncio
import json

from aiohttp.helpers import FormData

import logging
logger = logging.getLogger('tlask.api')


class Api(object):
    def __init__(self, token=None):
        self._offset = None
        # If api.py is used as a standalone class (e.g. not inherited by 
        # something that has a config), self._token is used for the token.
        if token:
            self.token = token

    async def getUpdates(self, offset=None, timeout=20):
        """ See: https://core.telegram.org/bots/api#getUpdates """
        if not offset:
            offset = self._offset

        updates = await self._api_call(
            'getUpdates', offset=offset, timeout=timeout)
        # Trust that the server gives messages in order
        if updates:
            self._offset = updates[-1]['update_id'] + 1
        return updates

    async def getMe(self):
        """ See: https://core.telegram.org/bots/api#getme """
        return await self._api_call('getMe')

    async def sendMessage(self,
                          chat_id,
                          text,
                          parse_mode=None,
                          disable_web_page_preview=None,
                          disable_notification=None,
                          reply_to_message_id=None,
                          reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendMessage """
        return await self._api_call(
            'sendMessage',
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def forwardMessage(self,
                             chat_id,
                             from_chat_id,
                             message_id,
                             disable_notification=None):
        """ See: https://core.telegram.org/bots/api#forwardMessage """
        return await self._api_call(
            'forwardMessage',
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            disable_notification=disable_notification)

    async def _send_by_id_or_file(self, method, file, **kwargs):
        if type(file[0]) == str:
            arg = {file[1]: file[0]}
            return await self._api_call(method, **arg, **kwargs)
        else:
            arg = {file[1]: file[0]}
            return await self._api_call_upload(method, **arg, **kwargs)

    async def sendPhoto(self,
                        chat_id,
                        photo,
                        caption=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendPhoto """
        return await self._send_by_id_or_file(
            'sendPhoto', [photo, 'photo'],
            chat_id=chat_id,
            caption=caption,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendAudio(self,
                        chat_id,
                        audio,
                        duration=None,
                        performer=None,
                        title=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendAudio """
        return await self._send_by_id_or_file(
            'sendAudio', [audio, 'audio'],
            chat_id=chat_id,
            duration=duration,
            performer=performer,
            title=title,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendDocument(self,
                           chat_id,
                           document,
                           caption=None,
                           disable_notification=None,
                           reply_to_message_id=None,
                           reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendDocument """
        return await self._send_by_id_or_file(
            'sendDocument', [document, 'document'],
            chat_id=chat_id,
            caption=caption,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendSticker(self,
                          chat_id,
                          sticker,
                          caption=None,
                          disable_notification=None,
                          reply_to_message_id=None,
                          reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendSticker """
        return await self._send_by_id_or_file(
            'sendSticker', [sticker, 'sticker'],
            chat_id=chat_id,
            caption=caption,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendVideo(self,
                        chat_id,
                        video,
                        duration=None,
                        width=None,
                        height=None,
                        caption=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendVideo """
        return await self._send_by_id_or_file(
            'sendVideo', [video, 'video'],
            chat_id=chat_id,
            caption=caption,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendVoice(self,
                        chat_id,
                        voice,
                        duration=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendVoice """
        return await self._send_by_id_or_file(
            'sendVoice', [voice, 'voice'],
            chat_id=chat_id,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendLocation(self,
                           chat_id,
                           latitude,
                           longitude,
                           disable_notification=None,
                           reply_to_message_id=None,
                           reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendLocation """
        return await self._api_call(
            'sendLocation',
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendVenue(self,
                        chat_id,
                        latitude,
                        longitude,
                        title,
                        address,
                        foursquare_id=None,
                        disable_notification=None,
                        reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendVenue """
        return await self._api_call(
            'sendVenue',
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            title=title,
            address=address,
            foursquare_id=foursquare_id,
            disable_notification=disable_notification,
            reply_markup=reply_markup)

    async def sendContact(self,
                          chat_id,
                          phone_number,
                          first_name,
                          last_name=None,
                          disable_notification=None,
                          reply_to_message_id=None,
                          reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendContact """
        return await self._api_call(
            'sendContact',
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup)

    async def sendChatAction(self, chat_id, action):
        """ See: https://core.telegram.org/bots/api#sendChatAction """
        return await self._api_call(
            'sendChatAction', chat_id=chat_id, action=action)

    async def getUserProfilePhotos(self, user_id, offset=None, limit=None):
        """ See: https://core.telegram.org/bots/api#getUserProfilePhotos """
        return await self._api_call(
            'getUserProfilePhotos',
            user_id=user_id,
            offset=offset,
            limit=limit)

    async def getFile(self, file_id):
        """ See: https://core.telegram.org/bots/api#getFile """
        return await self._api_call('getFile', file_id=file_id)

    async def kickChatMember(self, chat_id, user_id):
        """ See: https://core.telegram.org/bots/api#kickChatMember """
        return await self._api_call(
            'kickChatMember', chat_id=chat_id, user_id=user_id)

    async def leaveChat(self, chat_id):
        """ See: https://core.telegram.org/bots/api#leaveChat """
        return await self._api_call('leaveChat', chat_id=chat_id)

    async def unbanChatMember(self, chat_id, user_id):
        """ See: https://core.telegram.org/bots/unbanChatMember """
        return await self._api_call(
            'unbanChatMember', chat_id=chat_id, user_id=user_id)

    async def getChat(self, chat_id):
        """ See: https://core.telegram.org/bots/api#getChat """
        return await self._api_call('getChat', chat_id=chat_id)

    async def getChatAdministrators(self, chat_id):
        """ See: https://core.telegram.org/bots/api#getChatAdministrators """
        return await self._api_call('getChatAdministrators', chat_id=chat_id)

    async def getChatMembersCount(self, chat_id):
        """ See: https://core.telegram.org/bots/api#getChatMembersCount """
        return await self._api_call('getChatMembersCount', chat_id=chat_id)

    async def getChatMember(self, chat_id, user_id):
        """ See: https://core.telegram.org/bots/api#getChatMember """
        return await self._api_call(
            'getChatMember', chat_id=chat_id, user_id=user_id)

    async def answerCallbackQuery(self,
                                  callback_query_id,
                                  text=None,
                                  show_alert=None):
        """ See: https://core.telegram.org/bots/api#answerCallbackQuery """
        return await self._api_call(
            'answerCallbackQuery',
            callback_query_id=callback_query_id,
            text=text,
            show_alert=show_alert)

    async def editMessageText(self,
                              text,
                              chat_id=None,
                              message_id=None,
                              inline_message_id=None,
                              parse_mode=None,
                              disable_web_page_preview=None,
                              reply_markup=None):
        """ See: https://core.telegram.org/bots/api#editMessageText """
        #TODO: Check one of (chat_id, message_id) or inline_message_id is supplied
        return await self._api_call(
            'editMessageText',
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup)

    async def editMessageCaption(self,
                                 chat_id=None,
                                 message_id=None,
                                 inline_message_id=None,
                                 caption=None,
                                 reply_markup=None):
        """ See: https://core.telegram.org/bots/api#editMessageCaption """
        #TODO: Check one of (chat_id, message_id) or inline_message_id is supplied
        return await self._api_call(
            'editMessageCaption',
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            caption=caption,
            reply_markup=reply_markup)

    async def editMessageReplyMarkup(self,
                                     chat_id=None,
                                     message_id=None,
                                     inline_message_id=None,
                                     reply_markup=None):
        """ See: https://core.telegram.org/bots/api#editMessageReplyMarkup """

        #TODO: Check one of (chat_id, message_id) or inline_message_id is supplied
        return await self._api_call(
            'editMessageReplyMarkup',
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            reply_markup=reply_markup)

    async def answerInlineQuery(self,
                                inline_query_id,
                                results,
                                cache_time=None,
                                is_personal=None,
                                next_offset=None,
                                switch_pm_text=None,
                                switch_pm_parameter=None):
        """ See: https://core.telegram.org/bots/api#answerInlineQuery """
        return await self._api_call(
            'answerInlineQuery',
            inline_query_id=inline_query_id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter)

    async def _api_call(self, method, **kwargs):
        if not hasattr(self, 'token'):
            raise RuntimeError("Telegram token not set")

# Remove optional items that aren't supplied from the options
#params = {k: v for k, v in kwargs.items() if v is not None}
        params = {}

        for k, v in kwargs.items():
            if v is not None:
                if type(v) == dict or type(v) == list:
                    v = json.dumps(v)
                params[k] = v

        baseurl = 'https://api.telegram.org/bot' + self.token + '/'
        async with aiohttp.ClientSession() as session:
            async with session.get(baseurl + method,
                                   params=params) as response:
                if not response.status == 200:
                    responsetext = await response.text()
                    raise RuntimeError(
                        "Got a {} return status. Telegram error: {}".format(
                            response.status, responsetext))
                jsondata = await response.json()
                return jsondata['result']

    async def download_file(self, file_id, dest):
        #TODO: Implement caching
        if not hasattr(self, 'token'):
            raise RuntimeError("Telegram token not set")

        file = await self.getFile(file_id=file_id)
        baseurl = 'https://api.telegram.org/file/bot' + self.token + '/'

        async with aiohttp.ClientSession() as session:
            async with session.get(baseurl + file['file_path']) as response:
                if not response.status == 200:
                    responsetext = await response.text()
                    raise RuntimeError(
                        "Got a {} return status. Response content: {}".format(
                            response.status, responsetext))
                chunk_size = 1024
                if type(dest) == 'str':
                    with open(dest, 'wb') as f:
                        while True:
                            chunk = await response.content.read(chunk_size)
                            if not chunk:
                                break
                            f.write(chunk)
                else:
                    while True:
                        chunk = await response.content.read(chunk_size)
                        if not chunk:
                            break
                        dest.write(chunk)

    async def _api_call_upload(self, method, **kwargs):
        if not hasattr(self, 'token'):
            raise RuntimeError("Telegram token not set")
        data = FormData()
        for k, v in kwargs.items():
            if v is not None:
                # Ints and bools need to be converted to strings, but files not
                if type(v) == dict or type(v) == list:
                    v = json.dumps(v)
                if type(v) != str and not hasattr(v, 'read'):
                    v = str(v)
                data.add_field(k, v)

        baseurl = 'https://api.telegram.org/bot' + self.token + '/'

        async with aiohttp.ClientSession() as session:
            async with session.post(baseurl + method, data=data) as response:
                if not response.status == 200:
                    responsetext = await response.text()
                    raise RuntimeError(
                        "Got a {} return status. Telegram error: {}".format(
                            response.status, responsetext))
                jsondata = await response.json()
                return jsondata['result']
