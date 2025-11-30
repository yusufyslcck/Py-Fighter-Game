import pygame
from settings import *
from constants import *

class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        try:
            self.image = pygame.transform.scale(
                pygame.image.load('assets/terrain/spike.png').convert_alpha(), 
                (TILE_SIZE, TILE_SIZE)
            )
        except:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            points = [
                (TILE_SIZE//2, 10),
                (10, TILE_SIZE-5),
                (TILE_SIZE-10, TILE_SIZE-5)
            ]
            pygame.draw.polygon(self.image, '#888888', points)
            pygame.draw.polygon(self.image, '#666666', points, 3)
            
        self.rect = self.image.get_rect(topleft=pos)
        self.damage = SPIKE_DAMAGE


class Saw(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        try:
            base_img = pygame.image.load('assets/terrain/saw.png').convert_alpha()
            self.original_image = pygame.transform.scale(base_img, (TILE_SIZE, TILE_SIZE))
        except:
            size = TILE_SIZE
            self.original_image = pygame.Surface((size, size), pygame.SRCALPHA)
            center = size // 2
            pygame.draw.circle(self.original_image, '#888888', (center, center), center-5)
            for i in range(8):
                angle = (360 / 8) * i
                import math
                x1 = center + int((center-10) * math.cos(math.radians(angle)))
                y1 = center + int((center-10) * math.sin(math.radians(angle)))
                x2 = center + int((center+5) * math.cos(math.radians(angle)))
                y2 = center + int((center+5) * math.sin(math.radians(angle)))
                pygame.draw.line(self.original_image, '#666666', (x1, y1), (x2, y2), 3)
            pygame.draw.circle(self.original_image, '#555555', (center, center), 8)
            
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        self.angle = 0
        self.rotation_speed = 5
        self.damage = SAW_DAMAGE
        
    def update(self):
        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center


class FallingPlatform(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        try:
            self.image = pygame.transform.scale(
                pygame.image.load('assets/terrain/falling_platform.png').convert_alpha(), 
                (TILE_SIZE * 2, TILE_SIZE // 2)
            )
        except:
            self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE // 2))
            self.image.fill('#A0522D')
            pygame.draw.line(self.image, '#654321', (20, 0), (25, TILE_SIZE//2), 2)
            pygame.draw.line(self.image, '#654321', (50, 0), (45, TILE_SIZE//2), 2)
            pygame.draw.line(self.image, '#654321', (90, 0), (95, TILE_SIZE//2), 2)
            
        self.rect = self.image.get_rect(topleft=pos)
        self.original_pos = pygame.math.Vector2(pos)
        self.falling = False
        self.fall_speed = 0
        self.shake_time = 0
        self.shake_amount = 2
        
    def trigger_fall(self):
        if not self.falling:
            self.shake_time = pygame.time.get_ticks()
            
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.shake_time > 0 and not self.falling:
            if current_time - self.shake_time < 500:
                import random
                self.rect.x = self.original_pos.x + random.randint(-self.shake_amount, self.shake_amount)
            else:
                self.falling = True
                self.shake_time = 0
        
        if self.falling:
            self.fall_speed += 0.5
            self.rect.y += self.fall_speed
            
            if self.rect.y > 1000:
                self.kill()
