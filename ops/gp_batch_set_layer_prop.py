import bpy
from bpy.types import PropertyGroup
from bpy.props import CollectionProperty, EnumProperty, PointerProperty
from ..common.drawing import draw_layer_selection_list, LayerSelected
from ..util_funcs import get_property_group_from_props

def get_layer_prop_icon(prop_name):
    match prop_name:
        case 'blend_mode':
            return 'OVERLAY'
        case 'channel_color':
            return 'KEYTYPE_KEYFRAME_VEC'
        case 'hide':
            return 'HIDE_OFF'
        case 'info':
            return 'INFO'
        case 'line_change':
            return 'MOD_THICKNESS'
        case 'lock':
            return 'LOCKED'
        case 'lock_frame':
            return 'KEY_DEHLT'
        case 'lock_material':
            return 'MATERIAL'
        case 'matrix_inverse':
            return 'VIEW_ORTHO'
        case 'opacity':
            return 'MOD_OPACITY'
        case 'parent':
            return 'ORIENTATION_PARENT'
        case 'parent_type':
            return 'OBJECT_DATA'
        case 'parent_bone':
            return 'BONE_DATA'
        case 'pass_index':
            return 'NODE_COMPOSITING'
        case 'select':
            return 'DECORATE_KEYFRAME'
        case 'show_in_front':
            return 'SEQ_SPLITVIEW'
        case 'show_points':
            return 'CON_TRACKTO'
        case 'tint_color':
            return 'COLORSET_10_VEC'
        case 'use_lights':
            return 'OUTLINER_OB_LIGHT'
        case 'use_mask_layer':
            return 'MOD_MASK'
        case 'use_onion_skinning':
            return 'ONIONSKIN_ON'
        case 'use_solo_mode':
            return 'SOLO_ON'
        case 'vertex_paint_opacity':
            return 'VPAINT_HLT'
        case 'viewlayer_render':
            return 'RENDERLAYERS'
        #Transforms
        case 'location':
            return 'ORIENTATION_VIEW'
        case 'rotation':
            return 'ORIENTATION_GIMBAL'
        case 'scale':
            return 'MOD_LENGTH'
        case _:
            return 'NONE'
#Some property names don't correspond to the names you see in blender's ui. So fix them.
def get_layer_prop_name(prop_identifier, prop_name):
    match prop_identifier:
        case 'info':
            return 'Name'
        case 'line_change':
            return 'Stroke Thickness'
        case 'use_solo_mode':
            return 'Show Only on Keyframed'
        case _:
            return prop_name

class ShouldBeVanilla_OT_gp_batch_set_layer_prop(bpy.types.Operator):
    """Opens a menu to set a property of multiple layers at once"""
    bl_idname = "shouldbevanilla.gp_batch_set_layer_prop"
    bl_label = "Batch Set Layer Property"
    bl_options = {'REGISTER', 'UNDO'}
    
    gp = None
    cleaned = False     #I don't like it any more than you do.
    props_unfiltered = bpy.types.GPencilLayer.bl_rna.properties
    props = [bpy.types.GPencilLayer.bl_rna.properties[k] for k in props_unfiltered.keys() 
            if not bpy.types.GPencilLayer.bl_rna.properties[k].is_readonly and not bpy.types.GPencilLayer.bl_rna.properties[k].is_hidden and 
            'annotation' not in k and 'annotation' not in bpy.types.GPencilLayer.bl_rna.properties[k].description]
    prop_identifiers = [prop.identifier for prop in props]
    prop_selected : EnumProperty(name = "Property Selected", description = "The property to set in the selected layers", items = 
                                 [(id,get_layer_prop_name(id,bpy.types.GPencilLayer.bl_rna.properties[id].name),bpy.types.GPencilLayer.bl_rna.properties[id].description,get_layer_prop_icon(id),i) 
                                  for i,id in enumerate(prop_identifiers)]) # type: ignore
    
    property_group_class = None
    property_group_name = 'TempSBVPropertyGroup'
    bool_icons = {  #Pairs of (False, True) icons for some properties
        'default':              ('CHECKBOX_DEHLT','CHECKBOX_HLT'),
        'hide':                 ('HIDE_OFF','HIDE_ON'),
        'lock':                 ('UNLOCKED','LOCKED'),
        'use_lights':           ('OUTLINER_DATA_LIGHT','OUTLINER_OB_LIGHT'),
        'use_mask_layer':       ('LAYER_ACTIVE','MOD_MASK'),
        'use_onion_skinning':   ('ONIONSKIN_OFF','ONIONSKIN_ON'),
        'use_solo_mode':        ('SOLO_OFF','SOLO_ON'),
        'select':               ('KEYFRAME','KEYFRAME_HLT'),
    }

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL' and len(ob.data.layers) > 0

    def invoke(self, context, event):
        bpy.types.Scene.shouldbevanilla_temp_selection_list = CollectionProperty(type=LayerSelected)
        context.scene.shouldbevanilla_temp_selection_list.clear()
        
        self.property_group_class = get_property_group_from_props(self.props,self.property_group_name)
        
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
        #####   Property to set   #####
        if property_group := getattr(context.scene, self.property_group_name):
            box = layout.box()
            box.label(text="Property to set")
            col = box.column(align=True)
            col.prop(self, 'prop_selected',text='')
            prop_selected_prop = getattr(property_group,self.prop_selected)
            match self.prop_selected:
                case 'viewlayer_render':
                    col.prop_search(property_group,'viewlayer_render',context.scene,'view_layers',text='')
                case 'parent_bone':
                    skellington = None
                    for item in context.scene.shouldbevanilla_temp_selection_list:  #Try to find the skellington to use to find the bones in the layers
                        if item.select and (l := self.gp.layers[item.name]) and l.parent_type == 'BONE' and (obj := l.parent):
                            skellington = obj.data
                            break
                    if skellington:
                        col.prop_search(property_group, 'parent_bone', skellington, "bones", text="",icon='NONE')
                    else:   
                        col.prop(property_group,self.prop_selected,text='',icon='BONE_DATA')
                case _:
                    if isinstance(prop_selected_prop, bool):
                        col.prop(property_group,self.prop_selected,text='',toggle=True, icon=self.bool_icons.get(self.prop_selected,('CHECKBOX_DEHLT','CHECKBOX_HLT'))[prop_selected_prop])
                    else:
                        col.prop(property_group,self.prop_selected,text='')
        
        
    def execute(self, context):
        if hasattr(context.scene,'shouldbevanilla_temp_selection_list') and (property_group := getattr(context.scene, self.property_group_name)):
            selection_list = context.scene.shouldbevanilla_temp_selection_list
            selected_list_names = [item.name for item in selection_list if item.select]
            for n in selected_list_names:
                if l := self.gp.layers.get(n):
                    setattr(l,self.prop_selected,getattr(property_group,self.prop_selected))  #Set the selected layer's property to the corresponding property on the dummy
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
            delattr(bpy.types.Scene, self.property_group_name)
            if self.property_group_class:
                bpy.utils.unregister_class(self.property_group_class)
            
            self.cleaned = True

