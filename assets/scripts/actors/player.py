import pygame
from pygame.math import Vector2 as vec2

from .actor import Actor

class Player(Actor):
    def __init__(self):
        super().__init__((100, 100), (6, 6))
