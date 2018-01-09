# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from math import *
from bpy.props import StringProperty
from sverchok.node_tree import SverchCustomTreeNode
from sverchok.data_structure import (updateNode)


class SvFormulaDeformNode(bpy.types.Node, SverchCustomTreeNode):
    ''' Deform Verts by Math '''
    bl_idname = 'SvFormulaDeformNode'
    bl_label = 'Deform by formula'
    bl_icon = 'OUTLINER_OB_EMPTY'

    ModeX = StringProperty(name='formulaX', default='x', update=updateNode)
    ModeY = StringProperty(name='formulaY', default='y', update=updateNode)
    ModeZ = StringProperty(name='formulaZ', default='z', update=updateNode)

    def sv_init(self, context):
        self.inputs.new('VerticesSocket', 'Verts')
        self.outputs.new('VerticesSocket', 'Verts')

    def draw_buttons(self, context, layout):
        for element in 'XYZ':
            row = layout.row()
            split = row.split(percentage=0.15)
            split.label(element)
            split.split().prop(self, "Mode"+element, text='')

    def process(self):
        Io = self.inputs[0]
        Oo = self.outputs[0]
        if Oo.is_linked:
            V = Io.sv_get()
            IndObj = range(len(V))
            exec("Oo.sv_set([[("+self.ModeX+","+self.ModeY+","+self.ModeZ+") for (x, y, z),i in zip(L,range(len(L)))] for L,I in zip(V,IndObj)])")

    def update_socket(self, context):
        self.update()


def register():
    bpy.utils.register_class(SvFormulaDeformNode)


def unregister():
    bpy.utils.unregister_class(SvFormulaDeformNode)
