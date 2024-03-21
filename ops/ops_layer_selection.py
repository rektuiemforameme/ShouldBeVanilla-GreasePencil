import bpy
from bpy.props import EnumProperty

class ShouldBeVanilla_OT_gp_batch_adjust_layer_selection(bpy.types.Operator):
    """Adjust layer selection in dialogue"""
    bl_idname = "shouldbevanilla.gp_batch_adjust_layer_selection"
    bl_label = "Adjust Selection"
    bl_options = {'REGISTER', 'UNDO'}

    mode : EnumProperty(items = [('INVERT', 'Invert', 'Invert current selection', 'NONE', 0), 
                                ('DESELECT_ALL', 'Deselect All', 'Deselect All', 'NONE',1),
                                ('SELECT_ALL', 'Select All', 'Select All', 'NONE',2)], default='SELECT_ALL', 
                                name = "Selection Adjustment Mode", description = "Type of adjustment to make to the current selection") # type: ignore

    def execute(self, context):
        if hasattr(context.scene,'shouldbevanilla_temp_selection_list'):
            selection_list = context.scene.shouldbevanilla_temp_selection_list
            match self.mode:
                case 'INVERT':
                    for item in selection_list:
                        item.select = not item.select
                case 'DESELECT_ALL':
                    for item in selection_list:
                        item.select = False
                case 'SELECT_ALL':
                    for item in selection_list:
                        item.select = True
            return {'FINISHED'}
        return {'CANCELLED'}
    
    @classmethod
    def description(cls, context, properties):
        match properties.mode:
            case 'INVERT':
                return 'Invert current selection so that selected layers will be deselected and unselected layers will be selected'
            case 'DESELECT_ALL':
                return 'Deselect All'
            case 'SELECT_ALL':
                return 'Select All'
            
def register():
    bpy.utils.register_class(ShouldBeVanilla_OT_gp_batch_adjust_layer_selection)
    
def unregister():
    bpy.utils.unregister_class(ShouldBeVanilla_OT_gp_batch_adjust_layer_selection)