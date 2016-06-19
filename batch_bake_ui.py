import bpy
from bpy.types import Panel

###########################################################################
class CyclesButtonsPanel:
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    COMPAT_ENGINES = {'CYCLES'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        ob = context.active_object
        return rd.engine in cls.COMPAT_ENGINES and ob and ob.type == 'MESH'

class BBake_Panel(CyclesButtonsPanel, Panel):
    bl_label = "BBake"
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'CYCLES'}

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        cscene = scene.cycles
        cbk = scene.render.bake
        ob = context.active_object
        bbake = ob.bbake
        ob_settings = bbake.ob_settings

        col = layout.column()

        row=col.row(align=True)
        row.operator('scene.bbake_bake_selected', icon='RENDER_STILL', text='Bake Selected Objects')
        row.operator('scene.bbake_bake_selected', icon='RENDER_STILL', text='Bake All Objects').all=True
        col.separator()
        col.separator()
        col.prop(ob_settings, 'use', text='Bake this object ("%s")' %ob.name, toggle=0)

        if ob_settings.use:
            ### SELECTED TO ACTIVE SETTINGS
            box = col.box()
            box.prop(ob_settings, 'path')
            row = box.row()
            row.prop(ob_settings, 'use_selected_to_active')
            if ob_settings.use_selected_to_active:
                if ob_settings.sources:
                    sources = [s.strip() for s in ob_settings.sources.split(',')]
                    if len(sources) == 1:
                        row.prop(ob_settings, 'align')

                row = box.row()
                row.prop(ob_settings, 'use_cage')
                if ob_settings.use_cage:
                    #row.prop(ob_settings, 'cage_object', icon='OBJECT_DATAMODE')
                    row.prop_search(ob_settings, "cage_object", scene, "objects", text="")

                row=box.row()
                if ob_settings.use_cage:
                    ray_name = 'Extrusion'
                else:
                    ray_name = 'Ray Distance'
                row.prop(ob_settings, 'cage_extrusion', text=ray_name)

                subbox = box.box()
                row=subbox.row()
                row.label('Source Objects:')
                row.operator('object.set_bbake_sources', icon='FORWARD', text='Set Sources')
                row=subbox.row()
                if ob_settings.sources:
                    row.prop(ob_settings, 'sources', text='')

            ### AOVs SETTINGS
            box = col.box()

            row = box.row()
            row.label('AOVs:')
            row.operator('object.bbake_copy_settings', text='Copy Settings', icon='COPY_ID')

            def draw_aov_header(layout, aov):
                row = layout.row()
                row.prop(aov, 'use', text=aov.name)
                if aov.dimensions == 'CUSTOM':
                    row.prop(aov, 'dimensions_custom', text='')
                row.prop(aov, 'dimensions', text='')

            def draw_pass_types(layout, aov):
                if aov.use:
                    row = layout.row(align=True)
                    row.prop(aov, 'use_pass_direct', toggle=True)
                    row.prop(aov, 'use_pass_indirect', toggle=True)
                    row.prop(aov, 'use_pass_color', toggle=True)

            def draw_pass_types_combined(layout, aov):
                if aov.use:
                    row=layout.row()
                    row.prop(aov, 'use_pass_ao')
                    row.prop(aov, 'use_pass_emit')
                    row=layout.row(align=True)
                    row.prop(aov, 'use_pass_direct', toggle=True)
                    row.prop(aov, 'use_pass_indirect', toggle=True)
                    row=layout.row()
                    row.prop(aov, 'use_pass_diffuse')
                    row.prop(aov, 'use_pass_transmission')
                    row=layout.row()
                    row.prop(aov, 'use_pass_glossy')
                    row.prop(aov, 'use_pass_subsurface')

            def draw_pass_types_normal(layout, aov):
                if aov.use:
                    layout.label('Normal Settings:')
                    layout.prop(aov, "normal_space", text="Space")
                    row = layout.row(align=True)
                    row.label(text="Swizzle:")
                    row.prop(aov, "normal_r", text="")
                    row.prop(aov, "normal_g", text="")
                    row.prop(aov, "normal_b", text="")

            #COMBINED
            aov = bbake.aov_combined
            box_aov = box.box()
            draw_aov_header(box_aov, aov)
            draw_pass_types_combined(box_aov, aov)

            #DIFFUSE
            aov = bbake.aov_diffuse
            box_aov = box.box()
            draw_aov_header(box_aov, aov)
            draw_pass_types(box_aov, aov)

            #GLOSSY
            aov = bbake.aov_glossy
            box_aov = box.box()
            draw_aov_header(box_aov, aov)
            draw_pass_types(box_aov, aov)


            #TRANSMISSION
            aov = bbake.aov_transmission
            box_aov = box.box()
            draw_aov_header(box_aov, aov)
            draw_pass_types(box_aov, aov)

            #SUBSURFACE
            aov = bbake.aov_subsurface
            box_aov = box.box()
            draw_aov_header(box_aov, aov)
            draw_pass_types(box_aov, aov)

            #NORMAL
            aov = bbake.aov_normal
            box_aov = box.box()
            draw_aov_header(box_aov, aov)
            draw_pass_types_normal(box_aov, aov)

            #AO
            aov = bbake.aov_ao
            box_aov = box.box()
            draw_aov_header(box_aov, aov)

            #SHADOW
            aov = bbake.aov_shadow
            box_aov = box.box()
            draw_aov_header(box_aov, aov)

            #EMIT
            aov = bbake.aov_emit
            box_aov = box.box()
            draw_aov_header(box_aov, aov)

            #UV
            aov = bbake.aov_uv
            box_aov = box.box()
            draw_aov_header(box_aov, aov)

            #ENVIRONMENT
            aov = bbake.aov_environment
            box_aov = box.box()
            draw_aov_header(box_aov, aov)


def register():
    #print('\nREGISTER:\n', __name__)
    bpy.utils.register_class(BBake_Panel)

def unregister():
    #print('\nUN-REGISTER:\n', __name__)
    bpy.utils.unregister_class(BBake_Panel)
