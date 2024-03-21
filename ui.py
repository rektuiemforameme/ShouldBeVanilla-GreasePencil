import bpy
    

def select_menu_additions(self, context):
    self.layout.operator("shouldbevanilla.multiframe_select_from_active")

def layer_context_menu_aditions(self, context):
    self.layout.separator()
    self.layout.operator("shouldbevanilla.gp_batch_add_mask")
    self.layout.operator("shouldbevanilla.gp_batch_set_layer_prop")

def register():
    bpy.types.VIEW3D_MT_select_edit_gpencil.prepend(select_menu_additions)
    bpy.types.GPENCIL_MT_layer_context_menu.append(layer_context_menu_aditions)
    
def unregister():
    bpy.types.VIEW3D_MT_select_edit_gpencil.remove(select_menu_additions)
    bpy.types.GPENCIL_MT_layer_context_menu.remove(layer_context_menu_aditions)