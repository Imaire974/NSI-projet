import numpy as np
import glm
import pygame as pg
import moderngl as mgl

class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0,0,0), rot=(0,0,0), scale=(1,1,1)):
        self.app = app
        self.pos= pos
        self.scale = scale
        self.rot =glm.vec3([glm.radians(a) for a in rot])
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        #translate
        m_model = glm.translate(m_model, self.pos)
        #rotations
        m_model = glm.rotate(m_model,self.rot.x,glm.vec3(1,0,0))
        m_model = glm.rotate(m_model,self.rot.y,glm.vec3(0,1,0))
        m_model = glm.rotate(m_model,self.rot.z,glm.vec3(0,0,1))
        #scale
        m_model = glm.scale(m_model, self.scale)
                             
        return m_model
    
    def render(self): 
        self.update()
        self.vao.render()

class ExtendedBaseModel(BaseModel):

    def __init__(self, app, vao_name, tex_id, pos,rot,scale):
        super().__init__(app, vao_name, tex_id,pos,rot,scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)
    
    def on_init(self):
        #texture 
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use()

        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['dirLight.direction'].write(self.app.light.dirLightDirection)
        self.program['dirLight.color'].write(self.app.light.dirLightColot)
        self.program['dirLight.ambient'].write(self.app.light.Id)
        self.program['dirLight.diffuse'].write(self.app.light.Id)
        self.program['dirLight.specular'].write(self.app.light.Is)
        
        '''
        for i in range(9):
            self.program['lights[{}].position'.format(str(i))].write(glm.vec3(i*3,4,i*-3))
            self.program['lights[{}].Id'.format(str(i))].write(glm.vec3(0.8,0.8,0.8))
            self.program['lights[{}].Is'.format(str(i))].write(glm.vec3(0.7,0.7,0.7))'''        

class Cube(ExtendedBaseModel):

    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0,0,0),rot=(0,0,0),scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id,pos,rot,scale)

class Cat(ExtendedBaseModel):

    def __init__(self, app, vao_name='cat', tex_id='cat', pos=(0,0,0),rot=(-90,0,0),scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id,pos,rot,scale)
    
class SkyBox(BaseModel):

    def __init__(self, app, vao_name='skybox', tex_id='skybox',rot=(45,0,0),scale=(1,1,1)):
        super().__init__(app, vao_name, tex_id,rot,scale)
        self.on_init()

    def changeTex(self, tex_id):
        self.tex_id = tex_id
        self.texture = self.app.mesh.texture.textures[tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

    def update(self):     

        self.rot.y +=  glm.radians(self.app.deltaTime * 0.001 * 1)

        preRotated = self.camera.m_view

        preRotated = glm.rotate(preRotated,self.rot.x,glm.vec3(1,0,0))
        preRotated = glm.rotate(preRotated,self.rot.y,glm.vec3(0,1,0))
        preRotated = glm.rotate(preRotated,self.rot.z,glm.vec3(0,0,1))

        m_view = glm.mat4(glm.mat3(preRotated))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))
        # self.program['m_invProjViewWorld'].write(glm.inverse(self.camera.m_proj * self.camera.m_view))

    def on_init(self):
        # texture
        # self.program['lightDir'].write(self.app.light.dirLightDirection)
        self.rot =glm.vec3([glm.radians(a) for a in (45,0,0)])
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

        
        
        