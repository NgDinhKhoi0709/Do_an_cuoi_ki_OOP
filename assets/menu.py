import pygame
import sys
import cv2
from button import Button
from main import main_game

class Menu:
    def __init__(self):
        pygame.init()
        self.SCREEN = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Battle Legends")
        self.icon = pygame.image.load("assets/images/icons/ares.png").convert_alpha()
        pygame.display.set_icon(self.icon)
        self.cap = cv2.VideoCapture('assets/images/background/menu_bg.mp4')
        self.clock = pygame.time.Clock()
        
    def get_font(self, size):
        return pygame.font.Font("assets/fonts/font.ttf", size)

    def play(self):
        main_game()

    def options(self):
        while True:
            OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
            self.SCREEN.fill("white")

            OPTIONS_TEXT = self.get_font(45).render("This is the OPTIONS screen.", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            self.SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            OPTIONS_BACK = Button(image=None, pos=(640, 460),
                                  text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Red")

            OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
            OPTIONS_BACK.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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

            name_game_font = pygame.font.Font("assets/fonts/turok.ttf", 160)
            MENU_TEXT = name_game_font.render("BATTLE LEGENDS", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 130))

            PLAY_BUTTON = Button(image=pygame.image.load("assets/images/button/Play Rect.png"), pos=(640, 330),
                                 text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/button/Options Rect.png"), pos=(640, 480),
                                    text_input="OPTIONS", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/images/button/Quit Rect.png"), pos=(640, 630),
                                 text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="White")

            self.SCREEN.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cap.release()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.cap.release()
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.cap.release()
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            self.clock.tick(15)

def main_run():
    menu = Menu()
    menu.main_menu()

if __name__ == "__main__":
    main_run()
