import os

from tornado.platform.asyncio import AsyncIOMainLoop

import asyncio
from rtm import RTM
from ui import UI


def main(token):
    loop = asyncio.get_event_loop()
    AsyncIOMainLoop().install()
    ui = UI()
    rtm = RTM(ui=ui)
    ui_task = loop.create_task(ui.start())
    rtm_task = asyncio.gather(rtm.start(token), return_exceptions=True)
    loop.run_until_complete(ui_task)
    rtm_task.cancel()
    loop.run_until_complete(rtm_task)
    loop.close()


if __name__ == '__main__':
    token = os.environ['SLACK_API_TOKEN']
    main(token)
