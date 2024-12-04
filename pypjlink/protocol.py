# -*- coding: utf-8 -*-

import sys


def to_binary(body, param, sep=' '):
    assert body.isupper()

    assert len(body) == 4
    assert len(param) <= 128

    return '%1' + body + sep + param + '\r'

async def parse_response(reader, encoding, data=''):
    if len(data) < 7:
        lookahead = (await reader.read(1)).decode(encoding)
        if lookahead == '\n':
            data += (await reader.read(2 + 4 + 1 - len(data))).decode(encoding)
        else:
            data += lookahead + (await reader.read(2 + 4 - len(data))).decode(encoding)

    header = data[0]
    assert header == '%'

    version = data[1]
    # only class 1 is currently defined
    assert version == '1'

    body = data[2:6]
    # commands are case-insensitive, but let's turn them upper case anyway
    # this will avoid the rest of our code from making this mistake
    # FIXME: AFAIR this takes the current locale into consideration, it shouldn't.
    body = body.upper()

    sep = data[6]
    assert sep == '='

    param = (await reader.readuntil(b'\r')).decode(encoding)

    return body, param.split('\r')[0]

ERRORS = {
    'ERR1': 'undefined command',
    'ERR2': 'out of parameter',
    'ERR3': 'unavailable time',
    'ERR4': 'projector failure',
}

async def send_command(reader, writer, req_body, req_param, encoding):
    data = to_binary(req_body, req_param).encode(encoding)
    writer.write(data)
    await writer.drain()

    resp_body, resp_param = await parse_response(reader, encoding)
    assert resp_body == req_body

    if resp_param in ERRORS:
        return False, ERRORS[resp_param]
    return True, resp_param
