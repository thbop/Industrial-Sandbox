import pygame
from pygame.math import Vector2 as vec2

from perlin_noise import PerlinNoise
import json



class Chunk:
    def __init__(self, cpos: vec2):
        '''A 16x16 chunk of tiles'''
        self.cpos = cpos # If one chunk was one pixel big, then this is the location of the chunk
        
    
    def add(self, pos, tile_id):
        self.tiles[pos[0]][pos[1]] = tile_id
    
    def generate(self, seed, density=4):
        self.tiles = [[0 for x in range(16)] for y in range(16)]
        noise = PerlinNoise(octaves=10, seed=seed)
        chunk_offset = self.cpos * 16
        for x in range(16):
            for y in range(16):
                if round(noise([(x + chunk_offset.x)/100, (y + chunk_offset.y)/100]) * density) != 0:
                    self.add((x, y), 1)
        
    
    def import_chunk(self, level_chunk):
        # Cpos is assigned during instantiation
        self.tiles = level_chunk['tiles']
    
    def export_chunk(self):
        level_chunk = {
            'cpos': list(self.cpos),
            'tiles': self.tiles,
            'actors':[]
        }
        return level_chunk
    
    
    def draw_hit(self, surf, camera):
        for x in range(16):
            for y in range(16):
                if self.tiles[x][y] != 0:
                    tile_pos = (vec2(x, y) + self.cpos * 16) * 6 - camera.get_pos()
                    pygame.draw.rect(surf, (255, 0, 0), [tile_pos.x, tile_pos.y, 6, 6], 1)


        

class Tiles:
    def __init__(self, gm):
        self.gm = gm

        file = open('levels/level.json')
        self.level = json.load(file)
        file.close()
        self.seed = 1
        
        self.chunks = []
        self.on_screen = []
    
    def view_chunks(self):
        camera_pos = self.gm.camera.get_pos()
        origin = (round(camera_pos / 96, 0) - vec2(1, 1))
        for x in range(5):
            for y in range(4):
                cpos = origin + vec2(x, y) # screen chunk position
                if cpos not in self.on_screen: # check if we're already storing it as an onscreen chunk
                    self.load(cpos) # if not lets load/generate it
                    self.on_screen.append(cpos.copy()) # and also append it to self.on_screen
        
        on_screen_remove = []
        for c in self.on_screen:
            if c.x < origin.x or c.x > origin.x + 4 or c.y < origin.y or c.y > origin.y + 3:
                on_screen_remove.append(c)
                self.unload(c)
        for c in on_screen_remove:
            self.on_screen.remove(c)
        # real_origin = origin * 96 - camera_pos
        # pygame.draw.rect(self.gm.screen, (255, 255, 0), [real_origin.x, real_origin.y, 96, 96], 1)
    
    def draw_hit(self):
        for c in self.chunks:
            c.draw_hit(self.gm.screen, self.gm.camera)
    
    
    def get_level_chunk(self, cpos):
        for c in self.level['chunks']:
            if list(cpos) == c['cpos']:
                return c
    
    def get_level_chunk_index(self, cpos):
        for i, c in enumerate(self.level['chunks'], 0):
            if list(cpos) == c['cpos']:
                return i
    
    def get_chunk(self, cpos):
        for c in self.chunks:
            if cpos == c.cpos:
                return c
            
    
    def load(self, cpos):
        level_chunk = self.get_level_chunk(cpos)
        if level_chunk != None: # If chunk exists in world, load it
            chunk = Chunk(cpos)
            chunk.import_chunk(level_chunk)
            self.chunks.append(chunk)
        else: # Else, generate a fresh chunk
            chunk = Chunk(cpos)
            chunk.generate(self.seed)
            self.chunks.append(chunk)
        return chunk
    
    def unload(self, cpos):
        chunk = self.get_chunk(cpos)
        if chunk != None: # If chunk exists, continue
            index = self.get_level_chunk_index(cpos)
            if index == None: # If chunk does not exist in the level, add it
                self.level['chunks'].append(chunk.export_chunk())
            else: # If chunk exists in the level, write to it directly
                self.level['chunks'][index] = chunk.export_chunk()
            
            self.chunks.remove(chunk)
    
    def save(self):
        file = open('levels/level.json', 'w')
        file.write(json.dumps(self.level))
        file.close()


if __name__ == '__main__':
    # chunk = Chunk(vec2(0, 0))
    # chunk.generate(1)
    tiles = Tiles(0)
    print(tiles.get_level_chunk(vec2(1, 0)))