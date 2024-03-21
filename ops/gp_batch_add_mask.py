import bpy
from bpy.props import IntProperty, CollectionProperty
from ..common.drawing import draw_layer_selection_list, LayerSelected, ShouldBeVanillaUIListItemString

class ShouldBeVanilla_OT_gp_batch_add_mask(bpy.types.Operator):
    """Opens a menu to add masks to multiple layers at once"""
    bl_idname = "shouldbevanilla.gp_batch_add_mask"
    bl_label = "Batch Add Mask(s)"
    bl_options = {'REGISTER', 'UNDO'}
    
    gp = None
    cleaned = False

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL' and len(ob.data.layers) > 1

    def invoke(self, context, event):
        bpy.types.Scene.shouldbevanilla_temp_selection_list = CollectionProperty(type=LayerSelected)
        bpy.types.Scene.shouldbevanilla_temp_mask_list = CollectionProperty(type=ShouldBeVanillaUIListItemString)
        bpy.types.Scene.shouldbevanilla_temp_mask_list_index = IntProperty()
        context.scene.shouldbevanilla_temp_selection_list.clear()
        context.scene.shouldbevanilla_temp_mask_list.clear()
        bpy.ops.shouldbevanilla.ui_list_new_item()

        self.gp = context.object.data
        for l in self.gp.layers:
            item = context.scene.shouldbevanilla_temp_selection_list.add()
            item.name = l.info
            item.select = False
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        #####   Selection List  #####
        draw_layer_selection_list(self,context,layout)
        #####   Mask List   #####
        box = layout.box()
        box.label(text="Masks")
        row = box.row()
        row.template_list("GPLAYER_UL_string_search", "Mask List", context.scene, "shouldbevanilla_temp_mask_list", context.scene, "shouldbevanilla_temp_mask_list_index", rows=1)
            #ADD and REMOVE
        col = row.column(align=True)
        col.operator('shouldbevanilla.ui_list_new_item', text='',icon='ADD')
        col.operator('shouldbevanilla.ui_list_delete_item', text='',icon='REMOVE')
        
    def execute(self, context):
        if hasattr(context.scene,'shouldbevanilla_temp_selection_list') and hasattr(context.scene,'shouldbevanilla_temp_mask_list'):
            selection_list = context.scene.shouldbevanilla_temp_selection_list
            mask_list = context.scene.shouldbevanilla_temp_mask_list
            mask_list_names = [item.name for item in mask_list]
            mask_list_layers = [l for n in mask_list_names if (l := self.gp.layers.get(n))]
            selected_list_names = [item.name for item in selection_list if (item.select and item.name not in mask_list_names)]

            for n in selected_list_names:
                l = self.gp.layers.get(n)
                if l:
                    l.use_mask_layer = True
                    for m in mask_list_layers:
                        l.mask_layers.add(m)
            self.clean(context)
            return {'FINISHED'}
        self.clean(context)
        return {'CANCELLED'}
    
    def cancel(self, context):
        self.clean(context)

    def clean(self, context):
        if not self.cleaned:
            if hasattr(context.scene,'shouldbevanilla_temp_selection_list'):
                context.scene.property_unset('shouldbevanilla_temp_selection_list')
                del bpy.types.Scene.shouldbevanilla_temp_selection_list
            if hasattr(context.scene,'shouldbevanilla_temp_mask_list'):
                context.scene.property_unset('shouldbevanilla_temp_mask_list')
                del bpy.types.Scene.shouldbevanilla_temp_mask_list
            if hasattr(context.scene,'shouldbevanilla_temp_mask_list_index'):
                context.scene.property_unset('shouldbevanilla_temp_mask_list_index')
                del bpy.types.Scene.shouldbevanilla_temp_mask_list_index
            self.cleaned = True

def register():
    bpy.utils.register_class(ShouldBeVanilla_OT_gp_batch_add_mask)
    
def unregister():
    bpy.utils.unregister_class(ShouldBeVanilla_OT_gp_batch_add_mask)