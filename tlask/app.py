# -*- coding: utf-8 -*-

import os
import sys
import pkgutil
import functools

import asyncio
import aiohttp

import logging
logger = logging.getLogger('tlask.app')

from .api import Api
from .config import ConfigAttribute, Config
from .datastructures import ImmutableDict
from .helper import Sender
from .routing import Rule
from .utils import get_root_path, _endpoint_from_view_func

from .middleware import session

class Tlask(Api):

    url_rule_class = Rule

    config_class = Config

    token = ConfigAttribute('TGTOKEN') 

    default_config = ImmutableDict({
        'MIDDLEWARES': [session.handle],
        'TGTOKEN':  None,
        'METHOD':   'polling',
        })

    def __init__(self, import_name, root_path=None):
        super(Tlask, self).__init__()

        self.import_name = import_name

        if root_path == None:
            self.root_path = get_root_path(self.import_name)

        self.config = self.make_config()

        self.url_map = []

        self.view_functions = {}

        self._middlewares = []
        
        for middelware in self.config['MIDDLEWARES']:
            self.use(middelware)

        self._middleware_stack = lambda res=None, update=None, sub=None: True

    def make_config(self):
        root_path = self.root_path
        return self.config_class(root_path, self.default_config)

    def route(self, rule=None, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint

        logger.debug("Adding rule %s to the map", rule)

        rule = self.url_rule_class(rule, **options)
        self.url_map.append(rule)

        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: {}'.format(endpoint))
            self.view_functions[endpoint] = view_func

    async def fetch_messages(self):
        if self.config['METHOD'] == 'polling':
            return await self.getUpdates()
        else:
            raise RuntimeError('{} is not a valid METHOD'.format(self.config['METHOD']))

    async def routing_loop(self):
        while True:
            updates = await self.fetch_messages()
            for update in updates:
                logger.debug(update)
                update['params'] = {}
                res = Sender(self, update)
                if self._middleware_stack(res, update):
                    logger.debug("Update after the middelware stack: %s", update)
                    
                    if 'message' in update:
                        for rule in self.url_map:
                            if rule.match(update):
                                logger.info("%s - %s", update['message']['chat']['id'], update['message']['text'])
                                await self.view_functions[rule.endpoint](res, update, **update['params'])
                else:
                    logger.debug("Some middelware took the update")

    def use(self, middleware):
        @functools.wraps(middleware)
        def wrapper(res=None, update=None, sub=None):
            return middleware(res, update, sub)

        self._middlewares.append(wrapper)

    def _build_middelware_stack(self):
        for middleware in reversed(self._middlewares):
            self._middleware_stack = functools.partial(middleware, sub=self._middleware_stack)

    def run(self, token=None):
        if token:
            self.token = token

        self._build_middelware_stack()
        self.eventloop = asyncio.get_event_loop()
        self.eventloop.create_task(self.routing_loop())
        self.eventloop.run_forever()
