import glm
import moderngl as mgl
import numpy as np
from shaderProgram import ShaderProgram
import pygame as pg
from PIL import Image



class Renderer():
    def __init__(self,app):
        self.isPostProcessEnable = False
        self.app = app
        self.ctx = app.ctx
        self.scene = app.scene
        self.WIN_SIZE = app.WIN_SIZE
        self.program = ShaderProgram(self.ctx)

        self.setup_framebuffers()
        self.setup_shaders()
        self.setup_vao()

    def setup_framebuffers(self):
        # Create a color texture and a depth texture for the scene framebuffer
        self.color_texture = self.ctx.texture(self.WIN_SIZE, 4)
        self.depth_texture = self.ctx.depth_texture(self.WIN_SIZE, alignment=1)
        self.normal_texture = self.ctx.texture(self.WIN_SIZE, 4, dtype='f4')

        # Create the scene framebuffer
        self.scene_framebuffer = self.ctx.framebuffer(
            color_attachments=[self.color_texture, self.normal_texture],
            depth_attachment=self.depth_texture
        )

        # Create the post-processing framebuffer
        self.output_texture = self.ctx.texture(self.WIN_SIZE, 4)
        self.post_processing_framebuffer = self.ctx.framebuffer(
            color_attachments=[self.output_texture]
        )

    def setup_shaders(self):

        self.shaderSRC = self.program.programs['src']
        self.shaderPostProcess = self.program.programs['postProcess']

    
    def setup_vao(self):
        # Define a full-screen quad for post-processing
        quad_vertices = np.array([
            -1.0, -1.0, 0.0, 0.0,  # Bottom left corner
            1.0, -1.0, 1.0, 0.0,   # Bottom right corner
            -1.0, 1.0, 0.0, 1.0,   # Top left corner
            1.0, 1.0, 1.0, 1.0,    # Top right corner
        ], dtype='f4')

        # Create indices for the full-screen quad
        quad_indices = np.array([0, 1, 2, 2, 1, 3], dtype='i4')

        # Create a Vertex Buffer Object (VBO) and Index Buffer Object (IBO)
        vbo = self.ctx.buffer(quad_vertices)
        ibo = self.ctx.buffer(quad_indices)

        # Create a VAO for the full-screen quad with the shader program
        self.quad_vao_postProcess = self.ctx.vertex_array(
            self.shaderPostProcess,
            [(vbo, '2f 2f', 'in_position', 'in_texcoord')],
            ibo
        )

        if self.isPostProcessEnable == False:
            self.quad_vao_postProcess = self.ctx.vertex_array(
            self.shaderSRC,
            [(vbo, '2f 2f', 'in_position', 'in_texcoord')],
            ibo
            )

        self.quad_vao = self.ctx.vertex_array(
            self.shaderSRC,
            [(vbo, '2f 2f', 'in_position', 'in_texcoord')],
            ibo
        )

        '''
        print(self.program.programs['postProcess']._members)

        uniforms = {name: self.shaderPostProcess[name] for name in self.shaderPostProcess
            if isinstance(self.shaderPostProcess[name], mgl.Uniform)}
        print(uniforms)
        '''

        #self.shaderPostProcess['texture1'].write((0,0,0))

    def render(self):
        # Render the scene
        self.render_scene()
        
        # Perform post-processing
        self.post_process()
        
        # Draw the final image to the screen
        self.display_result()

    #     self.ctx.clear()

    #     self.postProcess.preRender()

    #     self.ctx.enable(mgl.DEPTH_TEST)
    #     self.ctx.enable(mgl.CULL_FACE)

    #     self.scene.render()

    #     self.postProcess.render()

    def post_process(self):
        # Bind the post-processing framebuffer
        self.post_processing_framebuffer.use()
        
        # Clear the color buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        
        # Disable depth testing and face culling (not needed for post-processing)
        self.ctx.disable(mgl.DEPTH_TEST)
        self.ctx.disable(mgl.CULL_FACE)
        
        #print(self.shaderPostProcess.__iter__())

        self.shaderPostProcess['color_tex']  = 0
        # self.shaderPostProcess['depth_tex']  = 1
        # self.shaderPostProcess['normal_tex'] = 2

        # self.shaderPostProcess['light_direction'].write(self.app.light.dirLightDirection)
        # self.shaderPostProcess['INV_VIEW_MATRIX'].write(glm.inverse(self.app.camera.m_proj))
        self.shaderPostProcess['VIEWPORT_SIZE'].write(glm.vec2(self.app.WIN_SIZE))

        # Bind the color texture from the scene framebuffer

        self.color_texture.use(location=0)
        self.depth_texture.use(location=1)
        self.normal_texture.use(location=2)

        self.quad_vao_postProcess.render(mgl.TRIANGLE_STRIP)

    def drawText(self, x, y, text):              

        textSurface = self.app.debugFont.render(text, True, (255, 255, 255, 255), (0, 0, 0, 0))
        
        text_image = Image.frombytes('RGBA', textSurface.get_size(), pg.image.tostring(textSurface, 'RGBA'))

        text_data = np.array(text_image)

        text_texture = self.ctx.texture(size=textSurface.get_size(), components=4, data=text_data.tobytes())

        vertices = np.array([
        # x, y, z, u, v
        -1.0, 1.0, 0.0, 0.0, 1.0,  # Top-left
         1.0, 1.0, 0.0, 1.0, 1.0,  # Top-right
        -1.0,-1.0, 0.0, 0.0, 0.0,  # Bottom-left
         1.0,-1.0, 0.0, 1.0, 0.0   # Bottom-right
        ], dtype='f4')

        vbo = self.ctx.buffer(vertices.tobytes())

    def display_result(self):
        # Bind the default screen framebuffer
        self.ctx.screen.use()
        
        # Use the output texture from the post-processing framebuffer
        self.output_texture.use(location=0)
        
        # Render the full-screen quad to the screen
        self.quad_vao.render(mgl.TRIANGLE_STRIP)

    def render_scene(self):
        # Bind the scene framebuffer
        self.scene_framebuffer.use()
        
        # Clear the color and depth buffers
        self.ctx.clear(color=(0.08, 0.16, 0.18), depth=1.0)
        
        # Enable depth testing and face culling
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.CULL_FACE)
        
        # Perform 3D rendering (not implemented here, but use your own rendering logic)
        self.scene.render()

        #depth = np.frombuffer(self.depth_texture.read(alignment=1), dtype=np.dtype('f4')).reshape(self.WIN_SIZE[::-1])
        #print(1/depth) # should all be 1  
