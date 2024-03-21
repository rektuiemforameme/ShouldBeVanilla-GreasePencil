import bpy
from bpy.props import EnumProperty

#Thanks to Diego Gangl and the tutorial at https://sinestesia.co/blog/tutorials/using-uilists-in-blender/ for these UIList operators
class LIST_OT_NewItem(bpy.types.Operator): 
    #Add a new item to the list.
    bl_idname = "shouldbevanilla.ui_list_new_item" 
    bl_label = "Add a new item"
    def execute(self, context):
        if hasattr(context.scene, 'shouldbevanilla_temp_mask_list'):
            l = context.scene.shouldbevanilla_temp_mask_list
            l.add()

            other_layers = [item.name for item in l]
            gp = context.object.data
            if len(l) > 1: #There are already layers in the list. Find the last one, and try to add the layer that is next in line.
                last_layer_index = 0
                for n in reversed(l):
                    if n.name != '':
                        try:
                            last_layer_index = gp.layers.find(n.name)
                            if last_layer_index == -1: continue
                            for li in range(last_layer_index-1,-1,-1):          #Backwards
                                if gp.layers[li].info not in other_layers:
                                    l[len(l)-1].name = gp.layers[li].info
                                    return{'FINISHED'}
                            for li in range(last_layer_index+1,len(gp.layers)): #Try going forwards
                                if gp.layers[li].info not in other_layers:
                                    l[len(l)-1].name = gp.layers[li].info
                                    return{'FINISHED'}
                        except ValueError:
                            continue
            l[len(l)-1].name = gp.layers.active.info    #Default to the active layer if this is the first item being added

            return{'FINISHED'}
        return{'CANCELLED'}
    
class LIST_OT_DeleteItem(bpy.types.Operator): 
    #Delete the selected item from the list. 
    bl_idname = "shouldbevanilla.ui_list_delete_item" 
    bl_label = "Deletes an item"
    def execute(self, context):
        if hasattr(context.scene, 'shouldbevanilla_temp_mask_list') and hasattr(context.scene, 'shouldbevanilla_temp_mask_list_index'):
            l = context.scene.shouldbevanilla_temp_mask_list
            i = context.scene.shouldbevanilla_temp_mask_list_index
            l.remove(i) 
            context.scene.shouldbevanilla_temp_mask_list_index = min(max(0, i - 1), len(l) - 1)
            return{'FINISHED'}
        return{'CANCELLED'}
    
class LIST_OT_MoveItem(bpy.types.Operator): 
    #Move an item in the list. 
    bl_idname = "shouldbevanilla.ui_list_move_item" 
    bl_label = "Move an item in the list" 
    direction : EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),))
    def execute(self, context):
        if hasattr(context.scene, 'shouldbevanilla_temp_mask_list') and hasattr(context.scene, 'shouldbevanilla_temp_mask_list_index'):
            l = context.scene.shouldbevanilla_temp_mask_list
            i = context.scene.shouldbevanilla_temp_mask_list_index
            neighbor = i + (-1 if self.direction == 'UP' else 1) 
            l.move(neighbor, i)
            list_length = len(l) - 1 # (index starts at 0) 
            new_index = i + (-1 if self.direction == 'UP' else 1) 
            context.scene.shouldbevanilla_temp_mask_list_index = max(0, min(new_index, list_length))
            return{'FINISHED'}
        return{'CANCELLED'}
    
def register():
    bpy.utils.register_class(LIST_OT_NewItem)
    bpy.utils.register_class(LIST_OT_DeleteItem)
    bpy.utils.register_class(LIST_OT_MoveItem)
    
def unregister():
    bpy.utils.unregister_class(LIST_OT_NewItem)
    bpy.utils.unregister_class(LIST_OT_DeleteItem)
    bpy.utils.unregister_class(LIST_OT_MoveItem)