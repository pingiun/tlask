import re
import logging
logger = logging.getLogger('tlask.routing')

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
    while pos < end:
        m = _rule_re.match(rule, pos)
        if m is None:
            break

        pos = m.end()

    if pos < end:
        remaining = rule[pos:]
        if '>' in remaining or '<' in remaining:
            raise ValueError('malformed rule: %r' % rule)
        yield None, remaining

class Rule(object):
    def __init__(self, string, endpoint, **options):
        if not string.startswith('/'):
            raise ValueError("Rules must start with a trailing slash")

        self.rule = string
        self.endpoint = endpoint

        self._regex = None

        self.compile()

    def compile(self):
        regex_parts = []

        for converter, variable in parse_rule(self.rule):
            if converter is None:
                if variable == '/':
                    variable = '/start'
                regex_parts.append(re.escape(variable))
            else:
                RuntimeError("Converters are not supported yet")

        regex = r'^{}$'.format(''.join(regex_parts))
        logger.debug("Regex for rule %s: %s", self.rule, regex)
        self._regex = re.compile(regex, re.UNICODE)

    def match(self, update):
        m = self._regex.search(update['message']['text'])
        if m is not None:
            return True