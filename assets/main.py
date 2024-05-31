import pygame
from pygame import mixer
from fighter import Fighter

class Main:
    def __init__(self):
        mixer.init()
        pygame.init()

        # Create game window
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Battle Legends")

        # Set framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Define game variables
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000
        self.paused = False

        # Define font
        self.count_font = pygame.font.Font("assets/fonts/turok.ttf", 150)
        self.score_font = pygame.font.Font("assets/fonts/m3x6.ttf", 30)
        self.menu_font = pygame.font.Font(None, 40)

        # Define fighter variables
        self.WARRIOR_SIZE = 162
        self.WARRIOR_SCALE = 4
        self.WARRIOR_OFFSET = [72, 56] 
        self.WARRIOR_DATA = [self.WARRIOR_SIZE, self.WARRIOR_SCALE, self.WARRIOR_OFFSET, 2.75, 10]
        self.WIZARD_SIZE = 250
        self.WIZARD_SCALE = 3
        self.WIZARD_OFFSET = [110, 107]
        self.WIZARD_DATA = [self.WIZARD_SIZE, self.WIZARD_SCALE, self.WIZARD_OFFSET, 4, 7]

        # Load music and sounds
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
        self.magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")

        # Load background image
        self.bg_img = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

        # Load icon game
        self.icon = pygame.image.load("assets/images/icons/ares.png").convert_alpha()
        pygame.display.set_icon(self.icon)

        # Load spritesheets
        self.warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
        self.wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

        # Load victory img
        self.victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

        # Define number of steps in each animation
        self.WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        # Create two instances of fighters
        self.fighter_1 = Fighter(1, 200, 460, False, self.WARRIOR_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx, self.screen)
        self.fighter_2 = Fighter(2, 1000, 460, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx, self.screen)

    def draw_bg(self):
        scaled_bg = pygame.transform.scale(self.bg_img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0, 0))

    def draw_text(self, text, font, col, x, y):
        img = font.render(text, True, col)
        self.screen.blit(img, (x, y))

    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, 'black', (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, 'red', (x, y, 400, 30))
        pygame.draw.rect(self.screen, 'green', (x, y, 400 * ratio, 30))

    def draw_grid(self):
        grid_color = (0, 0, 0)  # Grey color
        
        for x in range(0, self.SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, self.SCREEN_HEIGHT))
        
        for y in range(0, self.SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, grid_color, (0, y), (self.SCREEN_WIDTH, y))

    def draw_menu(self):
        # Draw the pause menu
        self.screen.fill((0, 0, 0, 128))  # Semi-transparent overlay
        self.draw_text("Paused", self.menu_font, 'white', self.SCREEN_WIDTH / 2 - 50, self.SCREEN_HEIGHT / 2 - 100)
        self.draw_text("Press 'R' to Resume", self.menu_font, 'white', self.SCREEN_WIDTH / 2 - 100, self.SCREEN_HEIGHT / 2 - 50)
        self.draw_text("Press 'Q' to Quit", self.menu_font, 'white', self.SCREEN_WIDTH / 2 - 100, self.SCREEN_HEIGHT / 2)
        self.draw_text("Press 'N' for New Game", self.menu_font, 'white', self.SCREEN_WIDTH / 2 - 100, self.SCREEN_HEIGHT / 2 + 50)

    def run_game(self):
        running = True
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
                    self.draw_text(str(self.intro_count), self.count_font, 'red', self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 3)
                    if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                        self.intro_count -= 1
                        self.last_count_update = pygame.time.get_ticks()

                self.fighter_1.update()
                self.fighter_2.update()

                self.fighter_1.draw(self.screen)
                self.fighter_2.draw(self.screen)

                if not self.round_over:
                    if self.fighter_1.alive == False:
                        self.score[1] += 1
                        self.round_over = True
                        self.round_over_time = pygame.time.get_ticks()
                    elif self.fighter_2.alive == False:
                        self.score[0] += 1
                        self.round_over = True
                        self.round_over_time = pygame.time.get_ticks()
                else:
                    self.screen.blit(self.victory_img, (510, 250)) 
                    if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                        self.round_over = False
                        self.fighter_1 = Fighter(1, 200, 460, False, self.WARRIOR_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx, self.screen)
                        self.fighter_2 = Fighter(2, 1000, 460, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx, self.screen)
                        self.intro_count = 3
            else:
                self.draw_menu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                    elif self.paused:
                        if event.key == pygame.K_r:
                            self.paused = False
                        elif event.key == pygame.K_q:
                            running = False
                        elif event.key == pygame.K_n:
                            self.paused = False
                            self.score = [0, 0]
                            self.fighter_1 = Fighter(1, 200, 460, False, self.WARRIOR_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx, self.screen)
                            self.fighter_2 = Fighter(2, 1000, 460, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx, self.screen)
                            self.intro_count = 3

            pygame.display.update()

        pygame.quit()

def main_game():
    main = Main()
    main.run_game()

if __name__ == "__main__":
    main_game()
