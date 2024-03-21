import bpy
import math
from bpy.types import PropertyGroup, UIList
from bpy.props import StringProperty, BoolProperty, IntProperty

class LayerSelected(PropertyGroup):
    name: StringProperty(name="", default="")
    select: BoolProperty(name="Selected", description="Whether or not this layer is selected for modification", default=True)

class ShouldBeVanillaUIListItemString(PropertyGroup):
    name : StringProperty()
    id : IntProperty()

class GPLAYER_UL_string_search(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.08)
        split.label(text="",icon='LAYER_ACTIVE' if context.scene.shouldbevanilla_temp_mask_list_index == index else 'LAYER_USED')
        split.prop_search(item, "name", context.object.data, "layers", text="",icon='NONE')

def draw_layer_selection_list(self, context, layout=None):
    if layout is None:
        layout = self.layout
    
    selection_list = context.scene.shouldbevanilla_temp_selection_list
    use_masks = hasattr(context.scene, 'shouldbevanilla_temp_mask_list')
    box = layout.box()
    if use_masks:
        mask_list = context.scene.shouldbevanilla_temp_mask_list
        mask_list_names = [item.name for item in mask_list]
        box.label(text="Layers to add masks to")
        col = box.column_flow(columns=math.ceil((len(selection_list)-len(mask_list_names))/30))
    else:
        box.label(text="Layers to adjust")
        col = box.column_flow(columns=math.ceil(len(selection_list)/30))

    
    for item in reversed(selection_list):
        if not use_masks or item.name not in mask_list_names:    #Only render the layers that aren't marked as masks if we're using masks
            col.prop(item, "select", text=item["name"],toggle=True)
    #Selection Adjustment operators
    row = box.row(align=True)
    row.operator('shouldbevanilla.gp_batch_adjust_layer_selection', text='', icon='RADIOBUT_OFF').mode='DESELECT_ALL'
    row.operator('shouldbevanilla.gp_batch_adjust_layer_selection', text='', icon='ARROW_LEFTRIGHT').mode='INVERT'
    row.operator('shouldbevanilla.gp_batch_adjust_layer_selection', text='', icon='RADIOBUT_ON').mode='SELECT_ALL'

def register():
    bpy.utils.register_class(GPLAYER_UL_string_search)
    bpy.utils.register_class(ShouldBeVanillaUIListItemString)
    bpy.utils.register_class(LayerSelected)
    
def unregister():
    bpy.utils.unregister_class(LayerSelected)
    bpy.utils.unregister_class(GPLAYER_UL_string_search)
    bpy.utils.unregister_class(ShouldBeVanillaUIListItemString)