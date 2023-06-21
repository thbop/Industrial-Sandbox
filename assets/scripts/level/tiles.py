import pygame
from pygame.math import Vector2 as vec2

from perlin_noise import PerlinNoise
import json

from ..spritesheet import spritesheet

def load_tile_row(y, s=6):
    row = {
        '[False, False, False, False]':tss.image_at([ 0, y, s, s ]),
        '[False, False, True, True]':  tss.image_at([ s, y, s, s ]),
        '[True, False, False, True]':  tss.image_at([ s*2, y, s, s ]),
        '[False, True, True, False]':  tss.image_at([ s*3, y, s, s ]),
        '[True, True, False, False]':  tss.image_at([ s*4, y, s, s ]),
        '[False, True, True, True]':   tss.image_at([ s*5, y, s, s ]),
        '[True, False, True, True]':   tss.image_at([ s*6, y, s, s ]),
        '[True, True, False, True]':   tss.image_at([ s*7, y, s, s ]),
        '[True, True, True, False]':   tss.image_at([ s*8, y, s, s ]),
        '[True, False, False, False]': tss.image_at([ s*9, y, s, s ]),
        '[False, True, False, False]': tss.image_at([ s*10, y, s, s ]),
        '[False, False, True, False]': tss.image_at([ s*11, y, s, s ]),
        '[False, False, False, True]': tss.image_at([ s*12, y, s, s ]),
        '[True, False, True, False]':  tss.image_at([ s*13, y, s, s ]),
        '[False, True, False, True]':  tss.image_at([ s*14, y, s, s ]),
        '[True, True, True, True]':    tss.image_at([ s*15, y, s, s ]),
        'bg':                          tss.image_at([ s*16, y, s, s ])
    }
    return row


tss = spritesheet('assets/graphics/tiles.png')
tdefs = [
    0, 
    load_tile_row(0)
]


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
    
    def draw(self):
        for c in self.chunks:
            for x in range(16):
                for y in range(16):
                    if c.tiles[x][y] != 0:
                        tile_pos = (vec2(x, y) + c.cpos * 16) * 6 - self.gm.camera.get_pos()
                        tile_row = tdefs[c.tiles[x][y]]
                        try:
                            other_tiles = [
                                bool(c.tiles[x-1][y]),
                                bool(c.tiles[x][y-1]),
                                bool(c.tiles[x+1][y]),
                                bool(c.tiles[x][y+1]),
                            ]
                        except IndexError:
                            ntpos = vec2(x, y) + c.cpos * 16
                            other_tiles = [
                                bool(self.get_tile(vec2(ntpos.x-1, ntpos.y))),
                                bool(self.get_tile(vec2(ntpos.x, ntpos.y-1))),
                                bool(self.get_tile(vec2(ntpos.x+1, ntpos.y))),
                                bool(self.get_tile(vec2(ntpos.x, ntpos.y+1))),
                            ]

                            
                        self.gm.screen.blit(tile_row[str(other_tiles)], tile_pos)
    

    def get_tile(self, tpos): # True position / 6
        cpos = tpos / 16
        if cpos.x > round(cpos.x)-1 and cpos.x < round(cpos.x):
            cpos.x = round(cpos.x)-1
        else:
            cpos.x = round(cpos.x)
        if cpos.y > round(cpos.y)-1 and cpos.y < round(cpos.y):
            cpos.y = round(cpos.y)-1
        else:
            cpos.y = round(cpos.y)

        x = round(tpos.x % 16)
        y = round(tpos.y % 16)

        if x > 15:
            x = 0
        if y > 15:
            y = 0
                
        # pygame.draw.rect(self.gm.screen, (255, 0, 255), [cpos.x*96, cpos.y*96, 96, 96], 1)

        chunk = self.get_chunk(cpos)
        try:
            return chunk.tiles[x][y]
        except AttributeError:
            return 0
    
    
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
    
    def unload(self, cpos, remove=True):
        chunk = self.get_chunk(cpos)
        if chunk != None: # If chunk exists, continue
            index = self.get_level_chunk_index(cpos)
            if index == None: # If chunk does not exist in the level, add it
                self.level['chunks'].append(chunk.export_chunk())
            else: # If chunk exists in the level, write to it directly
                self.level['chunks'][index] = chunk.export_chunk()
            if remove:
                self.chunks.remove(chunk)
    
    def save(self):
        for c in self.on_screen:
            self.unload(c, remove=False)

        file = open('levels/level.json', 'w')
        file.write(json.dumps(self.level))
        file.close()


if __name__ == '__main__':
    # chunk = Chunk(vec2(0, 0))
    # chunk.generate(1)
    tiles = Tiles(0)
    print(tiles.get_level_chunk(vec2(1, 0)))