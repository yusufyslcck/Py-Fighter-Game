import pygame, sys
from settings import *
from constants import *
from player import Player
from enemy import Enemy
from hazards import Spike, Saw, FallingPlatform
from particles import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        try: self.image = pygame.transform.scale(pygame.image.load('assets/terrain/wall.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
        except: self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)); self.image.fill('brown')
        self.rect = self.image.get_rect(topleft=pos)

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        try: self.image = pygame.transform.scale(pygame.image.load('assets/objects/coin.png').convert_alpha(), (48, 48))
        except: self.image = pygame.Surface((40, 40)); self.image.fill('yellow')
        self.rect = self.image.get_rect(center = (pos[0]+32, pos[1]+32))

class Key(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        try: self.image = pygame.transform.scale(pygame.image.load('assets/objects/key.png').convert_alpha(), (48, 48))
        except: self.image = pygame.Surface((48, 48)); self.image.fill('gold')
        self.rect = self.image.get_rect(center = (pos[0]+32, pos[1]+32))

class DoorPart(pygame.sprite.Sprite):
    def __init__(self, pos, groups, part_type):
        super().__init__(groups)
        part_names = {
            '1': 'door-tl.png',
            '2': 'door-tr.png', 
            '3': 'door-bl.png',
            '4': 'door-br.png'
        }
        
        img_path = f'assets/terrain/{part_names.get(part_type, "door-tl.png")}'
        
        try:
            img = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"ERROR: Door part not found! Path: {img_path}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill('purple')
            
        self.rect = self.image.get_rect(topleft=pos)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_active = True 
        self.paused = False  # Pause durumu
        self.current_level_index = 1
        self.has_key = False
        self.return_to_menu = False
        self.all_levels_completed = False
        
        self.level_start_time = pygame.time.get_ticks()
        self.show_level_banner = True
        self.banner_duration = 2000
        self.floating_texts = []
        self.score_pop_time = 0
        self.heart_shake_time = 0

        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.coin_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.key_sprites = pygame.sprite.Group()
        self.door_sprites = pygame.sprite.Group()
        self.moving_platforms = pygame.sprite.Group()
        self.hazard_sprites = pygame.sprite.Group()  # Tuzaklar
        self.falling_platforms = pygame.sprite.Group()  # Düşen platformlar
        self.particle_group = pygame.sprite.Group()  # Parçacık efektleri
        self.projectile_group = pygame.sprite.Group()  # Düşman mermileri

        # UI ve Fontlar
        self.score = 0
        self.font = pygame.font.Font(None, 40)
        self.game_over_font = pygame.font.Font(None, 80)
        self.score_font = pygame.font.Font(None, 60)
        
        # Resim Yüklemeleri (Güvenli)
        try:
            self.heart_full = pygame.transform.scale(pygame.image.load('assets/ui/heart_full.png').convert_alpha(), (48, 48))
            self.heart_half = pygame.transform.scale(pygame.image.load('assets/ui/heart_half.png').convert_alpha(), (48, 48))
            self.heart_empty = pygame.transform.scale(pygame.image.load('assets/ui/heart_empty.png').convert_alpha(), (48, 48))
        except:
            self.heart_full = pygame.Surface((48, 48)); self.heart_full.fill('red')
            self.heart_half = pygame.Surface((48, 48)); self.heart_half.fill('orange')
            self.heart_empty = pygame.Surface((48, 48)); self.heart_empty.fill('gray')

        # Game Over Karakter Resmi
        try:
            player_img = pygame.image.load('assets/player/idle/0.png').convert_alpha()
            self.game_over_player = pygame.transform.scale(player_img, (150, 150))
        except:
            self.game_over_player = pygame.Surface((150,150)); self.game_over_player.fill('red')

        self.create_map()

    def create_map(self):
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.coin_sprites.empty()
        self.enemy_sprites.empty()
        self.key_sprites.empty()
        self.door_sprites.empty()
        self.moving_platforms.empty()
        self.hazard_sprites.empty()
        self.falling_platforms.empty()
        self.has_key = False

        current_map = LEVELS[self.current_level_index - 1]

        for row_index, row in enumerate(current_map):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                
                if col == 'X': Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'A': Coin((x, y), [self.visible_sprites, self.coin_sprites])
                if col == 'P': self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.particle_group)
                if col == 'E': Enemy((x, y), [self.visible_sprites, self.enemy_sprites], 'normal', self.current_level_index, self.obstacle_sprites)
                if col == 'S': Enemy((x, y), [self.visible_sprites, self.enemy_sprites], 'strong', self.current_level_index, self.obstacle_sprites)
                if col == 'B': Enemy((x, y), [self.visible_sprites, self.enemy_sprites], 'flying', self.current_level_index, self.obstacle_sprites)
                if col == 'G': Enemy((x, y), [self.visible_sprites, self.enemy_sprites], 'shooter', self.current_level_index, self.obstacle_sprites)
                if col == 'K': Key((x, y), [self.visible_sprites, self.key_sprites])
                if col in ['1', '2', '3', '4']: DoorPart((x, y), [self.visible_sprites, self.door_sprites], col)
                if col == 'T': Spike((x, y), [self.visible_sprites, self.hazard_sprites])
                # 'L' (Lava) tile kaldırıldı — haritalarda kullanılmıyor
                if col == 'W': Saw((x, y), [self.visible_sprites, self.hazard_sprites])
                if col == 'Y': FallingPlatform((x, y), [self.visible_sprites, self.falling_platforms, self.obstacle_sprites])

    def reset_game(self):
        self.score = 0
        self.current_level_index = 1
        self.has_key = False
        self.all_levels_completed = False
        self.game_active = True
        self.create_map()

    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index > len(LEVELS):
            self.all_levels_completed = True
            return
        self.has_key = False
        self.level_start_time = pygame.time.get_ticks()
        self.show_level_banner = True
        self.create_map()

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.obstacle_sprites, False):
                enemy.reverse()
            
            for obstacle in self.obstacle_sprites:
                if enemy.rect.colliderect(obstacle.rect):
                    if enemy.direction.x > 0:
                        enemy.rect.right = obstacle.rect.left
                    elif enemy.direction.x < 0:
                        enemy.rect.left = obstacle.rect.right
                    enemy.reverse()

    def combat_logic(self):
        if self.player.is_attacking:
            for enemy in self.enemy_sprites.sprites():
                if self.player.rect.colliderect(enemy.rect):
                    enemy.get_damage()
                    enemy.health -= 10 
                    knockback = 25
                    if self.player.rect.centerx < enemy.rect.centerx: 
                        enemy.rect.x += knockback
                    else: 
                        enemy.rect.x -= knockback
                    if enemy.health <= 0:
                        create_enemy_death_particles(enemy.rect.center, self.particle_group, enemy.enemy_type)
                        enemy.kill()
                        self.score += 200
                        if enemy.enemy_type == 'strong': self.score += 300

        hits = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False)
        if hits and not self.player.is_attacking and not self.player.is_hit:
            hit_enemy = hits[0]
            if self.player.rect.centerx < hit_enemy.rect.centerx:
                self.player.last_hit_direction = 1
            else:
                self.player.last_hit_direction = -1
            self.player.get_damage()
            self.heart_shake_time = pygame.time.get_ticks()

    def check_level_complete(self):
        if pygame.sprite.spritecollide(self.player, self.key_sprites, True): 
            self.has_key = True
        if pygame.sprite.spritecollide(self.player, self.door_sprites, False):
            if self.has_key and len(self.enemy_sprites) == 0: 
                self.next_level()

    def hazard_collision(self):
        hits = pygame.sprite.spritecollide(self.player, self.hazard_sprites, False)
        if hits and not self.player.is_hit:
            hazard = hits[0]
            if hasattr(hazard, 'instant_kill') and hazard.instant_kill:
                self.player.health = 0
            else:
                self.player.get_damage(hazard.damage)
                self.heart_shake_time = pygame.time.get_ticks()
                if self.player.rect.centerx < hazard.rect.centerx:
                    self.player.last_hit_direction = 1
                else:
                    self.player.last_hit_direction = -1
    
    def projectile_collision(self):
        for projectile in self.projectile_group:
            if projectile.rect.colliderect(self.player.rect):
                self.player.get_damage(PROJECTILE_DAMAGE)
                projectile.kill()
                self.heart_shake_time = pygame.time.get_ticks()
            
            for obstacle in self.obstacle_sprites:
                if projectile.rect.colliderect(obstacle.rect):
                    projectile.kill()
                    break
    
    def falling_platform_check(self):
        for platform in self.falling_platforms:
            if platform.rect.colliderect(self.player.rect):
                overlap = self.player.rect.bottom - platform.rect.top
                if 0 < overlap < 20 and self.player.direction.y >= 0:
                    platform.trigger_fall()

    def check_death(self):
        if self.player.health <= 0:
            self.player.health = 0
            self.game_active = False

    def display_ui(self):
        current_time = pygame.time.get_ticks()
        
        # Retro Pixel Style Score Display - Compact
        scale = 1.0
        if current_time - self.score_pop_time < 300:
            scale = 1.0 + (300 - (current_time - self.score_pop_time)) / 300 * 0.2
        
        # Score box - pixelated style (optimized)
        score_text = str(self.score)
        score_font_size = int(28 * scale)
        score_font = pygame.font.Font(None, score_font_size)
        score_width = score_font.size(score_text)[0]
        
        score_box = pygame.Rect(15, 15, max(100, score_width + 30), 42)
        pygame.draw.rect(self.display_surface, '#1a1a1a', score_box)
        pygame.draw.rect(self.display_surface, '#FFD700', score_box, 3)
        pygame.draw.rect(self.display_surface, '#000000', score_box.inflate(6, 6), 2)
        
        # Pixel corners (8-bit style)
        corner_size = 4
        pygame.draw.rect(self.display_surface, '#FFD700', (score_box.left-2, score_box.top-2, corner_size, corner_size))
        pygame.draw.rect(self.display_surface, '#FFD700', (score_box.right-2, score_box.top-2, corner_size, corner_size))
        pygame.draw.rect(self.display_surface, '#FFD700', (score_box.left-2, score_box.bottom-2, corner_size, corner_size))
        pygame.draw.rect(self.display_surface, '#FFD700', (score_box.right-2, score_box.bottom-2, corner_size, corner_size))
        
        # Score label
        label_font = pygame.font.Font(None, 20)
        label_surf = label_font.render('SCORE', True, '#888888')
        self.display_surface.blit(label_surf, (22, 19))
        
        # Score value - pixelated font
        score_surf = score_font.render(score_text, True, '#FFFF00')
        self.display_surface.blit(score_surf, (22, 33))
        
        # Level box - pixelated style (optimized)
        level_font = pygame.font.Font(None, 28)
        level_text = f'{self.current_level_index}'
        level_value_width = level_font.size(level_text)[0]
        level_label_width = label_font.size('LEVEL')[0]
        
        box_width = max(level_label_width, level_value_width) + 30
        level_box = pygame.Rect(WIDTH - box_width - 15, 15, box_width, 42)
        pygame.draw.rect(self.display_surface, '#1a1a1a', level_box)
        pygame.draw.rect(self.display_surface, '#00FFFF', level_box, 3)
        pygame.draw.rect(self.display_surface, '#000000', level_box.inflate(6, 6), 2)
        
        # Pixel corners
        pygame.draw.rect(self.display_surface, '#00FFFF', (level_box.left-2, level_box.top-2, corner_size, corner_size))
        pygame.draw.rect(self.display_surface, '#00FFFF', (level_box.right-2, level_box.top-2, corner_size, corner_size))
        pygame.draw.rect(self.display_surface, '#00FFFF', (level_box.left-2, level_box.bottom-2, corner_size, corner_size))
        pygame.draw.rect(self.display_surface, '#00FFFF', (level_box.right-2, level_box.bottom-2, corner_size, corner_size))
        
        # Level label
        stage_surf = label_font.render('LEVEL', True, '#888888')
        self.display_surface.blit(stage_surf, (level_box.left + 7, 19))
        
        # Level value
        level_surf = level_font.render(level_text, True, '#00FFFF')
        self.display_surface.blit(level_surf, (level_box.left + 7, 33))

        enemy_count = len(self.enemy_sprites)
        if not self.has_key: msg = "Find the Key!"; color = 'yellow'
        elif enemy_count > 0: msg = f"Defeat Enemies: {enemy_count}"; color = 'red'
        else: msg = "GO TO THE DOOR! ->"; color = 'green'
        
        mission_surf = self.font.render(msg, True, color)
        mission_rect = mission_surf.get_rect(center=(WIDTH/2, 30))
        self.display_surface.blit(mission_surf, mission_rect)

        heart_start_x, heart_start_y = 20, 70
        shake_x = 0
        if current_time - self.heart_shake_time < 200:
            import random
            shake_x = random.randint(-3, 3)
        
        for i in range(3):
            heart_x = heart_start_x + (i * 50) + shake_x
            hp_for_this_heart = self.player.health - (i * 2)
            
            if hp_for_this_heart >= 2:
                self.display_surface.blit(self.heart_full, (heart_x, heart_start_y))
            elif hp_for_this_heart == 1:
                self.display_surface.blit(self.heart_half, (heart_x, heart_start_y))
            else:
                self.display_surface.blit(self.heart_empty, (heart_x, heart_start_y))
        
        for text_data in self.floating_texts[:]:
            text_data['pos'][1] += text_data['vel']
            text_data['life'] -= 1
            alpha = int(255 * (text_data['life'] / 60))
            text_surf = self.font.render(text_data['text'], True, '#FFD700')
            text_surf.set_alpha(alpha)
            self.display_surface.blit(text_surf, text_data['pos'])
            if text_data['life'] <= 0:
                self.floating_texts.remove(text_data)
        
        if self.show_level_banner and current_time - self.level_start_time < self.banner_duration:
            self.draw_level_banner()
        elif current_time - self.level_start_time >= self.banner_duration:
            self.show_level_banner = False
    
    def draw_level_banner(self):
        level_names = [
            "First Steps", "The Pits", "Fragile Ground", "Spiked Path", "Saw Zone",
            "Air Assault", "Fire Line", "Vertical Climb", "Fragile Passage", "Strong Guard",
            "Saw Labyrinth", "High Risk", "Strategic Climb", "Spiked Road", "Grand Finale"
        ]
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill('#000000')
        self.display_surface.blit(overlay, (0, 0))
        
        level_num = self.game_over_font.render(f'LEVEL {self.current_level_index}', True, '#FFD700')
        level_name = self.font.render(level_names[self.current_level_index - 1], True, '#FFFFFF')
        
        self.display_surface.blit(level_num, (WIDTH//2 - level_num.get_width()//2, HEIGHT//2 - 50))
        self.display_surface.blit(level_name, (WIDTH//2 - level_name.get_width()//2, HEIGHT//2 + 20))

    def show_game_over_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill('#2c2c2c')
        self.display_surface.blit(overlay, (0,0))
        
        panel_rect = pygame.Rect((WIDTH-600)//2, (HEIGHT-500)//2, 600, 500)
        pygame.draw.rect(self.display_surface, '#4a3f35', panel_rect, border_radius=20)
        pygame.draw.rect(self.display_surface, '#c7a47a', panel_rect, 5, border_radius=20)
        
        title_surf = self.game_over_font.render("GAME OVER", True, '#d95763')
        self.display_surface.blit(title_surf, title_surf.get_rect(center=(WIDTH/2, panel_rect.top+80)))
        
        self.display_surface.blit(self.game_over_player, self.game_over_player.get_rect(center=(WIDTH/2-150, panel_rect.centery)))
        
        score_t = self.score_font.render("Final Score", True, '#c7a47a')
        score_v = self.score_font.render(str(self.score), True, 'white')
        self.display_surface.blit(score_t, (WIDTH/2+50, panel_rect.centery-30))
        self.display_surface.blit(score_v, (WIDTH/2+90, panel_rect.centery+30))
        
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        restart_rect = pygame.Rect(0,0,200,60); restart_rect.center=(WIDTH/2, panel_rect.bottom-100)
        if restart_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.display_surface, '#d95763', restart_rect, border_radius=10)
            if click: 
                self.reset_game()
                return
        else: pygame.draw.rect(self.display_surface, '#c7a47a', restart_rect, border_radius=10)
        
        r_text = self.font.render("RESTART", True, '#2c2c2c')
        self.display_surface.blit(r_text, r_text.get_rect(center=restart_rect.center))
        
        quit_rect = pygame.Rect(0,0,120,35); quit_rect.center=(WIDTH/2, panel_rect.bottom-30)
        if quit_rect.collidepoint(mouse_pos):
            q_text = self.font.render("Quit Game", True, '#d95763')
            if click: pygame.quit(); sys.exit()
        else: q_text = self.font.render("Quit Game", True, '#888888')
        self.display_surface.blit(q_text, q_text.get_rect(center=quit_rect.center))

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.draw_sprites_with_particles(self.particle_group)
        for projectile in self.projectile_group:
            offset_pos = projectile.rect.topleft - self.visible_sprites.offset
            self.display_surface.blit(projectile.image, offset_pos)
        
        current_time = pygame.time.get_ticks()
        banner_active = self.show_level_banner and current_time - self.level_start_time < self.banner_duration
        
        if self.game_active and not self.paused and not banner_active:
            self.player.update()
            
            for sprite in self.visible_sprites:
                if sprite != self.player:
                    sprite.update()
            
            self.hazard_sprites.update()
            self.falling_platforms.update()
            self.particle_group.update()
            
            for enemy in self.enemy_sprites:
                if hasattr(enemy, 'can_shoot') and enemy.can_shoot:
                    enemy.shoot(self.projectile_group)
            
            self.projectile_group.update()
            
            self.enemy_collision_reverse()
            self.falling_platform_check()
            self.coin_collision()
            self.combat_logic()
            self.hazard_collision()
            self.projectile_collision()
            
            self.check_level_complete()
            self.check_death()
        
        self.display_ui()
        
        if not self.game_active:
            self.show_game_over_screen()

    def coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player, self.coin_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.score += 100
                self.score_pop_time = pygame.time.get_ticks()
                self.floating_texts.append({
                    'text': '+100',
                    'pos': list(coin.rect.center),
                    'vel': -2,
                    'life': 60
                })
                create_coin_particles(coin.rect.center, self.particle_group)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.camera_speed = 0.1
        
        self.deadzone_width = 200
        self.deadzone_height = 150
        
        try:
            self.background = pygame.image.load('assets/background/sky.png').convert_alpha()
            self.bg_width = self.background.get_width()
        except:
            self.background = None
            self.bg_width = WIDTH

    def custom_draw(self, player):
        target_x = player.rect.centerx - WIDTH / 2
        
        self.offset.x += (target_x - self.offset.x) * self.camera_speed
        
        self.offset.x = max(0, self.offset.x)
        self.offset.y = 0
        
    def draw_sprites_with_particles(self, particle_group):
        if self.background:
            rel_x = self.offset.x * 0.2
            bg_x1 = -(rel_x % self.bg_width)
            bg_x2 = bg_x1 + self.bg_width
            
            self.display_surface.blit(self.background, (bg_x1, 0))
            self.display_surface.blit(self.background, (bg_x2, 0))
            if bg_x2 + self.bg_width < WIDTH:
                self.display_surface.blit(self.background, (bg_x2 + self.bg_width, 0))
        else:
            self.display_surface.fill('#87ceeb')
        
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            if isinstance(sprite, Enemy):
                bar_width = 40; bar_height = 6
                bar_x = offset_pos[0] + (sprite.image.get_width()//2) - (bar_width//2)
                bar_y = offset_pos[1] - 10
                ratio = sprite.health / sprite.max_health
                pygame.draw.rect(self.display_surface, '#2c2c2c', (bar_x, bar_y, bar_width, bar_height))
                pygame.draw.rect(self.display_surface, '#d95763', (bar_x, bar_y, bar_width*ratio, bar_height))
        
        for particle in particle_group:
            offset_pos = particle.rect.topleft - self.offset
            self.display_surface.blit(particle.image, offset_pos)