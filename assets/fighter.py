import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, surface):
        self.surface = surface
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip =  flip
        self.rect = pygame.Rect((x, y, 80, 120))
        self.vel_y = 0
        self.running = False
        self.run_left = flip
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_range =  data[3]
        self.damage =  data[4]
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        self.animation_list = self.load_img(sprite_sheet, animation_steps)
        self.action = 0 #0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death 
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()


    def load_img(self, sprite_sheet, animation_steps):
        # extract imgs from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x*self.size, y*self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size*self.image_scale, self.size*self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # check player 1 controls
            if self.player == 1:
                # movement
                if key[pygame.K_a]: # left
                    dx = -SPEED
                    self.running = True
                    self.run_left = True
                if key[pygame.K_d]: # right
                    dx = SPEED
                    self.running = True
                    self.run_left = False
                # jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -40
                    self.jump = True
                # attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # determine which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            
            # check player 2 controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]: # left
                    dx = -SPEED
                    self.running = True
                    self.run_left =  True
                if key[pygame.K_RIGHT]: # right
                    dx = SPEED
                    self.running = True
                    self.run_left = False
                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -40
                    self.jump = True
                # attack
                if key[pygame.K_k] or key[pygame.K_l]:
                    self.attack(target)
                    # determine which attack type was used
                    if key[pygame.K_k]:
                        self.attack_type = 1
                    if key[pygame.K_l]:
                        self.attack_type = 2

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 140:
            self.vel_y = 0
            self.jump = False
            dy =  screen_height - 140 -  self.rect.bottom
        
        '''# ensure player face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True'''

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 2
        #update player position
        self.rect.x += dx
        self.rect.y += dy

    # handle animation updates
    def update(self):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6) # death
        elif self.hit == True:
            self.update_action(5) # hit
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) # attack1
            elif self.attack_type == 2:
                self.update_action(4) # attcack2
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1) # run
        else:
            self.update_action(0) # idle
        
        animation_cooldown = 50
        #update img
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # check if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # check if damage was taken
                if self.action == 5:
                    self.hit = False
                    # if the player was in the middle of an attack, then the attack is stopped
                    self.attacking = False
                    self.attack_cooldown = 20
         
    def attack(self, target):
        if self.attack_cooldown == 0:
            # execute attack
            self.attacking = True
            self.attack_sound.play()
            attack_rect =  pygame.Rect((self.rect.centerx - (self.attack_range*self.rect.width*self.flip), self.rect.y, self.attack_range*self.rect.width, self.rect.height))
            if attack_rect.colliderect(target.rect):
                target.health -= self.damage
                target.hit = True
            pygame.draw.rect(self.surface, 'blue', attack_rect)

    def update_action(self, new_action):
        # check if the new action different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        if self.run_left:
            self.flip = True
        else:
            self.flip = False
        img =  pygame.transform.flip(self.image, self.flip, False)
        rect = pygame.Rect(self.rect.x, self.rect.y, 80, 160)
        pygame.draw.rect(surface, 'red', rect)
        surface.blit(img, (self.rect.x-(self.offset[0]*self.image_scale), self.rect.y-(self.offset[1]*self.image_scale)))