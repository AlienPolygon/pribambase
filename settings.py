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



class SB_State(bpy.types.PropertyGroup):
    # once, here were some session settings
    # they may come useful again so let's keep it wired
    pass


class SB_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    port: bpy.props.IntProperty(
        name="Port",
        description="Port used by the websocket server. Aseprite plugin must have the same value to connect",
        default=34613,
        min=1025,
        max=65535)

    localhost: bpy.props.BoolProperty(
        name="Only Local Connections",
        description="Only accept connections from localhost (127.0.0.1)",
        default=True)

    autostart: bpy.props.BoolProperty(
        name="Start Automatically",
        description="Set up the connection when Blender starts. Enabling increases blender's launch time",
        default=False)

    uv_layer:bpy.props.StringProperty(
        name="UV Layer Name",
        description="Name of the reference layer that will be created/used to display the UVs in Aseprite",
        default="UVMap")

    uv_scale:bpy.props.FloatProperty(
        name="UV Scale",
        description="Default resolution of the UV layer relative to the texture size",
        default=8.0,
        min=0.0,
        max=50.0)

    uv_color: bpy.props.FloatVectorProperty(
        name="UV Color",
        description="Default color to draw the UVs with",
        size=4,
        default=(0.0, 0.0, 0.0, 0.45),
        min=0.0,
        max=1.0,
        subtype='COLOR')

    uv_aa: bpy.props.BoolProperty(
        name="Anti-aliased UVs",
        description="Apply anti-aliasing to the UV map",
        default=True)

    uv_weight: bpy.props.FloatProperty(
        name="UV Thickness",
        description="Default thickness of the UV map with scale appied. For example, if `UV scale` is 2 and thickness is 3, the lines will be 1.5 pixel thick in aseprite",
        default=4.0)


    def template_box(self, layout, label="Box"):
        row = layout.row().split(factor=0.15)
        row.label(text=label)
        return row.box()


    def draw(self, context):
        layout = self.layout

        box = self.template_box(layout, label="UV Map:")

        box.row().prop(self, "uv_layer", text="Layer Name")
        box.row().prop(self, "uv_color")

        row = box.row()
        row.prop(self, "uv_scale", text="Scale")
        row.prop(self, "uv_weight", text="Thickness")
        row.prop(self, "uv_aa", text="Anti-aliasing")

        box = self.template_box(layout, label="Connection:")

        box.row().prop(self, "autostart")

        row = box.row()
        row.enabled = not addon.server_up
        row.prop(self, "localhost")
        row.prop(self, "port")

        if addon.server_up:
            box.row().operator("pribambase.stop_server")
        else:
            box.row().operator("pribambase.start_server")


class SB_OT_preferences(bpy.types.Operator):
    bl_idname = "pribambase.preferences"
    bl_label = "Preferences"
    bl_description = "Open this addon's settings"

    def execute(self, context):
        bpy.ops.preferences.addon_show(module=__package__)

        return {'FINISHED'}