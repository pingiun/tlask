# -*- coding: utf-8 -*-

import re
import logging
logger = logging.getLogger('tlask.routing')

from .utils import get_flavor, get_text

_rule_re = re.compile(r'''
    (?P<static>[^<]*)                           # static rule data
    <
    (?:
        (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
        \:                                      # variable delimiter
    )?
    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)        # variable name
    >
''', re.VERBOSE)


def parse_rule(rule):
    pos = 0
    end = len(rule)
    used_names = set()
    while pos < end:
        m = _rule_re.match(rule, pos)
        if m is None:
            break

        data = m.groupdict()
        if data['static']:
            yield None, data['static']
        
        variable = data['variable']
        if variable in used_names:
            raise ValueError('variable name {} used twice.'.format(variable))
        used_names.add(variable)
        if 'converter' in data:
            yield variable, data['converter']
        else:
            yield variable, None

        pos = m.end()

    if pos < end:
        remaining = rule[pos:]
        if '>' in remaining or '<' in remaining:
            raise ValueError('malformed rule: {}'.format(rule))
        yield None, remaining

def build_match_string(update, me):
    flavor = get_flavor(update)
    text = get_text(update, flavor)
    if flavor == 'message' or flavor == 'edited_message':
        chattype = update['message']['chat']['type']
    elif flavor == 'callback_query':
        chattype = update['callback_query']['message']['chat']['type']
    else:
        chattype = 'private'
    if text.endswith('@' + me['username']):
        return flavor + '/' + chattype + text
    else:
        return flavor + '/' + chattype + text + '@'

class Rule(object):

    def __init__(self, string, flavor, endpoint, **options):
        if not string.startswith('/'):
            raise ValueError("Rules must start with a trailing slash")

        self.rule = string
        self.endpoint = endpoint
        self.flavor = flavor

        self.variables = []
        self.converters = {}

        self._regex = None
        if options:
            self._options = options
        else:
            self._options = {}

    @property
    def help(self):
        if 'help' in self._options:
            return self._options['help']
        else:
            return self.rule
    

    def compile(self, me):
        regex_parts = []

        chattype = self._options.get('chattype', None)
        regex_parts.append(self.flavor + '\/')
        if chattype:
            regex_parts.append(chattype)
        else:
            regex_parts.append('.*')

        for variable, static in parse_rule(self.rule):
            if variable is None:
                regex_parts.append(re.escape(static.strip()))
            else:
                if regex_parts[-1].endswith('/'):
                    space = ''
                else:
                    space = '\ '
                regex_parts.append('(?:{}(?P<{}>[^ ]*))?'.format(space, variable))
                self.variables.append(variable)
                if static:
                    logger.debug("Converter for %s is %s", variable, static)
                    self.converters[variable] = static

        regex_parts.append('(?P<extra>.*)@(?P<username>' + me['username'] + ')?')

        regex = r'^{}$'.format(''.join(regex_parts))
        logger.debug("Regex for rule %s: %s", self.rule, regex)
        self._regex = re.compile(regex, re.UNICODE)

    def _convert(self, converter, data):
        if converter == 'int':
            try:
                return int(data)
            except:
                return data

    def match(self, update, me):
        match_string = build_match_string(update, me)
        logger.debug("Matching %s with regex %s", match_string, self._regex.pattern)
        m = self._regex.search(match_string)
        if m is not None:
            data = m.groupdict()
            for variable in data:
                if variable in self.converters:
                    data[variable] = self._convert(self.converters[variable], data[variable])
            del data['username']
            getextra = self._options.get('getextra', None)
            if not getextra and 'extra' in data:
                del data['extra']
            update['params'].update(data)
            return True
        else:
            return False
