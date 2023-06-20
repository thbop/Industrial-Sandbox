import pygame
from .actors.actor import Actor

class Camera(Actor):
    def __init__(self, pos, size):
        super().__init__(pos, size)

    def move_arrow(self, speed=1):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]: self.rect.x += speed
        elif keys[pygame.K_LEFT]: self.rect.x -= speed
        if keys[pygame.K_DOWN]: self.rect.y += speed
        elif keys[pygame.K_UP]: self.rect.y -= speed