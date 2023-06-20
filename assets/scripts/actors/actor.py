import pygame
from pygame.math import Vector2 as vec2

class Actor:
    def __init__(self, pos, size):
        self.rect = pygame.FRect(pos[0], pos[1], size[0], size[1])
        self.vel = vec2(0.0, 0.0)
    
    def get_pos(self):
        return vec2(self.rect.x, self.rect.y)