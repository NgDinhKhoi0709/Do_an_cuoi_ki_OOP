import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
intro_count = 3
last_count_update =  pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define font
count_font =  pygame.font.Font("assets/fonts/turok.ttf", 150)
score_font =  pygame.font.Font("assets/fonts/turok.ttf", 30)

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [122, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")

#=load background image
bg_img =  pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# load victory img
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


# function for draw background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# function for draw text
def draw_text(text, font, col, x, y):
    img = font.render(text, True, col)
    screen.blit(img, (x, y))

# function to draw fighter health bars
def draw_health_bar(health, x, y):
    ratio = health/100
    pygame.draw.rect(screen, 'black', (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, 'red', (x, y, 400, 30))
    pygame.draw.rect(screen, 'yellow', (x, y, 400*ratio, 30))

# function to draw grid
def draw_grid():
    # Set grid line colors
    grid_color = (0, 0, 0)  # Grey color
    
    # Draw vertical lines
    for x in range(0, SCREEN_WIDTH, 40):  # Adjust 50 as needed
        pygame.draw.line(screen, grid_color, (x, 0), (x, SCREEN_HEIGHT))
    
    # Draw horizontal lines
    for y in range(0, SCREEN_HEIGHT, 40):  # Adjust 50 as needed
        pygame.draw.line(screen, grid_color, (0, y), (SCREEN_WIDTH, y))

# create two instances of fighters
fighter_1 = Fighter(1, 200, 460, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 1000, 460, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# game loop
running =  True
while running:
    clock.tick(FPS)
    # draw background
    draw_bg()
  
    # draw player health
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 860, 20)
    draw_text("P1: " + str(score[0]), score_font, 'red', 20, 60)
    draw_text("P2: " + str(score[1]), score_font, 'red', 860, 60)
    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), count_font, 'red', SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # update fighter
    fighter_1.update()
    fighter_2.update()

    # draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory img
        screen.blit(victory_img, (510, 250)) 
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            fighter_1 = Fighter(1, 200, 460, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 1000, 460, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
            intro_count = 3

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update display
    pygame.display.update()
#exit pygame
pygame.quit()