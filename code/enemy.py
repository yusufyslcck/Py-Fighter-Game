# enemy.py - Düşman karakterleri ve mermiler

import pygame
from settings import *
from constants import *
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, groups, speed=PROJECTILE_SPEED):
        super().__init__(groups)
        self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image.fill(COLOR_PROJECTILE_RED)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.speed = speed
        self.lifetime = PROJECTILE_LIFETIME

    def update(self):
        self.rect.x += self.direction * self.speed
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, enemy_type='normal', level_index=1, obstacle_sprites=None):
        super().__init__(groups)
        
        self.obstacle_sprites = obstacle_sprites
        self.enemy_type = enemy_type
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = ENEMY_ANIMATION_SPEED
        
        if self.animations:
            self.image = self.animations[0]
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill('red')

        self.rect = self.image.get_rect(topleft=pos)
        # Float position for smooth movement and precise collision handling
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(1, 0)
        
        self.start_x = pos[0]
        self.patrol_distance = ENEMY_PATROL_DISTANCE
        self.left_boundary = self.start_x - self.patrol_distance
        self.right_boundary = self.start_x + self.patrol_distance
        
        if self.enemy_type == 'normal':
            self.speed = ENEMY_NORMAL_SPEED
            self.health = ENEMY_NORMAL_HEALTH
            self.max_health = ENEMY_NORMAL_HEALTH
            self.damage = ENEMY_NORMAL_DAMAGE
            self.can_fly = False
            self.can_shoot = False
        elif self.enemy_type == 'strong':
            self.speed = ENEMY_STRONG_SPEED
            self.health = ENEMY_STRONG_HEALTH
            self.max_health = ENEMY_STRONG_HEALTH
            self.damage = ENEMY_STRONG_DAMAGE
            self.can_fly = False
            self.can_shoot = False
        elif self.enemy_type == 'flying':
            self.speed = ENEMY_FLYING_SPEED
            self.health = ENEMY_FLYING_HEALTH
            self.max_health = ENEMY_FLYING_HEALTH
            self.damage = ENEMY_FLYING_DAMAGE
            self.can_fly = True
            self.can_shoot = False
            self.vertical_speed = ENEMY_FLYING_VERTICAL_SPEED
            self.vertical_direction = 1
            self.start_y = pos[1]
            self.vertical_distance = ENEMY_FLYING_VERTICAL_DISTANCE
        elif self.enemy_type == 'shooter':
            self.speed = ENEMY_SHOOTER_SPEED
            self.health = ENEMY_SHOOTER_HEALTH
            self.max_health = ENEMY_SHOOTER_HEALTH
            self.damage = ENEMY_SHOOTER_DAMAGE
            self.can_fly = False
            self.can_shoot = True
            self.shoot_cooldown = 0
            self.shoot_interval = ENEMY_SHOOT_INTERVAL
            self.projectiles = []

        # Apply level-based scaling to gradually increase difficulty
        try:
            lvl = int(level_index)
        except:
            lvl = 1

        # Use centralized scale function from settings if available
        try:
            scale = get_level_scale(lvl)
        except Exception:
            # fallback to safe defaults
            if lvl <= 5:
                scale = 1.0
            elif lvl <= 10:
                scale = 1.12
            else:
                scale = 1.25

        self.scale = scale

        # Scale movement, patrol distance and vertical movement
        self.speed = getattr(self, 'speed', 0) * scale
        self.patrol_distance = int(self.patrol_distance * scale)
        self.left_boundary = self.start_x - self.patrol_distance
        self.right_boundary = self.start_x + self.patrol_distance

        if hasattr(self, 'vertical_speed'):
            self.vertical_speed = self.vertical_speed * scale
            self.vertical_distance = int(self.vertical_distance * scale)

        # Shooter fires slightly faster on higher levels
        if hasattr(self, 'shoot_interval'):
            self.shoot_interval = max(20, int(self.shoot_interval / scale))

        self.hit_time = 0
        self.is_hit = False

    def import_assets(self):
        self.animations = []
        
        if self.enemy_type == 'normal':
            enemy_path = 'assets/enemy/run/'
            try:
                for _,__,img_files in os.walk(enemy_path):
                    for file in sorted(img_files):
                        if file.endswith('.png') and 'strong' not in file:
                            full_path = enemy_path + file
                            img = pygame.image.load(full_path).convert_alpha()
                            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                            self.animations.append(img)
            except: pass
        elif self.enemy_type == 'strong':
            try:
                img = pygame.image.load('assets/enemy/run/strong.png').convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.animations.append(img)
            except: pass
        elif self.enemy_type == 'flying':
            try:
                img = pygame.image.load('assets/enemy/run/0.png').convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.animations.append(img)
            except:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(COLOR_PURPLE)
                self.animations.append(surf)
        elif self.enemy_type == 'shooter':
            try:
                img = pygame.image.load('assets/enemy/run/0.png').convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.animations.append(img)
            except:
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                surf.fill(COLOR_ORANGE_RED)
                self.animations.append(surf)

    def get_damage(self):
        self.is_hit = True
        self.hit_time = pygame.time.get_ticks()

    def animate(self):
        if not self.animations: return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        base_image = self.animations[int(self.frame_index)]
        
        if self.direction.x > 0:
            self.image = pygame.transform.flip(base_image, True, False)
        else:
            self.image = base_image

        if self.is_hit:
            current_time = pygame.time.get_ticks()
            hit_duration = current_time - self.hit_time
            
            if hit_duration < ENEMY_HIT_EFFECT_DURATION:
                if (current_time // 50) % 2 == 0:
                    red_surf = self.image.copy()
                    red_surf.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_ADD)
                    self.image = red_surf
                else:
                    white_surf = self.image.copy()
                    white_surf.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_ADD)
                    self.image = white_surf
            else:
                self.is_hit = False

    def move(self):
        # Ensure obstacle_sprites is a Group (avoid None)
        if not hasattr(self, 'obstacle_sprites') or self.obstacle_sprites is None:
            self.obstacle_sprites = pygame.sprite.Group()

        # Horizontal movement (use float pos to avoid tunneling rounding issues)
        self.pos.x += self.direction.x * self.speed
        self.rect.x = int(self.pos.x)

        # Horizontal collisions
        if self.obstacle_sprites:
            collided = pygame.sprite.spritecollide(self, self.obstacle_sprites, False)
            for obstacle in collided:
                if self.direction.x > 0:
                    self.rect.right = obstacle.rect.left
                    self.pos.x = self.rect.x
                elif self.direction.x < 0:
                    self.rect.left = obstacle.rect.right
                    self.pos.x = self.rect.x
                self.reverse()

        # Patrol boundary checks
        if self.rect.x <= self.left_boundary:
            self.rect.x = self.left_boundary
            self.pos.x = self.rect.x
            self.direction.x = 1
        elif self.rect.x >= self.right_boundary:
            self.rect.x = self.right_boundary
            self.pos.x = self.rect.x
            self.direction.x = -1

        # Vertical movement for flying enemies with collision
        if self.can_fly:
            self.pos.y += self.vertical_direction * self.vertical_speed
            self.rect.y = int(self.pos.y)

            if self.obstacle_sprites:
                collided_v = pygame.sprite.spritecollide(self, self.obstacle_sprites, False)
                for obstacle in collided_v:
                    if self.vertical_direction > 0:
                        # moving down
                        self.rect.bottom = obstacle.rect.top
                        self.pos.y = self.rect.y
                        self.vertical_direction = -1
                    elif self.vertical_direction < 0:
                        # moving up
                        self.rect.top = obstacle.rect.bottom
                        self.pos.y = self.rect.y
                        self.vertical_direction = 1

            if self.rect.y <= self.start_y - self.vertical_distance:
                self.rect.y = self.start_y - self.vertical_distance
                self.pos.y = self.rect.y
                self.vertical_direction = 1
            elif self.rect.y >= self.start_y + self.vertical_distance:
                self.rect.y = self.start_y + self.vertical_distance
                self.pos.y = self.rect.y
                self.vertical_direction = -1

    def reverse(self):
        self.direction.x *= -1

    def shoot(self, projectile_group):
        if self.can_shoot:
            self.shoot_cooldown += 1
            if self.shoot_cooldown >= self.shoot_interval:
                self.shoot_cooldown = 0
                direction = 1 if self.direction.x > 0 else -1
                proj_speed = int(PROJECTILE_SPEED * getattr(self, 'scale', 1.0))
                Projectile(self.rect.center, direction, [projectile_group], speed=proj_speed)
    
    def update(self):
        self.animate()
        self.move()