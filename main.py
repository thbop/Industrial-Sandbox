import pygame
from pygame.math import Vector2 as vec2

import moderngl
from array import array

from assets.scripts.camera import Camera
from assets.scripts.actors.player import Player
from assets.scripts.level.tiles import Tiles


class Game:
    def __init__(self):
        pygame.init()

        # General constants
        self.FPS = 60
        self.SAVE_EVERY = 30 # seconds

        self.SIZE = vec2(320, 180)
        self.WINDOW_SIZE = self.SIZE * 4
        
        # Window initialization
        self.window = pygame.display.set_mode(self.WINDOW_SIZE, pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption('Game')
        self.screen = pygame.Surface(self.SIZE)
        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0
        ]))

        self.vert_shader = open('assets/scripts/shaders/vert.glsl').read()

        self.frag_shader = open('assets/scripts/shaders/frag.glsl').read()

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])
        
        

        # Game objects
        self.camera = Camera((0, 0), self.SIZE)
        # self.cursor = Camera([0, 0], [6, 6])
        self.tiles = Tiles(self)

        self.player = Player()


        self.tick = 1
    
    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swozzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex
    
    def show_chunks(self):
        for x in range(100):
            pygame.draw.line(self.screen, (0, 255, 0), (x*96-self.camera.rect.x, -self.camera.rect.y), (x*96-self.camera.rect.x, 500-self.camera.rect.y))
        for y in range(100):
            pygame.draw.line(self.screen, (0, 255, 0), (-self.camera.rect.x, y*96-self.camera.rect.y), (500-self.camera.rect.x, y*96-self.camera.rect.y))
    

    def run(self):
        running = True
        clock = pygame.time.Clock()


        save_counter = self.SAVE_EVERY


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            self.camera.move_arrow()
            # self.cursor.move_arrow()
            
            self.screen.fill((243, 208, 243))

            self.tiles.draw()
            self.tiles.view_chunks()
            # self.show_chunks()
            
            # if self.tiles.get_tile(self.cursor.get_pos()):
            #     pygame.draw.rect(self.screen, (255, 255, 255), self.cursor.rect, 1)
            # else:
            #     pygame.draw.rect(self.screen, (0, 0, 255), self.cursor.rect, 1)

            # pygame.draw.rect(self.screen, (0, 255, 255), [0, 0, 320, 180], 1) # Camera rect
            

            
            frame_tex = self.surf_to_texture(self.screen)
            frame_tex.use(0)
            self.program['tex'] = 0
            self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

            pygame.display.flip()

            frame_tex.release()

            if self.tick < self.FPS:
                self.tick += 1
            else:
                self.tick = 1
                if save_counter > 0:
                    save_counter -= 1
                else:
                    save_counter = self.SAVE_EVERY
                    self.tiles.save()
            clock.tick(self.FPS)
            
    


if __name__ == '__main__':
    gm = Game()
    gm.run()