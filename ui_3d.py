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
from .addon import addon
import numpy as np
from math import pi


def scale_image(image, scale):
    """Scale image in-place without filtering"""
    w, h = image.size
    px = np.array(image.pixels, dtype=np.float32)
    px.shape = (w, h, 4)
    image.scale(w * scale, h * scale)
    px = px.repeat(scale, 0).repeat(scale, 1)
    try:
        # version >= 2.83
        image.pixels.foreach_set(px.ravel())
    except:
        # version < 2.83
        image.pixels[:] = px.ravel()
    image.update()


class SB_OT_reference_add(bpy.types.Operator):
    bl_idname = "pribambase.reference_add"
    bl_label = "Add Reference"
    bl_description = "Add reference image with pixels aligned to the view grid"
    bl_options = {'REGISTER', 'UNDO'}

    scale: bpy.props.IntProperty(
        name="Prescale",
        description="Prescale the image",
        default=10,
        min=1,
        max=50)

    opacity: bpy.props.FloatProperty(
        name="Opacity",
        description="Image's viewport opacity",
        default=0.33,
        min=0.0,
        max=1.0,
        subtype='FACTOR')

    selectable: bpy.props.BoolProperty(
        name="Selectable",
        description="If checked, the image can be selected in the viewport, otherwise only in the outliner",
        default=True)

    # dialog
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.bmp;*.png", options={'HIDDEN'})
    use_filter: bpy.props.BoolProperty(default=True, options={'HIDDEN'})


    @classmethod
    def poll(self, context):
        return not context.object or context.object.mode == 'OBJECT'


    def invoke(self, context, event):
        self.invoke_context = context
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


    def execute(self, context):
        image = bpy.data.images.load(self.filepath)
        #image.pack() # NOTE without packing it breaks after reload but so what
        w, h = image.size
        scale_image(image, self.scale)
        image.sb_scale = self.scale

        bpy.ops.object.add(align='WORLD', rotation=(pi/2, 0, 0), location = (0, 0, 0))
        ref = context.active_object
        ref.data = image
        ref.empty_display_type = 'IMAGE'
        ref.use_empty_image_alpha = self.opacity < 1.0
        ref.color[3] = self.opacity
        ref.empty_display_size = max(w, h) * context.space_data.overlay.grid_scale
        if not self.selectable:
            ref.hide_select = True
            self.report({'INFO'}, "The reference won't be selectable. Use the outliner to reload/delete it")

        return {'FINISHED'}


class SB_OT_reference_reload(bpy.types.Operator):
    bl_idname = "pribambase.reference_reload"
    bl_label = "Reload Reference"
    bl_description = "Reload reference while keeping it prescaled"
    bl_options = {'REGISTER', 'UNDO'}


    @classmethod
    def poll(self, context):
        return context.object and context.object.type == 'EMPTY' \
                and context.object.empty_display_type == 'IMAGE'


    def execute(self, context):
        image = context.object.data
        image.reload()
        scale_image(image, image.sb_scale)

        return {'FINISHED'}


class SB_OT_reference_reload_all(bpy.types.Operator):
    bl_idname = "pribambase.reference_reload_all"
    bl_label = "Reload All References"
    bl_description = "Reload all references (including non-pribamabase's), while keeping them prescaled"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj.type == 'EMPTY' and obj.empty_display_type == 'IMAGE':
                image = obj.data
                image.reload()
                scale_image(image, image.sb_scale)

        return {'FINISHED'}



class SB_PT_panel_link(bpy.types.Panel):
    bl_idname = "SB_PT_panel_link_3d"
    bl_label = "Sync"
    bl_category = "Tool"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Link UP" if addon.server_up else "Link DOWN")

        row = row.row()
        row.alignment = 'RIGHT'
        if addon.server_up:
            row.operator("pribambase.stop_server", text="Stop", icon="DECORATE_LIBRARY_OVERRIDE")
        else:
            row.operator("pribambase.start_server", text="Connect", icon="DECORATE_LINKED")
        row.operator("pribambase.preferences", icon='PREFERENCES', text="", emboss=False)

        layout.row().operator("pribambase.reference_add")
        layout.row().operator("pribambase.reference_reload")
        layout.row().operator("pribambase.reference_reload_all")
