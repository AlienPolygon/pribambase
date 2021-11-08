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
import imbuf
import os
from os import path
import tempfile

from .addon import addon


def refresh():
    """Tag the ui for redrawing"""
    if bpy.context.screen:
        for area in bpy.context.screen.areas:
            area.tag_redraw()


def image_name(img):
    fp = img.filepath

    if img.sb_source:
        return img.sb_source

    elif not img.packed_file and fp:
        return fp if path.isabs(fp) else bpy.path.abspath(fp)

    return ""


def new_packed_image(name, w, h):
    """Create a packed image with data that will be saved (unlike bpy.data.images.new that is cleaned when the file is opened)"""
    img = bpy.data.images.new(name, w, h, alpha=True)
    tmp = path.join(tempfile.gettempdir(), "__sb__delete_me.png")
    img.filepath = tmp
    img.save() # the file needs to exist for pack() to work
    img.pack()
    img.filepath=""
    img.use_fake_user = True
    os.remove(tmp)
    return img


def update_image(w, h, name, pixels):
    """Replace the image with pixel data"""
    img = None

    for i in bpy.data.images:
        if (i.sb_source == name) or (name == i.filepath) or (name == i.name):
            img = i
            break
    else:
        # to avoid accidentally reviving deleted images, we ignore anything doesn't exist already
        return

    if not img:
        return None

    elif not img.has_data:
        # load *some* data so that the image can be packed, and then updated
        ib = imbuf.new((w, h))
        tmp = path.join(tempfile.gettempdir(), "__sb__delete_me.png")
        imbuf.write(ib, tmp)
        img.filepath = tmp
        img.reload()
        img.pack()
        img.filepath=""
        img.use_fake_user = True
        os.remove(tmp)

    elif (img.size[0] != w or img.size[1] != h):
            img.scale(w, h)

    # convert data to blender accepted floats
    pixels = pixels / 255.0
    # flip y axis ass backwards
    pixels.shape = (h, pixels.size // h)
    pixels = pixels[::-1,:]

    # change blender data
    try:
        # version >= 2.83
        # much faster
        img.pixels.foreach_set(pixels.ravel())
    except:
        # version < 2.83
        img.pixels[:] = pixels.ravel()

    img.update()

    return img


class SB_OT_report(bpy.types.Operator):
    bl_idname = "pribambase.report"
    bl_label = "Report. It doesn't seem to work as I hoped but does log nicely to the system console at least"
    bl_description = "Report the message"
    bl_options = {'REGISTER', 'INTERNAL'}

    message_type: bpy.props.StringProperty(name="Message Type", default='INFO')
    message: bpy.props.StringProperty(name="Message", default='Someone forgot to change the message text')

    def execute(self, context):
        self.report({self.message_type}, self.message)
        return {'FINISHED'}