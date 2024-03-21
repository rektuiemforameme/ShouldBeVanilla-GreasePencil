import bpy
from bpy.props import PointerProperty

def init_selected_points(context, self):
    if context.active_object.type != 'GPENCIL':
        return
    gp = context.active_object.data
    
    #list comprehension go brrr
    self.selected_points = [p
    for lr in gp.layers
        if not lr.lock and not lr.hide  #Respect layer locking and visibility
            for fr in ([fr for fr in lr.frames if fr.select] if gp.use_multiedit else [lr.active_frame])    #Respect multiframe editing settings
                for s in fr.strokes
                    if s.select
                        for p in s.points
                            if p.select]
    
def get_property_group_from_props(props,group_name='TempPropertyGroup'):
    attributes = {}
    for prop in props:
        att_identifier = prop.identifier
        att_type = type(prop)
        prop_options = set()
        if prop.is_hidden:  prop_options.add('HIDDEN')
        if prop.is_skip_save:  prop_options.add('SKIP_SAVE')
        if prop.is_animatable:  prop_options.add('ANIMATABLE')
        if prop.is_library_editable:  prop_options.add('LIBRARY_EDITABLE')
        if prop.is_path_output:  prop_options.add('OUTPUT_PATH')
        if hasattr(prop,'array_dimensions'):
            if prop.array_dimensions[1] == 0:       #1D Array
                array_size = prop.array_dimensions[0]
                array_default = prop.default_array
            else:
                if att_identifier == 'matrix_inverse':
                    pass
                array_size = [num for num in prop.array_dimensions if num > 0]
                if prop.array_dimensions[2] == 0:   #2D Array
                    array_default = [[prop.default_array[array_size[0]*y + x] for y in range(array_size[1])] for x in range(array_size[0])]
                else:                               #3D Array
                    array_default = [[[prop.default_array[(array_size[0]*array_size[1]*z) + array_size[0]*y + x] for z in range(array_size[2])] for y in range(array_size[1])] for x in range(array_size[0])]
                
        match att_type:
            case bpy.types.BoolProperty:
                if not prop.is_array:
                    attributes[att_identifier] = bpy.props.BoolProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context,
                                                                        default=prop.default,
                                                                        options=prop_options,subtype=prop.subtype) # type: ignore
                else:   # BoolVectorProperty
                    attributes[att_identifier] = bpy.props.BoolVectorProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context,
                                                                        size=array_size, default=array_default,
                                                                        options=prop_options,subtype=prop.subtype) # type: ignore
            case bpy.types.EnumProperty:
                attributes[att_identifier] = bpy.props.EnumProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context,
                                                                    items=[(item.identifier,item.name,item.description,item.icon,i) for i,item in enumerate(prop.enum_items)],
                                                                    default=prop.default,options=prop_options) # type: ignore
            case bpy.types.FloatProperty:
                if not prop.is_array:
                    attributes[att_identifier] = bpy.props.FloatProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context, 
                                                                        default=prop.default,min=prop.hard_min,max=prop.hard_max,soft_min=prop.soft_min,soft_max=prop.soft_max,   
                                                                        step=prop.step,precision=prop.precision,unit=prop.unit,
                                                                        options=prop_options,subtype=prop.subtype) # type: ignore
                else:   # FloatVectorProperty
                    attributes[att_identifier] = bpy.props.FloatVectorProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context, 
                                                                        min=prop.hard_min,max=prop.hard_max,soft_min=prop.soft_min,soft_max=prop.soft_max,   
                                                                        size=array_size,step=prop.step,precision=prop.precision,unit=prop.unit,default=array_default,
                                                                        options=prop_options,subtype=prop.subtype) # type: ignore
            case bpy.types.IntProperty:
                if not prop.is_array:
                    attributes[att_identifier] = bpy.props.IntProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context, 
                                                                        default=prop.default,min=prop.hard_min,max=prop.hard_max,soft_min=prop.soft_min,soft_max=prop.soft_max,   
                                                                        step=prop.step,
                                                                        options=prop_options,subtype=prop.subtype) # type: ignore
                else:   # IntVectorProperty
                    attributes[att_identifier] = bpy.props.IntVectorProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context, 
                                                                    min=prop.hard_min,max=prop.hard_max,soft_min=prop.soft_min,soft_max=prop.soft_max,   
                                                                    size=array_size,step=prop.step,default=array_default,
                                                                    options=prop_options,subtype=prop.subtype) # type: ignore
            case bpy.types.PointerProperty:
                attributes[att_identifier] = bpy.props.PointerProperty(type=type(prop.fixed_type),name=prop.name,description=prop.description,
                                                                    translation_context=prop.translation_context, options=prop_options) # type: ignore
            case bpy.types.StringProperty:
                attributes[att_identifier] = bpy.props.StringProperty(name=prop.name,description=prop.description,translation_context=prop.translation_context,
                                                                    default=prop.default,maxlen=prop.length_max,
                                                                    options=prop_options,subtype=prop.subtype) # type: ignore
            case _:
                continue
    data = {
        'bl_label': group_name,
        'bl_idname': f"sbv.{group_name}",
        '__annotations__': attributes
    }
    property_group_class = type(group_name, (bpy.types.PropertyGroup,), data)
    bpy.utils.register_class(property_group_class)
    setattr(bpy.types.Scene, group_name, PointerProperty(type=property_group_class))

    return property_group_class