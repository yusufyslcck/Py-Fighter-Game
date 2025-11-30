# player.py - Oyuncu karakteri

import pygame
from settings import *
from constants import *
import os
from particles import create_jump_particles, create_hit_particles

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites, particle_group=None):
        super().__init__(groups)
        self.particle_group = particle_group
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = ANIMATION_SPEED
        self.status = 'idle'
        self.previous_status = 'idle'
        self.facing_right = True
        self.image = self.animations['idle'][0] if self.animations['idle'] else pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.attack_animation_finished = True
        self.hit_animation_finished = True
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION
        self.air_resistance = PLAYER_AIR_RESISTANCE
        self.gravity = PLAYER_GRAVITY
        self.jump_speed = PLAYER_JUMP_SPEED
        self.max_fall_speed = PLAYER_MAX_FALL_SPEED
        self.collision_sprites = collision_sprites 
        self.on_ground = False
        self.jump_count = 0
        self.max_jumps = 2
        self.on_platform = None
        self.coyote_time = COYOTE_TIME
        self.time_since_grounded = 0
        self.jump_buffer_time = JUMP_BUFFER_TIME
        self.jump_buffer = 0 
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.is_attacking = False
        self.attack_cooldown = ATTACK_DURATION
        self.attack_time = 0
        self.is_hit = False
        self.hit_time = 0

    def import_character_assets(self):
        character_path = 'assets/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'hit': []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = []
            try:
                for _,__,img_files in os.walk(full_path):
                    for file in sorted(img_files):
                        if file.endswith('.png'):
                            path = full_path + '/' + file
                            img = pygame.image.load(path).convert_alpha()
                            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                            self.animations[animation].append(img)
            except: pass
        
        if not self.animations['jump'] and self.animations['idle']:
            self.animations['jump'] = [self.animations['idle'][0]]
        if not self.animations['fall'] and self.animations['idle']:
            self.animations['fall'] = [self.animations['idle'][0]]
        if not self.animations['attack'] and self.animations['idle']:
            self.animations['attack'] = [self.animations['idle'][0]]
        if not self.animations['hit'] and self.animations['idle']:
            self.animations['hit'] = [self.animations['idle'][0]]

    def get_damage(self, damage_amount=1):
        if not self.is_hit:
            if self.particle_group:
                create_hit_particles(self.rect.center, self.particle_group)
                
            self.is_hit = True
            self.hit_time = pygame.time.get_ticks()
            self.health -= 1
            self.hit_animation_finished = False
            self.frame_index = 0
            if hasattr(self, 'last_hit_direction'):
                self.direction.x = -self.last_hit_direction * PLAYER_KNOCKBACK_FORCE
                self.direction.y = -8 

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x += self.acceleration
            self.facing_right = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x -= self.acceleration
            self.facing_right = False
        else:
            friction = self.friction if self.on_ground else self.air_resistance
            self.direction.x *= friction
            if abs(self.direction.x) < 0.1:
                self.direction.x = 0

        self.direction.x = max(-self.speed, min(self.speed, self.direction.x))

        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump_buffer = self.jump_buffer_time
            if not hasattr(self, 'jump_pressed'):
                self.jump_pressed = False
            if not self.jump_pressed and self.jump_count < self.max_jumps:
                if self.on_ground or self.time_since_grounded < self.coyote_time:
                    self.jump()
                    self.jump_pressed = True
                elif self.jump_count == 1 and self.jump_count < self.max_jumps:
                    self.jump()
                    self.jump_pressed = True
        else:
            self.jump_pressed = False

        if keys[pygame.K_f] and not self.is_attacking:
            self.attack()

    def attack(self):
        self.is_attacking = True
        self.attack_time = pygame.time.get_ticks()
        self.attack_animation_finished = False
        self.frame_index = 0

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.is_attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.is_attacking = False
        
        if self.is_hit:
            if current_time - self.hit_time >= HIT_COOLDOWN: 
                self.is_hit = False

    def animate(self):
        animation = self.animations[self.status]
        
        if not animation:
            return
        
        if self.status != self.previous_status:
            self.frame_index = 0
            self.previous_status = self.status
        
        if self.status == 'attack':
            speed = 0.25
        elif self.status == 'hit':
            speed = 0.2
        elif self.status in ['jump', 'fall']:
            speed = 0.1
        else:
            speed = self.animation_speed
        
        self.frame_index += speed
        
        if self.status in ['attack', 'hit']:
            if self.frame_index >= len(animation):
                if self.status == 'attack':
                    self.attack_animation_finished = True
                if self.status == 'hit':
                    self.hit_animation_finished = True
                self.frame_index = len(animation) - 1
        else:
            if self.frame_index >= len(animation): 
                self.frame_index = 0

        image = animation[int(self.frame_index)]
        
        if self.facing_right: 
            self.image = image
        else: 
            self.image = pygame.transform.flip(image, True, False)

        if self.is_hit:
            current_time = pygame.time.get_ticks()
            if (current_time - self.hit_time) < 400:
                if (current_time // 80) % 2 == 0:
                    red_surf = self.image.copy()
                    red_surf.fill((255, 50, 50), special_flags=pygame.BLEND_RGB_ADD)
                    self.image = red_surf

    def get_status(self):
        if self.is_hit and not self.hit_animation_finished:
            self.status = 'hit'
            return
        
        if self.is_attacking and not self.attack_animation_finished:
            self.status = 'attack'
            return
        
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def apply_gravity(self):
        if self.direction.y < 0 and not (pygame.key.get_pressed()[pygame.K_SPACE] or 
                                          pygame.key.get_pressed()[pygame.K_UP] or 
                                          pygame.key.get_pressed()[pygame.K_w]):
            self.direction.y += self.gravity * 2
        else:
            self.direction.y += self.gravity
            
        if self.direction.y > self.max_fall_speed:
            self.direction.y = self.max_fall_speed
        self.rect.y += self.direction.y

    def jump(self):
        if self.particle_group:
            create_jump_particles((self.rect.centerx, self.rect.bottom), self.particle_group)
        
        self.direction.y = self.jump_speed
        self.jump_count += 1
        self.on_ground = False
        self.time_since_grounded = 999

    def move(self):
        self.rect.x += self.direction.x
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0: 
                    self.rect.right = sprite.rect.left
                    self.direction.x = 0
                elif self.direction.x < 0: 
                    self.rect.left = sprite.rect.right
                    self.direction.x = 0
        
        self.apply_gravity()
        was_on_ground = self.on_ground
        
        if not hasattr(self, 'on_platform') or self.on_platform is None:
            self.on_ground = False
        
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'movement_type'):
                continue
                
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                    self.jump_count = 0
                    self.time_since_grounded = 0
                elif self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0
        
        if was_on_ground and not self.on_ground:
            self.time_since_grounded = 0
        elif not self.on_ground:
            self.time_since_grounded += 1/60
        
        if self.jump_buffer > 0:
            self.jump_buffer -= 1/60
    
    def check_fall(self):
        if self.rect.y > 1000:
            self.health = 0

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move()
        self.check_fall()