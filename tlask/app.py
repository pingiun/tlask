# -*- coding: utf-8 -*-

import os
import sys
import pkgutil
import functools

import asyncio
import aiohttp

from .config import ConfigAttribute, Config
from .utils import get_root_path, _endpoint_from_view_func
from .api import Api
from .routing import Rule
from .datastructures import ImmutableDict

class Tlask(Api):

    url_rule_class = Rule

    config_class = Config

    debug = ConfigAttribute('DEBUG')

    testing = ConfigAttribute('TESTING')

    token = ConfigAttribute('TGTOKEN')

    default_config = ImmutableDict({
        'DEBUG':    False,
        'TESTING':  False,
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
        self._middleware_stack = lambda update=None, sub=None: None


    def make_config(self):
        root_path = self.root_path
        return self.config_class(root_path, self.default_config)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options['endpoint'] = endpoint

        rule = self.url_rule_class(rule, **options)
        self.url_map.append(rule)

        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: {}'.format(endpoint))
            self.view_functions[endpoint] = view_func

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    async def fetch_messages(self):
        if self.config['METHOD'] == 'polling':
            return await self.getUpdates()
        else:
            raise RuntimeError('{} is not a valid METHOD'.format(self.config['METHOD']))

    @asyncio.coroutine
    def routing_loop(self):
        while True:
            updates = yield from self.fetch_messages()
            for update in updates:
                self._middleware_stack(update)
                if 'message' in update:
                    pass

    def use(self, middleware):
        @functools.wraps(middleware)
        def wrapper(update=None, sub=None):
            middleware(update, sub)

        self._middlewares.append(wrapper)

    def _build_middelware_stack(self):
        for middelware in reversed(self._middlewares):
            self._middleware_stack = functools.partial(middelware, sub=self._middleware_stack)

    @property
    def token(self):
        return self.config['TGTOKEN']
    
    @token.setter
    def token(self, token):
        self.config['TGTOKEN'] = token

    def run(self, token=None):
        if self.config['TGTOKEN']:
            self.token = self.config['TGTOKEN']
        elif token:
            self.token = token
        else:
            raise Exception("TGTOKEN not supplied")
        self._build_middelware_stack()
        self.eventloop = asyncio.get_event_loop()
        self.eventloop.create_task(self.routing_loop())
        self.eventloop.run_forever()
