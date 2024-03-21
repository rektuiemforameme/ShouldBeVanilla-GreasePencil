from . import ui, util_ops
from .ops import gp_batch_add_mask, gp_batch_set_layer_prop, gp_select_stroke_multiframe, ops_layer_selection
from .common import drawing

bl_info = {
    "name": "Should be Vanilla: Grease Pencil",
    "author": "Matt Thompson",
    "version": (1, 0),
    "blender": (4, 0, 1),
    "location": "View3D > Sidebar (N)",
    "description": "A small collection of utilities that really should be in vanilla blender, but they're not, so here they are.",
    "warning": "",
    "doc_url": "",
    "category": "Grease Pencil",
}



def register():
    drawing.register()
    gp_batch_add_mask.register()
    gp_batch_set_layer_prop.register()
    gp_select_stroke_multiframe.register()
    util_ops.register()
    ui.register()
    ops_layer_selection.register()

def unregister():
    ops_layer_selection.unregister()
    ui.unregister()
    util_ops.unregister()
    gp_batch_set_layer_prop.unregister()
    gp_batch_add_mask.unregister()
    gp_select_stroke_multiframe.unregister()
    drawing.unregister()

if __name__ == "__main__":
    register()