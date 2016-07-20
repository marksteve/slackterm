import json

from tornado.platform.asyncio import to_asyncio_future
from tornado.websocket import websocket_connect

import requests


class RTM(object):

    def __init__(self, ui):
        self.ui = ui

    async def start(self, token):
        resp = requests.post(
            'https://slack.com/api/rtm.start',
            data={'token': token},
        ).json()
        if not resp['ok']:
            raise RuntimeError('Failed to start RTM')

        self.conn = await to_asyncio_future(websocket_connect(resp['url']))

        while True:
            msg = await to_asyncio_future(self.conn.read_message())
            if msg is None:
                break
            self.on_message(msg)

    def on_message(self, msg):
        evt = json.loads(msg)
        handler = getattr(self, 'handle_{}'.format(evt['type']), None)
        if handler:
            handler(evt)
        else:
            self.ui.buffers['MESSAGES'].text += repr(evt) + '\n'

    def handle_reconnect_url(self, evt):
        self.reconnect_url = evt['url']
