import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx) :
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img.png')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/SkyboxStars/', ext='png')
        self.textures['skyboxarea'] = self.get_texture_cube(dir_path='textures/SkyboxStarsArea/', ext='png')

    def get_texture_cube(self, dir_path,ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['front', 'back','right', 'left']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size,components=3,data=None)

        for i in range(6):
            textures_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=textures_data)
            # print("Loading texture : " + i)
        
        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size = texture.get_size(), components = 3, data=pg.image.tostring(texture,'RGB'))

        #mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        #AF
        texture.anisotropy = 32.0

        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]