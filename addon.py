# Copyright (c) 2021 lampysprites
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import bpy
from .messaging import Handlers

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .sync import Server
    from .settings import SB_Preferences, SB_State


class Addon:
    def __init__(self):
        self.handlers = Handlers()
        self._server = None


    @property
    def prefs(self) -> 'SB_Preferences':
        """Get typed addon settings"""
        return bpy.context.preferences.addons[__package__].preferences


    @property
    def state(self) -> 'SB_State':
        """Get typed scene settings"""
        return bpy.context.scene.sb_state


    def start_server(self):
        """Start server instance"""
        if self._server:
            raise RuntimeError(f"A server is already created at {self._server.host}:{self._server.port}")

        host = "localhost" if self.prefs.localhost else "0.0.0.0"

        from .sync import Server
        self._server = Server(host, addon.prefs.port)
        self._server.start()


    def stop_server(self):
        """Stop server instance"""
        self._server.stop()
        self._server = None


    @property
    def server(self) -> 'Server':
        return self._server


    @property
    def server_up(self) -> bool:
        return self._server is not None


    @property
    def connected(self) -> bool:
        return self._server and self._server.connected


addon = Addon()

from .messaging import handle
handlers = addon.handlers
handlers.add(handle.Batch)
handlers.add(handle.Image)
handlers.add(handle.NewImage)
handlers.add(handle.TextureList)
handlers.add(handle.ChangeName)