def register():
    bpy.utils.register_class(ShouldBeVanilla_OT_gp_batch_set_layer_prop)
    
def unregister():
    bpy.utils.unregister_class(ShouldBeVanilla_OT_gp_batch_set_layer_prop)




#BACKUP
'''
gp = None
    layer_active = None
    layer_dummy = None  #Instead of going down the rabbit hole of dynamic properties, I decided to just make a dummy layer that will hold the property we're changing. We'll delete it later
    cleaned = False     #I don't like it any more than you do.
    props = bpy.types.GPencilLayer.bl_rna.properties
    prop_selected : EnumProperty(name = "Property Selected", description = "The property to set in the selected layers", items = 
                                 [(k,get_layer_prop_name(k),bpy.types.GPencilLayer.bl_rna.properties[k].description,get_layer_prop_icon(k),i) 
                                  for i,k in enumerate(k for k in props.keys() 
                                if not bpy.types.GPencilLayer.bl_rna.properties[k].is_readonly and not bpy.types.GPencilLayer.bl_rna.properties[k].is_hidden and 
                                'annotation' not in k and 'annotation' not in bpy.types.GPencilLayer.bl_rna.properties[k].description)])

    @classmethod
    def poll(cls, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL' and len(ob.data.layers) > 0

    def invoke(self, context, event):
        bpy.types.Scene.shouldbevanilla_temp_selection_list = CollectionProperty(type=LayerSelected)
        context.scene.shouldbevanilla_temp_selection_list.clear()

        self.gp = context.object.data
        self.layer_active = self.gp.layers.active
        self.layer_dummy = self.gp.layers.new("_SBV_TEMP_LAYER_")

        for l in self.gp.layers:
            if l != self.layer_dummy:
                item = context.scene.shouldbevanilla_temp_selection_list.add()
                item.name = l.info
                item.select = False

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layer_main = self.layer_dummy
        #####   Selection List  #####
        draw_layer_selection_list(self,context,layout)
        #####   Property to set   #####
        box = layout.box()
        box.label(text="Property to set")
        row = box.row()
        row.prop(self, 'prop_selected',text='')
        try:
            match self.prop_selected:
                case 'viewlayer_render':    #Special case for viewlayer
                    box.prop_search(layer_main,self.prop_selected,context.scene,'view_layers',text='')
                case _:
                    box.prop(layer_main,self.prop_selected,text='')
        except: #I guess the layer didn't have that property. Bummer
            pass
        
        
    def execute(self, context):
        if hasattr(context.scene,'shouldbevanilla_temp_selection_list'):
            selection_list = context.scene.shouldbevanilla_temp_selection_list
            selected_list_names = [item.name for item in selection_list if item.select]

            for n in selected_list_names:
                if l := self.gp.layers.get(n):
                    setattr(l,self.prop_selected,getattr(self.layer_dummy,self.prop_selected))  #Set the selected layer's property to the corresponding property on the dummy
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
            self.gp.layers.remove(self.layer_dummy)
            self.gp.layers.active = self.layer_active
            self.cleaned = True
'''