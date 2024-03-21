import bpy
    
class ShouldBeVanilla_OT_multiframe_select_from_active(bpy.types.Operator):
    """Selects the same strokes that are selected in the active frame in other selected frames.
Only works for frames that have duplicated strokes that haven't had their order changed"""
    bl_idname = "shouldbevanilla.multiframe_select_from_active"
    bl_label = "Multiframe Select from Active"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(self, context):
        ob = context.object
        return ob and ob.type == 'GPENCIL' and ob.mode == 'EDIT_GPENCIL' and ob.data.use_multiedit

    def execute(self, context):
        gp = context.active_object.data
        warned = False  #Tracks if the user has had any warnings for incompatible strokes
        if context.tool_settings.gpencil_selectmode_edit == 'STROKE':
            for lr in gp.layers:
                if not lr.hide and not lr.lock:
                    select_status = [s.select for s in lr.active_frame.strokes] #Stores which strokes are selected in the active frame
                    stat_len = len(select_status)
                    for fr in lr.frames:
                        if fr.select and fr != lr.active_frame:
                            if len(fr.strokes) != stat_len:
                                self.report({'ERROR'}, f"Layer '{lr.info}', frame {fr.frame_number}, has a different number of strokes ({len(fr.strokes)}) than the active frame ({stat_len})")
                                warned = True
                                continue
                            for i in range(len(select_status)):
                                fr.strokes[i].select = select_status[i]
        elif context.tool_settings.gpencil_selectmode_edit == 'SEGMENT' or context.tool_settings.gpencil_selectmode_edit == 'POINT':
            original_frame_number = context.scene.frame_current
            for lr in gp.layers:
                if not lr.hide and not lr.lock:
                    src_frame = lr.active_frame
                    select_status = [[p.select for p in s.points] for s in src_frame.strokes]   #Get a list of lists for the selection status of points in the active frame
                    stat_len = len(select_status)
                    for fr in lr.frames:
                        if fr.select and fr != src_frame:
                            if len(fr.strokes) != stat_len:
                                self.report({'ERROR'}, f"Layer '{lr.info}', frame {fr.frame_number}, has a different number of strokes ({len(fr.strokes)}) than the active frame ({stat_len})")
                                warned = True
                                continue
                            context.scene.frame_set(fr.frame_number)    #For some reason, setting a point's select property in multiframe won't work unless it is in the active frame. Weird.
                            for si in range(len(select_status)):
                                st = fr.strokes[si]
                                select_p_status = select_status[si]     #Selection status of points in the source stroke
                                stat_p_len = len(select_p_status)
                                if len(st.points) != stat_p_len:
                                    self.report({'ERROR'}, f"Layer '{lr.info}', frame {fr.frame_number}, has a different number of points in stroke {si} ({len(st.points)}) than the active frame ({stat_p_len})")
                                    warned = True
                                    continue
                                for pi in range(stat_p_len):
                                    st.points[pi].select = select_p_status[pi]
                                
                    context.scene.frame_set(original_frame_number) #Go back to the original frame we were on before.
        if warned:
            self.report({'ERROR'}, f"Only frames with the same number of strokes and points are compatible with this operator")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ShouldBeVanilla_OT_multiframe_select_from_active)
    
def unregister():
    bpy.utils.unregister_class(ShouldBeVanilla_OT_multiframe_select_from_active)