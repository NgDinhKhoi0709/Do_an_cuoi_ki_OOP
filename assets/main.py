import cv2
import pygame
from pygame import mixer
from fighter import Fighter
from button import Button

class Menu:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Battle Legends")
        self.icon = pygame.image.load("assets/images/icons/ares.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.cap = cv2.VideoCapture('assets/images/background/menu_bg.mp4')

        self.name_game_font = pygame.font.Font("assets/fonts/turok.ttf", 165)

        self.tutorial_img = pygame.image.load("assets/images/background/tutorial_bg.png").convert_alpha()
        self.tutorial_bg = cv2.VideoCapture('assets/images/background/tutorial_bg.mp4')

        self.select_bg = cv2.VideoCapture('assets/images/background/select_bg.mp4')

        self.clock = pygame.time.Clock()
        
    def get_font(self, size):
        return pygame.font.Font("assets/fonts/font.ttf", size)

    def load_idle_animation(self, character_choice):
        idle_frames = []
        character_data = {
            'Warrior': ["assets/images/warrior/Sprites/warrior.png", 10, 162, 6],
            'Wizard': ["assets/images/wizard/Sprites/wizard.png", 8, 250, 4],
            'Hero': ["assets/images/hero/Sprites/hero.png", 6, 126, 6]
        }
        character_path, num_frames, size, scale = character_data[character_choice]
        frame = pygame.image.load(character_path).convert_alpha()
        for i in range(num_frames):
            temp_img = frame.subsurface(i * size, 0, size, size)
            idle_frames.append(pygame.transform.scale(temp_img, (int(size * scale), int(size * scale))))
        return idle_frames

    def character_selection(self):
        characters = ['Warrior', 'Wizard', 'Hero']
        current_character_index_1 = current_character_index_2 = 0
        player1_choice, player2_choice = None, None
        selected_character_1 = selected_character_2 = characters[0]
        idle_frames_1 = self.load_idle_animation(selected_character_1)
        idle_frames_2 = self.load_idle_animation(selected_character_2)
        current_frame_1 = current_frame_2 = 0
        last_update = pygame.time.get_ticks()
        animation_speed = 100
        
        
        
        while player1_choice is None or player2_choice is None:
            ret, frame = self.select_bg.read()
            if not ret:
                self.select_bg.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.select_bg.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame = pygame.transform.scale(frame, (1280, 720))
            self.SCREEN.blit(frame, (0, 0))

            title_font = self.get_font(50)
            TITLE_TEXT = title_font.render("Select Your Characters", True, "#b68f40")
            TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
            self.SCREEN.blit(TITLE_TEXT, TITLE_RECT)

            player1_font = self.get_font(45)
            PLAYER1_TEXT = player1_font.render("Player 1:", True, "#b68f40")
            PLAYER1_RECT = PLAYER1_TEXT.get_rect(center=(320, 200))
            self.SCREEN.blit(PLAYER1_TEXT, PLAYER1_RECT)

            PLAYER1_TEXT = player1_font.render("Press t", True, "#b68f40")
            PLAYER1_RECT = PLAYER1_TEXT.get_rect(center=(320, 650))
            self.SCREEN.blit(PLAYER1_TEXT, PLAYER1_RECT)

            PLAYER2_TEXT = player1_font.render("Player 2:", True, "#b68f40")
            PLAYER2_RECT = PLAYER2_TEXT.get_rect(center=(960, 200))
            self.SCREEN.blit(PLAYER2_TEXT, PLAYER2_RECT)

            PLAYER1_TEXT = player1_font.render("Press 2", True, "#b68f40")
            PLAYER1_RECT = PLAYER1_TEXT.get_rect(center=(960, 650))
            self.SCREEN.blit(PLAYER1_TEXT, PLAYER1_RECT)

            now = pygame.time.get_ticks()
            if now - last_update > animation_speed:
                current_frame_1 = (current_frame_1 + 1) % len(idle_frames_1)
                current_frame_2 = (current_frame_2 + 1) % len(idle_frames_2)
                last_update = now
            current_idle_frame_1 = idle_frames_1[current_frame_1]
            current_idle_frame_2 = idle_frames_2[current_frame_2]
            idle_rect = current_idle_frame_1.get_rect(center=(320, 450))
            self.SCREEN.blit(current_idle_frame_1, idle_rect)
            idle_rect = current_idle_frame_2.get_rect(center=(960, 450))
            self.SCREEN.blit(current_idle_frame_2, idle_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_d or event.key == pygame.K_a or event.key == pygame.K_t) and player1_choice == None:
                        if event.key == pygame.K_t:
                            player1_choice = selected_character_1
                            break
                        if event.key == pygame.K_d:
                            tmp = 1
                        else:
                            tmp = -1
                        current_character_index_1 = (current_character_index_1 + tmp) % len(characters)
                        selected_character_1 = characters[current_character_index_1]
                        idle_frames_1 = self.load_idle_animation(selected_character_1)
                        current_frame_1 = 0
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_KP2) and player2_choice == None:
                        if event.key == pygame.K_KP2:
                            player2_choice = selected_character_2
                            break
                        if event.key == pygame.K_RIGHT:
                            tmp = 1
                        else:
                            tmp = -1
                        current_character_index_2 = (current_character_index_2 + tmp) % len(characters)
                        selected_character_2 = characters[current_character_index_2]
                        idle_frames_2 = self.load_idle_animation(selected_character_2)
                        current_frame_2 = 0
                    if event.key == pygame.K_RETURN:
                        if player1_choice is None:
                            player1_choice = selected_character_1
                        else:
                            player2_choice = selected_character_2
                    
            pygame.display.update()
            self.clock.tick(60)

        return player1_choice, player2_choice
    
    def play(self):
        player1_choice, player2_choice = self.character_selection()
        main = Main(player1_choice, player2_choice)
        main.run_game()

    def draw_tutorial(self):
        while True:
            ret, frame = self.tutorial_bg.read()
            if not ret:
                self.tutorial_bg.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.tutorial_bg.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame = pygame.transform.scale(frame, (1280, 720))
            self.SCREEN.blit(frame, (0, 0))
            self.SCREEN.blit(self.tutorial_img, (0, 0))

            pygame.time.delay(80)

            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

            OPTIONS_BACK = Button(image=None, pos=(640, 660),
                                  text_input="BACK", font=self.get_font(50), base_color="#d7fcd4", hovering_color="White")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                        self.main_menu()

            pygame.display.update()

    def main_menu(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame = pygame.transform.scale(frame, (1280, 720))

            self.SCREEN.blit(frame, (0, 0))

            pygame.time.delay(100)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = self.name_game_font.render("BATTLE LEGENDS", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 130))

            PLAY_BUTTON = Button(image=None, pos=(640, 360),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            TUTORIAL_BUTTON = Button(image=None, pos=(640, 510),
                                    text_input="TUTORIAL", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=None, pos=(640, 650),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, TUTORIAL_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cap.release()
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.cap.release()
                        self.play()
                    if TUTORIAL_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.draw_tutorial()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.cap.release()
                        pygame.quit()
                        exit()

            pygame.display.update()
            self.clock.tick(15)

class WinnerScreen:
    def __init__(self, screen_width, screen_height, video_path, winner_choice):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.font = pygame.font.Font("assets/fonts/font.ttf", 60)
        self.winner_font = pygame.font.Font("assets/fonts/turok.ttf", 250)
        
        self.winner_choice = winner_choice
        
        self.clock = pygame.time.Clock()

        self.character_data = {
            'Warrior': ["assets/images/warrior/Sprites/warrior.png", 10, 162, 4],
            'Wizard': ["assets/images/wizard/Sprites/wizard.png", 8, 250, 2.5],
            'Hero': ["assets/images/hero/Sprites/hero.png", 6, 126, 4]
        }
        self.load_winner_idle()

    def load_winner_idle(self):
        self.idle_frames = []
        character_path, num_frames, size, scale = self.character_data[self.winner_choice]
        frame = pygame.image.load(character_path).convert_alpha()
        for i in range(num_frames):
            temp_img = frame.subsurface(i*size, 0, size, size)
            self.idle_frames.append(pygame.transform.scale(temp_img, (size*scale*1.5, size*scale*1.5)))
        self.current_frame = 0
        self.idle_animation_speed = 0.1
        self.last_update = pygame.time.get_ticks()

    def draw_winner_idle(self, screen):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1000 * self.idle_animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.last_update = now
        winner_frame = self.idle_frames[self.current_frame]
        frame_rect = winner_frame.get_rect(center=(self.screen_width // 2, 460))
        screen.blit(winner_frame, frame_rect)

    def display_winner_screen(self, screen):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.screen_width, self.screen_height))
            frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame, (0, 0))

            pygame.time.delay(100)
            
            self.draw_winner_idle(screen)

            img = self.winner_font.render("WINNER", True, 'red')
            screen.blit(img, (280, 20))

            WINNER_MOUSE_POS = pygame.mouse.get_pos()
            
            MAIN_MENU_BUTTON = Button(image=None, pos=(220, 650),
                                      text_input="MENU", font=self.font, base_color="#d7fcd4", hovering_color="White")
            REPLAY_BUTTON = Button(image=None, pos=(650, 650),
                                   text_input="REPLAY", font=self.font, base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=None, pos=(1060, 650),
                                 text_input="QUIT", font=self.font, base_color="#d7fcd4", hovering_color="White")

            for button in [MAIN_MENU_BUTTON, REPLAY_BUTTON, QUIT_BUTTON]:
                button.changeColor(WINNER_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cap.release()
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MAIN_MENU_BUTTON.checkForInput(WINNER_MOUSE_POS):
                        self.cap.release()
                        return "menu"
                    elif REPLAY_BUTTON.checkForInput(WINNER_MOUSE_POS):
                        self.cap.release()
                        return "replay"
                    elif QUIT_BUTTON.checkForInput(WINNER_MOUSE_POS):
                        self.cap.release()
                        pygame.quit()
                        exit()
                    
            pygame.display.update()
            self.clock.tick(15)

    def release_video(self):
        self.cap.release()

class Main:
    def __init__(self, player1_choice, player2_choice):
        mixer.init()
        pygame.init()
        
        self.player1_choice = player1_choice
        self.player2_choice = player2_choice

        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Battle Legends")

        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000
        self.paused = False

        self.count_font = pygame.font.Font("assets/fonts/DungeonFont.ttf", 200)
        self.score_font = pygame.font.Font("assets/fonts/m3x6.ttf", 50)
        self.menu_font = pygame.font.Font(None, 40)
        self.pause_game_font = pygame.font.Font("assets/fonts/font.ttf", 75)
        self.victory_font = pygame.font.Font("assets/fonts/DungeonFont.ttf", 150)

        self.WARRIOR_SIZE = 162
        self.WARRIOR_SCALE = 4
        self.WARRIOR_OFFSET = [72, 56] 
        self.WARRIOR_DATA = [self.WARRIOR_SIZE, self.WARRIOR_SCALE, self.WARRIOR_OFFSET, 2.75, 10]
        
        self.WIZARD_SIZE = 250
        self.WIZARD_SCALE = 3
        self.WIZARD_OFFSET = [110, 107]
        self.WIZARD_DATA = [self.WIZARD_SIZE, self.WIZARD_SCALE, self.WIZARD_OFFSET, 4, 7]

        self.HERO_SIZE = 126
        self.HERO_SCALE = 3.5
        self.HERO_OFFSET = [50, 30]
        self.HERO_DATA = [self.HERO_SIZE, self.HERO_SCALE, self.HERO_OFFSET, 2.80, 10]

        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        self.magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")

        self.icon = pygame.image.load("assets/images/icons/ares.png").convert_alpha()
        pygame.display.set_icon(self.icon)

        self.warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        self.wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
        self.hero_sheet = pygame.image.load("assets/images/hero/Sprites/hero.png").convert_alpha()

        self.WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
        self.HERO_ANIMATION_STEPS = [10, 8, 3, 7, 6, 3, 11]

        self.character_data = {
            'Warrior': [self.WARRIOR_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx],
            'Wizard': [self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx],
            'Hero': [self.HERO_DATA, self.hero_sheet, self.HERO_ANIMATION_STEPS, self.magic_fx]
        }
        self.fighter_1 = Fighter(1, 200, 460, False, *self.character_data[player1_choice], self.screen)
        self.fighter_2 = Fighter(2, 1000, 460, True, *self.character_data[player2_choice], self.screen)

        self.cap = cv2.VideoCapture('assets/images/background/pause_game_bg.mp4')

        self.bg_video = cv2.VideoCapture('assets/images/background/fighting_bg.mp4')

    def draw_bg(self):
        ret, frame = self.bg_video.read()
        if not ret:
            self.bg_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.bg_video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.screen.blit(frame, (0, 0))
        
    def draw_text(self, text, font, col, x, y):
        img = font.render(text, True, col)
        self.screen.blit(img, (x, y))

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, 'black', (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, 'red', (x, y, 400, 30))
        pygame.draw.rect(self.screen, 'green', (x, y, 400 * ratio, 30))

    def draw_pause_menu(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        self.screen.blit(frame, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        RESUME_BUTTON = Button(image=None, pos=(640, 290),
                               text_input="RESUME", font=self.pause_game_font, base_color="#d7fcd4", hovering_color="White")
        NEW_GAME_BUTTON = Button(image=None, pos=(640, 450),
                                 text_input="NEW GAME", font=self.pause_game_font, base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 610),
                             text_input="QUIT", font=self.pause_game_font, base_color="#d7fcd4", hovering_color="White")

        for button in [RESUME_BUTTON, QUIT_BUTTON, NEW_GAME_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(self.screen)

        pygame.display.update()
        self.clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.cap.release()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RESUME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.paused = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.cap.release()
                    pygame.quit()
                    exit()
                if NEW_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    self.paused = False
                    self.score = [0, 0]
                    self.fighter_1 = Fighter(1, 200, 460, False, *self.character_data[self.player1_choice], self.screen)
                    self.fighter_2 = Fighter(2, 1000, 460, True, *self.character_data[self.player2_choice], self.screen)
                    self.intro_count = 3

    def run_game(self):

        running = True
        winner = False
        while running:
            self.clock.tick(self.FPS)
            if not self.paused:
                self.draw_bg()

                self.draw_health_bar(self.fighter_1.health, 20, 20)
                self.draw_health_bar(self.fighter_2.health, 860, 20)
                self.draw_text("P1: " + str(self.score[0]), self.score_font, 'red', 20, 50)
                self.draw_text("P2: " + str(self.score[1]), self.score_font, 'red', 860, 50)
                
                if self.intro_count <= 0:
                    self.fighter_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.fighter_2, self.round_over)
                    self.fighter_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.fighter_1, self.round_over)
                else:
                    self.draw_text(str(self.intro_count), self.count_font, [220, 95, 0], 610, self.SCREEN_HEIGHT / 3)
                    if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                        self.intro_count -= 1
                        self.last_count_update = pygame.time.get_ticks()
                
                self.fighter_1.update()
                self.fighter_2.update()
                
                self.fighter_1.draw(self.screen)
                self.fighter_2.draw(self.screen)
                
                if not self.round_over:
                    if self.fighter_1.alive and self.fighter_2.alive:
                        if self.fighter_1.rect.centerx > self.fighter_2.rect.centerx:
                            self.fighter_1.flip = True
                            self.fighter_2.flip = False
                        else:
                            self.fighter_1.flip = False
                            self.fighter_2.flip = True
                    else:
                        self.round_over = True
                        self.round_over_time = pygame.time.get_ticks()
                        if self.fighter_1.alive:
                            victory = 'P1 Win Round!!!'
                            self.score[0] += 1
                        else:
                            victory = 'P2 Win Round!!!'
                            self.score[1] += 1
                
                if self.round_over:
                    self.draw_text(victory, self.victory_font, [220, 95, 0], 200, 300)
                    if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                        self.round_over = False
                        self.intro_count = 3
                        self.fighter_1 = Fighter(1, 200, 460, False, *self.character_data[self.player1_choice], self.screen)
                        self.fighter_2 = Fighter(2, 1000, 460, True, *self.character_data[self.player2_choice], self.screen)
                
                if self.score[0] >= 3 or self.score[1] >= 3:
                    if self.score[0] >= 3:
                        winner = self.player1_choice  
                    else:
                        winner = self.player2_choice

                    if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                        winner_screen = WinnerScreen(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "assets/images/background/winner_bg.mp4", winner)
                        action = winner_screen.display_winner_screen(self.screen)
                        winner_screen.release_video()

                        if action == "quit":
                            pygame.quit()
                            return
                        elif action == "menu":
                            main_game()
                        elif action == "replay":
                            self.round_over = False
                            self.score = [0, 0]
                            self.fighter_1 = Fighter(1, 200, 460, False, *self.character_data[self.player1_choice], self.screen)
                            self.fighter_2 = Fighter(2, 1000, 460, True, *self.character_data[self.player2_choice], self.screen)

            else:
                self.draw_pause_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused

            pygame.display.update()

        self.bg_video.release()
        self.cap.release()
        pygame.quit()

def main_game():
    menu = Menu()
    menu.main_menu()

if __name__ == "__main__":
    main_game()
