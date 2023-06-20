import pygame
from pygame.math import Vector2 as vec2

from assets.scripts.camera import Camera
from assets.scripts.actors.player import Player
from assets.scripts.level.tiles import Tiles


class Game:
    def __init__(self):
        pygame.init()

        # General constants
        self.FPS = 60

        self.SIZE = vec2(320, 180)
        self.WINDOW_SIZE = self.SIZE * 4
        
        # Window initialization
        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('Game')
        self.screen = pygame.Surface(self.SIZE)

        # Game objects
        self.camera = Camera((0, 0), self.SIZE)
        self.tiles = Tiles(self)

        self.player = Player()
    
    def show_chunks(self):
        for x in range(100):
            pygame.draw.line(self.screen, (0, 255, 0), (x*96-self.camera.rect.x, -self.camera.rect.y), (x*96-self.camera.rect.x, 500-self.camera.rect.y))
        for y in range(100):
            pygame.draw.line(self.screen, (0, 255, 0), (-self.camera.rect.x, y*96-self.camera.rect.y), (500-self.camera.rect.x, y*96-self.camera.rect.y))
    

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.camera.move_arrow()
            
            self.screen.fill((0, 0, 0))

            self.tiles.draw_hit()
            self.tiles.view_chunks()
            self.show_chunks()

            # pygame.draw.rect(self.screen, (0, 255, 255), [0, 0, 320, 180], 1) # Camera rect

            clock.tick(self.FPS)
            pygame.transform.scale(self.screen, self.WINDOW_SIZE, self.window)
            pygame.display.flip()


if __name__ == '__main__':
    gm = Game()
    gm.run()