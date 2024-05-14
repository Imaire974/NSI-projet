# Librairies : pip install pygame moderngl numpy PyGLM pywavefront Pillow
import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene
from renderer import Renderer
from OpenGL.GL import glViewport

class MoteurGraphique:

    def __init__(self, winSize=(1600,900)):
        #(320,180)
        pg.init()
        self.WIN_SIZE = winSize

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        self.display_flags = (pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE )

        self.screen = pg.display.set_mode(self.WIN_SIZE, self.display_flags)
        glViewport(0, 0, *self.WIN_SIZE)

        pg.display.set_icon(pg.image.load('Assets/icon.jpg'))
        pg.display.set_caption('White Nights')

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.ctx.viewport = (0, 0, *self.WIN_SIZE)

        self.debugFont = pg.font.Font('Assets/font.ttf', 32)
        self.isDebugMode = False
        self.maxFps = 60

        self.clock = pg.time.Clock()
        self.time = 0
        self.deltaTime = 0

        self.light = Light(intensite=0.5)

        self.camera = Camera(self)

        self.mesh = Mesh(self)

        self.scene = Scene(self)

        self.renderer = Renderer(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key ==  pg.K_ESCAPE) :
                self.mesh.destroy()
                pg.quit()
                sys.exit()
            if (event.type == pg.KEYDOWN and event.key ==  pg.K_F9):
                if not self.isDebugMode:
                    self.scene.skybox.changeTex("skyboxarea")
                    self.isDebugMode = True
                else:
                    self.scene.skybox.changeTex("skybox")
                    self.isDebugMode = False
                

    def render(self):

        self.renderer.render()
        pg.display.flip()

        # if self.isDebugMode:

            # self.screen.fill((255,255,255))

            # text  = self.debugFont.render('hello', True, (255, 255, 255),(0, 0, 0))

            # textRect = text.get_rect()
            # textRect.center = (200, 200)

            # self.screen.blit(text, textRect)

            # pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.deltaTime = self.clock.tick(self.maxFps)

if __name__ == "__main__":
    app = MoteurGraphique()
    app.run()