import sys

from pygments.token import Token

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import (BufferControl, FillControl,
                                            TokenListControl, UIControl)
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.shortcuts import create_asyncio_eventloop


class UI(object):

    manager = KeyBindingManager()

    buffers = {
        DEFAULT_BUFFER: Buffer(is_multiline=True),
        'MESSAGES': Buffer(is_multiline=True),
    }

    layout = VSplit([
        Window(
            dont_extend_width=True,
            content=TokenListControl(
                get_tokens=lambda cli: [(Token, 'SlackTerm')],
            ),
        ),
        Window(
            width=D.exact(1),
            content=FillControl('|', token=Token.Line),
        ),
        HSplit([
            Window(content=BufferControl(buffer_name='MESSAGES')),
            Window(
                height=D.exact(1),
                content=FillControl('_', token=Token.Line),
            ),
            Window(
                height=D.exact(3),
                content=BufferControl(buffer_name=DEFAULT_BUFFER),
            ),
        ]),
    ])

    def __init__(self):
        application = Application(
            buffers=self.buffers,
            layout=self.layout,
            key_bindings_registry=self.manager.registry,
            mouse_support=True,
            use_alternate_screen=True,
        )
        eventloop = create_asyncio_eventloop()
        self.cli = CommandLineInterface(application=application,
                                        eventloop=eventloop)
        sys.stdout = self.cli.stdout_proxy()

    async def start(self):
        while True:
            result = await self.cli.run_async()
            if not result:
                break

    @manager.registry.add_binding(Keys.ControlC, eager=True)
    def exit_(self):
        self.cli.set_return_value(None)


