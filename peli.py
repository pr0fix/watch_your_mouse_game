import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("graphics/elephant.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 370:
            self.gravity = -20
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 370:
            self.rect.bottom = 370
    
    def update(self):
        self.player_input()
        self.apply_gravity()

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/mouse.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), 370))
    
    def update(self):
        self.rect.x -= 5
        if self.rect.x <= -100:
            self.kill()

class Bush(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("graphics/bush.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), 390))

    def update(self):
        self.rect.x -= 5
        if self.rect.x <= -100:
            self.kill()

class Fly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        fly_1 = pygame.image.load("graphics/flyFly1.png").convert_alpha()
        fly_2 = pygame.image.load("graphics/flyFly2.png").convert_alpha()
        self.frames = [fly_1, fly_2]
        self.animation_idx = 0
        self.image = self.frames[self.animation_idx]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), 270))

    def animation_state(self):
        self.animation_idx += 0.1
        if self.animation_idx >= len(self.frames):
            self.animation_idx = 0
        self.image = self.frames[int(self.animation_idx)]

    def update(self):
        self.animation_state()
        self.rect.x -= 5
        if self.rect.x <= -100:
            self.kill()

def create_obstacle():
    obstacle_type = choice(["mouse", "mouse", "bush", "fly"])
    if obstacle_type == "mouse":
        obstacle_group.add(Mouse())
    elif obstacle_type == "bush":
        obstacle_group.add(Bush())
    else:
        obstacle_group.add(Fly())

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(f'Score:{current_time}', False, "Black")
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time
    
def check_collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Watch Your Mouse!")
icon = pygame.image.load("graphics/elephant.png").convert_alpha()
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
game_font = pygame.font.Font("font\PublicPixel.ttf", 15)
game_active = False
start_time = 0
score = 0
victory = False
bg_music = pygame.mixer.Sound("audio/bg_music.ogg")
bg_music.set_volume(0.2)
bg_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Background img
background_surf = pygame.image.load("graphics/desert_BG.png").convert()

# # Player img on intro screen
intro_player = pygame.image.load("graphics/elephant.png")
intro_player = pygame.transform.rotozoom(intro_player, 0, 2)
intro_player_rect = intro_player.get_rect(center = (400, 200))

# Game title on intro screen
game_title = game_font.render("Watch Your Mouse!", False, "Black")
game_title_rect = game_title.get_rect(center = (400, 70))

# Intro screen instructions
game_instructions = game_font.render("Press space to run", False, "Black")
game_instructions_rect = game_instructions.get_rect(center = (400, 330))

# End game screen
end_game_image = pygame.image.load("graphics/small-sheep.png")
end_game_image = pygame.transform.rotozoom(end_game_image, 0, 2)
end_game_rect = end_game_image.get_rect(center = (400, 200))

gem_image = pygame.image.load("graphics/gem.png")
gem_image = pygame.transform.rotozoom(gem_image, 0, 2)
gem_image_rect = gem_image.get_rect(center = (200, 200))


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Ground !!!!! CHANGE THIS !!!!!
ground_surf = pygame.Surface((800, 100), pygame.SRCALPHA)
ground_surf.fill((100,100,100,100))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                create_obstacle()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                score = 0
                victory = False
            
    if game_active:
        # Render background
        screen.blit(background_surf, (0,0))

        # Ground
        screen.blit(ground_surf, (0, 370))
        
        # Scoreboard
        score = display_score()

        # Player (elephant)
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # End game if player collides with obstacles
        game_active = check_collisions()

        if score >= 20:
            victory = True
        
        if victory:
            screen.fill((94, 129, 162))
            win_message = game_font.render(f"Congratulations you have won the game, here's a gem!", False, "Black")
            win_message_rect = win_message.get_rect(center = (400, 330))
            screen.blit(gem_image, gem_image_rect)
            screen.blit(end_game_image, end_game_rect)
            screen.blit(win_message, win_message_rect)
            pygame.display.update()
            pygame.time.wait(3000)
            pygame.quit()
            exit()

    else:
        screen.fill((94, 129, 162)) # change background color later
        screen.blit(intro_player, intro_player_rect)

        player_score = game_font.render(f"Your final score: {score}", False, "Black")
        player_score_rect = player_score.get_rect(center = (400, 330))
        screen.blit(game_title, game_title_rect)

        if score == 0:
            screen.blit(game_instructions, game_instructions_rect)
        else:
            screen.blit(player_score, player_score_rect)
        
    pygame.display.update()
    clock.tick(60)