# particles.py - Parçacık efektleri

import pygame
import random
from constants import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, velocity, groups, lifetime=30):
        super().__init__(groups)
        self.lifetime = lifetime
        self.age = 0
        size = random.randint(3, 6)
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.math.Vector2(velocity)
        self.gravity = PARTICLE_GRAVITY
    
    def update(self):
        self.velocity.y += self.gravity
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        self.age += 1
        alpha = 255 * (1 - self.age / self.lifetime)
        self.image.set_alpha(alpha)
        if self.age >= self.lifetime:
            self.kill()

def create_jump_particles(pos, particle_group):
    for _ in range(PARTICLE_JUMP_COUNT):
        vel = (random.uniform(-2, 2), random.uniform(-3, -1))
        Particle(pos, COLOR_DUST_BROWN, vel, [particle_group], lifetime=20)

def create_coin_particles(pos, particle_group):
    for _ in range(PARTICLE_COIN_COUNT):
        vel = (random.uniform(-3, 3), random.uniform(-4, -1))
        Particle(pos, COLOR_GOLD, vel, [particle_group], lifetime=25)

def create_hit_particles(pos, particle_group):
    for _ in range(PARTICLE_HIT_COUNT):
        vel = (random.uniform(-4, 4), random.uniform(-5, -2))
        Particle(pos, COLOR_RED, vel, [particle_group], lifetime=20)

def create_enemy_death_particles(pos, particle_group, enemy_type='normal'):
    color = '#4a90e2' if enemy_type == 'normal' else COLOR_ORANGE_RED
    for _ in range(PARTICLE_ENEMY_DEATH_COUNT):
        vel = (random.uniform(-5, 5), random.uniform(-6, -2))
        Particle(pos, color, vel, [particle_group], lifetime=PARTICLE_DEFAULT_LIFETIME)
