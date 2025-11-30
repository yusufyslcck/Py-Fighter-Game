# main.py - Ana oyun döngüsü ve menü sistemi

import pygame, sys, json, os
from settings import *
from constants import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Py-Fighter')
        self.clock = pygame.time.Clock()
        self.game_state = 'menu'
        self.show_controls_ingame = False
        self.high_score = self.load_high_score()
        self.level = Level()
        self.pause_font = pygame.font.Font(None, 100)
        self.pause_button_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 160)
        self.button_font = pygame.font.Font(None, 60)
        
        try:
            player_img = pygame.image.load('assets/player/idle/0.png').convert_alpha()
            self.menu_player = pygame.transform.scale(player_img, (200, 200))
        except: 
            self.menu_player = pygame.Surface((200,200))
            self.menu_player.fill('red')

        try:
            enemy_img = pygame.image.load('assets/enemy/run/0.png').convert_alpha()
            self.menu_enemy = pygame.transform.scale(enemy_img, (200, 200))
            self.menu_enemy = pygame.transform.flip(self.menu_enemy, True, False)
        except: 
            self.menu_enemy = pygame.Surface((200,200))
            self.menu_enemy.fill('blue')
    
    def load_high_score(self):
        highscore_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'highscore.json')
        try:
            if os.path.exists(highscore_file):
                with open(highscore_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0
    
    def save_high_score(self, score):
        highscore_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'highscore.json')
        try:
            with open(highscore_file, 'w') as f:
                json.dump({'high_score': score}, f)
        except:
            pass

    def draw_menu(self):
        self.screen.fill('#87ceeb')

        title_text = "PY-FIGHTER"
        shadow_surf = self.title_font.render(title_text, True, 'black')
        shadow_rect = shadow_surf.get_rect(center = (WIDTH/2 + 5, HEIGHT/3 + 5))
        self.screen.blit(shadow_surf, shadow_rect)
        
        title_surf = self.title_font.render(title_text, True, '#d95763')
        title_rect = title_surf.get_rect(center = (WIDTH/2, HEIGHT/3))
        self.screen.blit(title_surf, title_rect)
        
        high_score_font = pygame.font.Font(None, 45)
        high_score_text = f"HIGH SCORE: {self.high_score}"
        high_score_surf = high_score_font.render(high_score_text, True, '#ffbe0b')
        high_score_shadow = high_score_font.render(high_score_text, True, '#1a1a1a')
        high_score_pos = (WIDTH/2, HEIGHT/3 + 70)
        self.screen.blit(high_score_shadow, high_score_shadow.get_rect(center=(high_score_pos[0] + 2, high_score_pos[1] + 2)))
        self.screen.blit(high_score_surf, high_score_surf.get_rect(center=high_score_pos))

        self.screen.blit(self.menu_player, (100, HEIGHT - 250))
        self.screen.blit(self.menu_enemy, (WIDTH - 300, HEIGHT - 250))

        mouse_pos = pygame.mouse.get_pos()
        
        play_rect = pygame.Rect(WIDTH/2 - 120, HEIGHT/2 + 20, 240, 70)
        play_hover = play_rect.collidepoint(mouse_pos)
        play_color = '#ff9e00' if play_hover else '#ffbe0b'
        play_scale = 5 if play_hover else 0
        
        pygame.draw.rect(self.screen, play_color, 
                         (play_rect.x - play_scale, play_rect.y - play_scale, 
                          play_rect.width + play_scale*2, play_rect.height + play_scale*2), 
                         border_radius=20)
        pygame.draw.rect(self.screen, 'white', 
                         (play_rect.x - play_scale, play_rect.y - play_scale, 
                          play_rect.width + play_scale*2, play_rect.height + play_scale*2), 
                         3, border_radius=20)
        
        play_surf = self.button_font.render("PLAY", True, 'white')
        self.screen.blit(play_surf, play_surf.get_rect(center=play_rect.center))
        
        # Controls Butonu
        controls_rect = pygame.Rect(WIDTH/2 - 120, HEIGHT/2 + 110, 240, 70)
        controls_hover = controls_rect.collidepoint(mouse_pos)
        controls_color = '#64B5F6' if controls_hover else '#2196F3'
        controls_scale = 5 if controls_hover else 0
        
        pygame.draw.rect(self.screen, controls_color, 
                         (controls_rect.x - controls_scale, controls_rect.y - controls_scale, 
                          controls_rect.width + controls_scale*2, controls_rect.height + controls_scale*2), 
                         border_radius=20)
        pygame.draw.rect(self.screen, 'white', 
                         (controls_rect.x - controls_scale, controls_rect.y - controls_scale, 
                          controls_rect.width + controls_scale*2, controls_rect.height + controls_scale*2), 
                         3, border_radius=20)
        
        controls_surf = self.button_font.render("CONTROLS", True, 'white')
        self.screen.blit(controls_surf, controls_surf.get_rect(center=controls_rect.center))
        
        # Quit Butonu
        quit_rect = pygame.Rect(WIDTH/2 - 120, HEIGHT/2 + 200, 240, 70)
        quit_hover = quit_rect.collidepoint(mouse_pos)
        quit_color = '#e74c3c' if quit_hover else '#c0392b'
        quit_scale = 5 if quit_hover else 0
        
        pygame.draw.rect(self.screen, quit_color, 
                         (quit_rect.x - quit_scale, quit_rect.y - quit_scale, 
                          quit_rect.width + quit_scale*2, quit_rect.height + quit_scale*2), 
                         border_radius=20)
        pygame.draw.rect(self.screen, 'white', 
                         (quit_rect.x - quit_scale, quit_rect.y - quit_scale, 
                          quit_rect.width + quit_scale*2, quit_rect.height + quit_scale*2), 
                         3, border_radius=20)
        
        quit_surf = self.button_font.render("QUIT GAME", True, 'white')
        self.screen.blit(quit_surf, quit_surf.get_rect(center=quit_rect.center))
        
        return play_rect, controls_rect, quit_rect

    def draw_ingame_controls(self):
        overlay = pygame.Surface((380, 320))
        overlay.set_alpha(230)
        overlay.fill('#2c3e50')
        self.screen.blit(overlay, (WIDTH - 400, 20))
        pygame.draw.rect(self.screen, '#ecf0f1', (WIDTH - 400, 20, 380, 320), 3, border_radius=10)
        
        title_font = pygame.font.Font(None, 32)
        title_surf = title_font.render("CONTROLS", True, '#ffbe0b')
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH - 210, 45)))
        
        hint_font = pygame.font.Font(None, 22)
        hint_surf = hint_font.render("(Press TAB to hide)", True, '#95a5a6')
        self.screen.blit(hint_surf, hint_surf.get_rect(center=(WIDTH - 210, 70)))
        
        control_font = pygame.font.Font(None, 28)
        controls = [
            ("WASD/Arrows", "Move", 100),
            ("SPACE", "Jump", 140),
            ("F", "Attack", 180),
            ("ESC", "Pause", 220),
            ("TAB", "Toggle Help", 260)
        ]
        
        for key, action, y_offset in controls:
            key_surf = control_font.render(key, True, '#3498db')
            self.screen.blit(key_surf, (WIDTH - 380, y_offset))
            action_surf = control_font.render(f": {action}", True, '#ffffff')
            self.screen.blit(action_surf, (WIDTH - 240, y_offset))
        
        info_font = pygame.font.Font(None, 24)
        info_surf = info_font.render("Find key & reach door!", True, '#f39c12')
        self.screen.blit(info_surf, info_surf.get_rect(center=(WIDTH - 210, 305)))
    
    def draw_controls_menu(self):
        for i in range(HEIGHT):
            color = (25 + i//18, 50 + i//22, 85 + i//12)
            pygame.draw.line(self.screen, color, (0, i), (WIDTH, i))
        
        title_surf = self.title_font.render("CONTROLS", True, '#ffbe0b')
        title_shadow = self.title_font.render("CONTROLS", True, '#1a1a1a')
        self.screen.blit(title_shadow, title_shadow.get_rect(center=(WIDTH/2 + 5, 75)))
        self.screen.blit(title_surf, title_surf.get_rect(center=(WIDTH/2, 70)))
        
        subtitle_font = pygame.font.Font(None, 30)
        subtitle = subtitle_font.render("Master the controls to become a champion!", True, '#bdc3c7')
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH/2, 135)))
        
        controls = [
            ("WASD/Arrows", "Move", '#3498db', 165),
            ("SPACE", "Jump", '#2ecc71', 235),
            ("F", "Attack", '#e74c3c', 305),
            ("ESC", "Pause", '#9b59b6', 375),
            ("TAB", "Help", '#f39c12', 445)
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        panel_x = 150
        panel_width = 320
        
        for i, (key_text, action, color, y_pos) in enumerate(controls):
            shadow_offset = 4
            shadow_rect = pygame.Rect(panel_x + shadow_offset, y_pos + shadow_offset, panel_width, 55)
            shadow_surf = pygame.Surface((panel_width, 55))
            shadow_surf.set_alpha(100)
            shadow_surf.fill((0, 0, 0))
            self.screen.blit(shadow_surf, shadow_rect)
            
            key_rect = pygame.Rect(panel_x, y_pos, panel_width, 55)
            pygame.draw.rect(self.screen, color, key_rect, border_radius=12)
            pygame.draw.rect(self.screen, '#ffffff', key_rect, 3, border_radius=12)
            
            key_font = pygame.font.Font(None, 42)
            key_surf = key_font.render(key_text, True, '#ffffff')
            key_rect_center = key_surf.get_rect(center=key_rect.center)
            key_shadow = key_font.render(key_text, True, '#000000')
            self.screen.blit(key_shadow, (key_rect_center.x + 2, key_rect_center.y + 2))
            self.screen.blit(key_surf, key_rect_center)
            
            arrow_font = pygame.font.Font(None, 64)
            arrow_surf = arrow_font.render("=", True, '#ffbe0b')
            self.screen.blit(arrow_surf, (panel_x + panel_width + 40, y_pos + 8))
            
            action_font = pygame.font.Font(None, 48)
            action_surf = action_font.render(action, True, '#ffffff')
            action_shadow = action_font.render(action, True, '#1a1a1a')
            action_x = panel_x + panel_width + 100
            self.screen.blit(action_shadow, action_shadow.get_rect(midleft=(action_x + 2, y_pos + 29)))
            self.screen.blit(action_surf, action_surf.get_rect(midleft=(action_x, y_pos + 27)))
        
        line_y_top = 150
        line_y_bottom = 545
        pygame.draw.line(self.screen, '#ffbe0b', (150, line_y_top), (WIDTH - 150, line_y_top), 2)
        pygame.draw.line(self.screen, '#3498db', (150, line_y_top + 2), (WIDTH - 150, line_y_top + 2), 1)
        pygame.draw.line(self.screen, '#ffbe0b', (150, line_y_bottom), (WIDTH - 150, line_y_bottom), 2)
        pygame.draw.line(self.screen, '#3498db', (150, line_y_bottom + 2), (WIDTH - 150, line_y_bottom + 2), 1)
        
        back_rect = pygame.Rect(WIDTH/2 - 120, 575, 240, 70)
        back_hover = back_rect.collidepoint(mouse_pos)
        back_color = '#e74c3c' if back_hover else '#c0392b'
        back_scale = 6 if back_hover else 0
        
        shadow_surf = pygame.Surface((back_rect.width, back_rect.height))
        shadow_surf.set_alpha(120)
        shadow_surf.fill((0, 0, 0))
        self.screen.blit(shadow_surf, (back_rect.x + 5, back_rect.y + 5))
        
        pygame.draw.rect(self.screen, back_color, 
                         (back_rect.x - back_scale, back_rect.y - back_scale, 
                          back_rect.width + back_scale*2, back_rect.height + back_scale*2), 
                         border_radius=18)
        pygame.draw.rect(self.screen, '#ffffff', 
                         (back_rect.x - back_scale, back_rect.y - back_scale, 
                          back_rect.width + back_scale*2, back_rect.height + back_scale*2), 
                         4, border_radius=18)
        
        back_font = pygame.font.Font(None, 55)
        back_surf = back_font.render("BACK", True, '#ffffff')
        back_shadow = back_font.render("BACK", True, '#000000')
        text_center = back_rect.center
        self.screen.blit(back_shadow, back_shadow.get_rect(center=(text_center[0] + 2, text_center[1] + 2)))
        self.screen.blit(back_surf, back_surf.get_rect(center=text_center))
        
        try:
            player_img = pygame.image.load('assets/player/idle/0.png').convert_alpha()
            player_scaled = pygame.transform.scale(player_img, (120, 120))
            shadow_img = pygame.Surface((120, 120))
            shadow_img.set_alpha(80)
            shadow_img.fill((0, 0, 0))
            self.screen.blit(shadow_img, (42, HEIGHT - 108))
            self.screen.blit(player_scaled, (40, HEIGHT - 110))
            player_flipped = pygame.transform.flip(player_scaled, True, False)
            self.screen.blit(shadow_img, (WIDTH - 158, HEIGHT - 108))
            self.screen.blit(player_flipped, (WIDTH - 160, HEIGHT - 110))
        except:
            pass
        
        return back_rect
    
    def draw_pause_menu(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill('#000000')
        self.screen.blit(overlay, (0, 0))
        
        pause_surf = self.pause_font.render("PAUSED", True, '#FFD700')
        pause_rect = pause_surf.get_rect(center=(WIDTH/2, HEIGHT/3))
        self.screen.blit(pause_surf, pause_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        resume_rect = pygame.Rect(WIDTH/2 - 150, HEIGHT/2, 300, 70)
        resume_hover = resume_rect.collidepoint(mouse_pos)
        resume_color = '#66BB6A' if resume_hover else '#4CAF50'
        pygame.draw.rect(self.screen, resume_color, resume_rect, border_radius=15)
        pygame.draw.rect(self.screen, '#ffffff', resume_rect, 3, border_radius=15)
        resume_text = self.pause_button_font.render("RESUME", True, '#ffffff')
        self.screen.blit(resume_text, resume_text.get_rect(center=resume_rect.center))
        
        restart_rect = pygame.Rect(WIDTH/2 - 150, HEIGHT/2 + 90, 300, 70)
        restart_hover = restart_rect.collidepoint(mouse_pos)
        restart_color = '#FFB74D' if restart_hover else '#FF9800'
        pygame.draw.rect(self.screen, restart_color, restart_rect, border_radius=15)
        pygame.draw.rect(self.screen, '#ffffff', restart_rect, 3, border_radius=15)
        restart_text = self.pause_button_font.render("RESTART", True, '#ffffff')
        self.screen.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
        
        menu_rect = pygame.Rect(WIDTH/2 - 150, HEIGHT/2 + 180, 300, 70)
        menu_hover = menu_rect.collidepoint(mouse_pos)
        menu_color = '#64B5F6' if menu_hover else '#2196F3'
        pygame.draw.rect(self.screen, menu_color, menu_rect, border_radius=15)
        pygame.draw.rect(self.screen, '#ffffff', menu_rect, 3, border_radius=15)
        menu_text = self.pause_button_font.render("MAIN MENU", True, '#ffffff')
        self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))
        
        return resume_rect, restart_rect, menu_rect
    
    def draw_victory_screen(self):
        self.screen.fill('#1a1a2e')
        
        victory_surf = self.title_font.render("VICTORY!", True, '#FFD700')
        victory_rect = victory_surf.get_rect(center=(WIDTH/2, 150))
        shadow_surf = self.title_font.render("VICTORY!", True, '#000000')
        self.screen.blit(shadow_surf, (victory_rect.x + 4, victory_rect.y + 4))
        self.screen.blit(victory_surf, victory_rect)
        
        congrats_font = pygame.font.Font(None, 50)
        congrats_surf = congrats_font.render("You completed all levels!", True, '#ffffff')
        self.screen.blit(congrats_surf, congrats_surf.get_rect(center=(WIDTH/2, 250)))
        
        score_font = pygame.font.Font(None, 70)
        score_surf = score_font.render(f"Final Score: {self.level.score}", True, '#FFD700')
        self.screen.blit(score_surf, score_surf.get_rect(center=(WIDTH/2, 350)))
        
        is_new_record = self.level.score > self.high_score
        if is_new_record:
            new_record_font = pygame.font.Font(None, 55)
            new_record_surf = new_record_font.render("NEW HIGH SCORE!", True, '#ff6b6b')
            new_record_shadow = new_record_font.render("NEW HIGH SCORE!", True, '#000000')
            self.screen.blit(new_record_shadow, new_record_shadow.get_rect(center=(WIDTH/2 + 2, 422)))
            self.screen.blit(new_record_surf, new_record_surf.get_rect(center=(WIDTH/2, 420)))
        else:
            hs_font = pygame.font.Font(None, 45)
            hs_surf = hs_font.render(f"High Score: {self.high_score}", True, '#bdc3c7')
            self.screen.blit(hs_surf, hs_surf.get_rect(center=(WIDTH/2, 420)))
        
        if hasattr(self, 'menu_player'):
            self.screen.blit(self.menu_player, (150, HEIGHT - 250))
        if hasattr(self, 'menu_enemy'):
            self.screen.blit(self.menu_enemy, (WIDTH - 350, HEIGHT - 250))
        
        mouse_pos = pygame.mouse.get_pos()
        
        play_rect = pygame.Rect(WIDTH/2 - 180, 480, 170, 70)
        play_hover = play_rect.collidepoint(mouse_pos)
        play_color = '#66BB6A' if play_hover else '#4CAF50'
        pygame.draw.rect(self.screen, play_color, play_rect, border_radius=15)
        pygame.draw.rect(self.screen, '#ffffff', play_rect, 3, border_radius=15)
        play_text = self.pause_button_font.render("PLAY AGAIN", True, '#ffffff')
        self.screen.blit(play_text, play_text.get_rect(center=play_rect.center))
        
        menu_rect = pygame.Rect(WIDTH/2 + 10, 480, 170, 70)
        menu_hover = menu_rect.collidepoint(mouse_pos)
        menu_color = '#64B5F6' if menu_hover else '#2196F3'
        pygame.draw.rect(self.screen, menu_color, menu_rect, border_radius=15)
        pygame.draw.rect(self.screen, '#ffffff', menu_rect, 3, border_radius=15)
        menu_text = self.pause_button_font.render("MENU", True, '#ffffff')
        self.screen.blit(menu_text, menu_text.get_rect(center=menu_rect.center))
        
        return play_rect, menu_rect

    def run(self):
        while True:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True
                
                # ESC tuşu - Pause toggle
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.game_state == 'playing':
                        self.game_state = 'paused'
                    elif self.game_state == 'paused':
                        self.game_state = 'playing'
                
                # TAB tuşu - In-game controls overlay toggle
                if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    if self.game_state == 'playing':
                        self.show_controls_ingame = not self.show_controls_ingame

            mouse_pos = pygame.mouse.get_pos()

            if self.game_state == 'menu':
                play_rect, controls_rect, quit_rect = self.draw_menu()
                if click:
                    if play_rect.collidepoint(mouse_pos):
                        self.game_state = 'playing'
                        pygame.time.delay(200)
                    elif controls_rect.collidepoint(mouse_pos):
                        self.game_state = 'controls'
                        pygame.time.delay(200)
                    elif quit_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
            
            elif self.game_state == 'controls':
                back_rect = self.draw_controls_menu()
                if click and back_rect.collidepoint(mouse_pos):
                    self.game_state = 'menu'
                    pygame.time.delay(200)
            
            elif self.game_state == 'playing':
                self.screen.fill('#87ceeb')
                self.level.paused = False
                self.level.run()
                
                if self.show_controls_ingame:
                    self.draw_ingame_controls()
                
                if self.level.score > self.high_score:
                    self.high_score = self.level.score
                    self.save_high_score(self.high_score)
                
                if self.level.all_levels_completed:
                    self.game_state = 'victory'
            
            elif self.game_state == 'paused':
                self.screen.fill('#87ceeb')
                self.level.paused = True
                self.level.run()
                resume_rect, restart_rect, menu_rect = self.draw_pause_menu()
                
                if click:
                    if resume_rect.collidepoint(mouse_pos):
                        self.game_state = 'playing'
                    elif restart_rect.collidepoint(mouse_pos):
                        self.level.reset_game()
                        self.game_state = 'playing'
                    elif menu_rect.collidepoint(mouse_pos):
                        self.level.reset_game()
                        self.game_state = 'menu'
            
            elif self.game_state == 'victory':
                play_rect, menu_rect = self.draw_victory_screen()
                
                if click:
                    if play_rect.collidepoint(mouse_pos):
                        self.level.reset_game()
                        self.game_state = 'playing'
                    elif menu_rect.collidepoint(mouse_pos):
                        self.level.reset_game()
                        self.game_state = 'menu'

            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()