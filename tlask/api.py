import aiohttp
import asyncio

class Api(object):

    def __init__(self, token=None): 
        self._offset = None
        # If api.py is used as a standalone class (e.g. not inherited by 
        # something that has a config), self._token is used for the token. 
        self._token = token

    async def getUpdates(self, offset=None, timeout=10):
        """ See: https://core.telegram.org/bots/api#getUpdates """
        if not offset:
            offset = self._offset

        updates = await self._api_call('getUpdates', offset=offset, 
                                       timeout=timeout)
        # Trust that the server gives messages in order
        if updates:
            self._offset = updates[-1]['update_id'] + 1
        return updates

    async def getMe(self):
        """ See: https://core.telegram.org/bots/api#getme """
        return await self._api_call('getMe')

    async def sendMessage(self, chat_id, text, parse_mode=None, 
                          disable_web_page_preview=None, 
                          disable_notification=None, 
                          reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendMessage """
        return await self._api_call('sendMessage', chat_id=chat_id, text=text, 
                                    parse_mode=parse_mode,
                                    disable_web_page_preview=disable_web_page_preview,
                                    disable_notification=disable_notification,
                                    reply_to_message_id=reply_to_message_id, 
                                    reply_markup=reply_markup)

    async def forwardMessage(self, chat_id, from_chat_id, message_id, 
                             disable_notification=None):
        """ See: https://core.telegram.org/bots/api#forwardMessage """
        return await self._api_call('forwardMessage', chat_id=chat_id, 
                                    from_chat_id=from_chat_id, 
                                    message_id=message_id,
                                    disable_notification=disable_notification)

    async def sendPhoto(self, chat_id, photo, caption, 
                        disable_notification=None, reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendPhoto """

        pass #TODO

    async def sendAudio(self, chat_id, audio, duration=None, performer=None,
                        title=None, disable_notification=None,
                        reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendAudio """
        pass #TODO

    async def sendDocument(self, chat_id, document, caption=None, 
                           disable_notification=None,
                           reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendDocument """
        pass #TODO

    async def sendSticker(self, chat_id, sticker, caption=None, 
                           disable_notification=None,
                           reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendSticker """
        pass #TODO

    async def sendVideo(self, chat_id, video, duration=None, width=None, 
                        height=None, caption=None, disable_notification=None,
                        reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendVideo """
        pass #TODO

    async def sendVoice(self, chat_id, voice, duration=None, 
                        disable_notification=None, reply_to_message_id=None,
                        reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendVoice """
        pass #TODO

    async def sendLocation(self, chat_id, latitude, longitude, 
                           disable_notification=None, reply_to_message_id=None, 
                           reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendLocation """
        return await self._api_call('sendLocation', chat_id=chat_id, 
                                    latitude=latitude, longitude=longitude, 
                                    disable_notification=disable_notification, 
                                    reply_to_message_id=reply_to_message_id,
                                    reply_markup=reply_markup)

    async def sendVenue(self, chat_id, latitude, longitude, title, address, 
                        foursquare_id=None, disable_notification=None, 
                        reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendVenue """
        return await self._api_call('sendVenue', 
                                    chat_id=chat_id, latitude=latitude, 
                                    longitude=longitude, title=title,
                                    address=address, 
                                    foursquare_id=foursquare_id, 
                                    disable_notification=disable_notification,
                                    reply_markup=reply_markup)

    async def sendContact(self, chat_id, phone_number, first_name,
                          last_name=None, disable_notification=None,
                          reply_to_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#sendContact """
        return await self._api_call('sendContact', chat_id=chat_id, 
                                    phone_number=phone_number,
                                    first_name=first_name, last_name=last_name,
                                    disable_notification=disable_notification,
                                    reply_to_message_id=reply_to_message_id,
                                    reply_markup=reply_markup)

    async def sendChatAction(self, chat_id, action):
        """ See: https://core.telegram.org/bots/api#sendChatAction """
        return await self._api_call('sendChatAction', chat_id=chat_id, 
                                    action=action)

    async def getUserProfilePhotos(self, user_id, offset=None, limit=None):
        """ See: https://core.telegram.org/bots/api#getUserProfilePhotos """
        return await self._api_call('getUserProfilePhotos', user_id=user_id, 
                                    offset=offset, limit=limit)

    async def getFile(self, file_id):
        """ See: https://core.telegram.org/bots/api#getFile """
        return await self._api_call('getFile', file_id=file_id)

    async def kickChatMember(self, chat_id, user_id):
        """ See: https://core.telegram.org/bots/api#kickChatMember """
        return await self._api_call('kickChatMember', chat_id=chat_id, 
                                    user_id=user_id)

    async def leaveChat(self, chat_id):
        """ See: https://core.telegram.org/bots/api#leaveChat """
        return await self._api_call('leaveChat', chat_id=chat_id)

    async def unbanChatMember(self, chat_id, user_id):
        """ See: https://core.telegram.org/bots/unbanChatMember """
        return await self._api_call('unbanChatMember', chat_id=chat_id, 
                                    user_id=user_id)

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
        return await self._api_call('getChatMember',
                                    chat_id=chat_id, user_id=user_id)

    async def answerCallbackQuery(self, callback_query_id, text=None, show_alert=None):
        """ See: https://core.telegram.org/bots/api#answerCallbackQuery """
        return await self._api_call('answerCallbackQuery', 
                                    callback_query_id=callback_query_id,
                                    text=text, show_alert=show_alert)

    async def editMessageText(self, chat_id=None, message_id=None,
                              inline_message_id=None, text, parse_mode=None,
                              disable_web_page_preview=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#editMessageText """
        return await self._api_call('editMessageText', chat_id=chat_id,
                                    message_id=message_id, 
                                    inline_message_id=inline_message_id,
                                    text=text, parse_mode=parse_mode,
                                    disable_web_page_preview=disable_web_page_preview,
                                    reply_markup=reply_markup)

    async def editMessageCaption(self, chat_id=None, message_id=None, 
                                 inline_message_id=None, caption=None,
                                 reply_markup=None):
        """ See: https://core.telegram.org/bots/api#editMessageCaption """
        return await self._api_call('editMessageCaption', chat_id=chat_id,
                                    inline_message_id=inline_message_id,
                                    caption=caption, reply_markup=reply_markup)

    async def editMessageReplyMarkup(self, chat_id=None, message_id=None, 
                                     inline_message_id=None, reply_markup=None):
        """ See: https://core.telegram.org/bots/api#editMessageReplyMarkup """
        return await self._api_call('editMessageReplyMarkup', chat_id=chat_id,
                                    message_id=message_id, 
                                    inline_message_id=inline_message_id,
                                    reply_markup=reply_markup)

    async def answerInlineQuery(self, inline_query_id, results, cache_time=None,
                                is_personal=None, next_offset=None,
                                switch_pm_text=None, switch_pm_parameter=None):
        """ See: https://core.telegram.org/bots/api#answerInlineQuery """
        return await self._api_call('answerInlineQuery', 
                                    inline_query_id=inline_query_id,
                                    results=results, cache_time=cache_time,
                                    is_personal=is_personal,
                                    next_offset=next_offset, 
                                    switch_pm_text=switch_pm_text,
                                    switch_pm_parameter=switch_pm_parameter)


    async def _api_call(self, method, **kwargs):
        if not self.token:
            if not self._token:
                raise Exception("Telegram token not set")
            else:
                token = self._token
        else:
            token = self.token

        baseurl = 'https://api.telegram.org/bot' + token + '/'
        async with aiohttp.ClientSession() as session:
            async with session.get(baseurl + method, params=kwargs) as response:
                jsondata = await response.json()
                if not response.status == 200:
                    raise Exception("Got a non {} return. Telegram error: {}".format(response.status, jsondata))
                return jsondata['result']
