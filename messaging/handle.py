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
import asyncio
import re
from typing import Tuple, Iterable
from os import path
from . import Handler
import numpy as np
# TODO move into local methods
from .. import util


class Batch(Handler):
    """Process batch messages"""
    id = "["

    def parse(self, args):
        count = self.take_uint(2)
        args.messages = [self.take_data() for _ in range(count)]


    async def execute(self, messages:Iterable[memoryview]):
        for m in messages:
            await self._handlers.process(m)


class Image(Handler):
    id = 'I'

    def parse(self, args):
        args.size = self.take_uint(2), self.take_uint(2)
        args.name = self.take_str()
        args.data = np.frombuffer(self.take_data(), dtype=np.ubyte)

    async def execute(self, *, size:Tuple[int, int], name:str, data:np.array):
        try:
            # TODO separate cases for named and anonymous sprites
            if not bpy.context.window_manager.is_interface_locked:
                util.update_image(size[0], size[1], name, data)
            else:
                bpy.ops.pribambase.report({'WARNING'}, "UI is locked, image update skipped")
        except:
            # blender 2.80... if it crashes, it crashes :\
            util.update_image(size[0], size[1], name, data)


class NewImage(Image):
    """Same as image except it creates a named image if it doesn't exist"""
    id = 'N'

    async def execute(self, *, size:Tuple[int, int], name:str, data:np.array):
        _, short = path.split(name)
        img = util.new_packed_image(short, size[0], size[1])
        img.sb_source = name
        await super().execute(size=size, name=name, data=data)


class TextureList(Handler):
    """Send the list of available textures"""
    id = 'L'

    async def execute(self):
        bpy.ops.pribambase.texture_list()


class ChangeName(Handler):
    """Change textures' sources when aseprite saves the file under a new name"""
    id = 'C'

    def parse(self, args):
        args.old_name = self.take_str()
        args.new_name = self.take_str()


    async def execute(self, *, old_name, new_name):
        try:
            # FIXME there's a risk of race condition but it's pretty bad if the rename doesn't happen
            while bpy.context.window_manager.is_interface_locked:
                bpy.ops.pribambase.report({'WARNING'}, "UI is locked, waiting to update image source..")
                asyncio.sleep(0.1)
        except:
            # version 2.80... caveat emptor
            pass

        # avoid having identical sb_source on several images
        for img in bpy.data.images:
            if old_name in (img.sb_source, img.filepath, img.name):
                img.sb_source = new_name

                if re.search(r"\.(?:png|jpg|jpeg|bmp|tga)$", new_name):
                    img.filepath = new_name
                else:
                    img.filepath = ""

                bpy.ops.pribambase.texture_list()