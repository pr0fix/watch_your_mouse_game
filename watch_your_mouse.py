import pygame
from sys import exit
from random import randint, choice
from high_score_calculator import save_high_score, get_high_score

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

        if keys[pygame.K_UP] and self.rect.bottom >= 370:
            self.gravity = -20
        
        if pygame.mouse.get_pressed()[0] and self.rect.bottom >= 370:
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

class Coin(pygame.sprite.Sprite):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.animation_speed = 0.1
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), 300))

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

    def update(self):
        self.animate()
        self.rect.x -= 5
        if self.rect.x <= -100:
            self.kill()

def create_coin(frames):
    y_range = range(200, 300)
    y = randint(min(y_range), max(y_range))
    coin = Coin(frames)
    coin.rect.midbottom = (randint(900, 1100), y)

    while pygame.sprite.spritecollideany(coin, obstacle_group):
        coin.rect.midbottom = (randint(900, 1100), y)
    coin_group.add(coin)

def extract_frames(sheet, frame_width, frame_height, num_frames, scale):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    for x in range(0, sheet_width - frame_width * num_frames, frame_width):
        frame = sheet.subsurface((x, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
        frames.append(frame)
    return frames

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
    
def check_collisions(score):
    global high_score

    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        return False
    
    coin_collision = pygame.sprite.spritecollide(player.sprite, coin_group, True)
    for coin in coin_collision:
        score += 5

    return True

def animate_game_title():
    global game_title_scale, game_title_direction

    if game_title_direction == "expand":
        game_title_scale += 0.005
    else:
        game_title_scale -= 0.005
    
    if game_title_scale >= 1.2:
        game_title_direction = "shrink"
    elif game_title_scale <= 1.0:
        game_title_direction = "expand"


    game_title_surface = game_font.render("Watch Your Mouse!", False, (0, 0, 0))
    game_title_surface = pygame.transform.rotozoom(game_title_surface, 0, game_title_scale)

    game_title_rect = game_title_surface.get_rect(center=(400, 60))

    # Blit the animated game title onto the screen
    screen.blit(game_title_surface, game_title_rect)

pygame.init()

# Game screen width & height variables
width = 800
height = 400
screen = pygame.display.set_mode((width,height))

# Game caption
pygame.display.set_caption("Watch Your Mouse!")

# Game icon
icon = pygame.image.load("graphics/elephant.png").convert_alpha()
pygame.display.set_icon(icon)

# Initialize font
game_font = pygame.font.Font("font\PublicPixel.ttf", 15)

# Game state & score system variables
game_active = False
victory = False
clock = pygame.time.Clock()
start_time = 0
score = 0

# Background music
bg_music = pygame.mixer.Sound("audio/bg_music.ogg")
bg_music.set_volume(0.2)
bg_music.play(loops = -1)

# Game title animation variables
game_title_scale = 1.0
game_title_direction = "expand"

# Spritesheet for animated coins
coin_spritesheet = pygame.image.load("graphics/coin.png").convert_alpha()
coin_frames = extract_frames(coin_spritesheet, 16, 16, num_frames=7, scale = 2)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Background img
background_surf = pygame.image.load("graphics/desert_BG.png").convert()
background_surf = pygame.transform.scale(background_surf,(width,height))
background_idx = 0

# Player img on intro screen
intro_player = pygame.image.load("graphics/elephant.png")
intro_player = pygame.transform.rotozoom(intro_player, 0, 2)
intro_player_rect = intro_player.get_rect(center = (400, 180))

# Game title on intro screen
game_title = game_font.render("Watch Your Mouse!", False, "Black")
game_title_rect = game_title.get_rect(center = (400, 60))

# Intro screen instructions
game_instructions = game_font.render("Press space to run", False, "Black")
game_instructions_rect = game_instructions.get_rect(center = (400, 340))

# Get high score
high_score = get_high_score()

# Victory screen sheep
end_game_image = pygame.image.load("graphics/sheep.png")
end_game_image = pygame.transform.rotozoom(end_game_image, 0, 2)
end_game_rect = end_game_image.get_rect(center = (400, 200))

# Victory screen gem
gem_image = pygame.image.load("graphics/gem.png")
gem_image = pygame.transform.rotozoom(gem_image, 0, 2)
gem_image_rect = gem_image.get_rect(center = (250, 260))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Ground
ground_surf = pygame.Surface((width, 100), pygame.SRCALPHA)

# Main game loop
while True:

    # Checking for player events in the game loop
    for event in pygame.event.get():

        # If player quits the game, exit main game loop
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # If game state is set to active start spawning obstacles
        if game_active:
            if event.type == obstacle_timer:
                create_obstacle()
                if randint(1, 10) in [1, 5, 8]:
                    create_coin(coin_frames)

        # If game state is not set to active
        else:
            # If player presses down on the SPACEBAR, 
            # set game to active, start timer and start counting the score
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                score = 0
                victory = False
            
    
    if game_active:
        
        # Render moving background
        screen.blit(background_surf, (background_idx,0))
        screen.blit(background_surf, (width+background_idx, 0))
        if (background_idx==-width):
            screen.blit(background_surf, (width+background_idx,0))
            background_idx=0
        background_idx-=1

        # Render ground
        screen.blit(ground_surf, (0, 370))
        
        # Render scoreboard
        score = display_score()

        # Add player (elephant)
        player.draw(screen)
        player.update()

        # Add obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Add coins
        coin_group.draw(screen)
        coin_group.update()

        # End game if player collides with obstacles
        game_active = check_collisions(score)

        # When score is equal to or higher than 1000 == victory
        if score >= 1000:
            victory = True
        
        # If victory render ending screen
        if victory:
            screen.fill((94, 129, 162))
            win_message = game_font.render(f"Congratulations you have won the game, here's a gem!", False, "Black")
            win_message_rect = win_message.get_rect(center = (400, 330))
            screen.blit(gem_image, gem_image_rect)
            screen.blit(end_game_image, end_game_rect)
            screen.blit(win_message, win_message_rect)
            pygame.display.update()
            pygame.time.wait(5000)
            pygame.quit()
            exit()

    
    else:
        # Show intro player
        screen.fill((94, 129, 162)) # change background color later
        screen.blit(intro_player, intro_player_rect)

        # Display the score player reached on last run
        player_score = game_font.render(f"Your final score: {score}", False, "Black")
        player_score_rect = player_score.get_rect(center = (400, 340))

        # Display animated game title
        animate_game_title()

        # If current score is 0, show intro screen
        if score == 0:
            screen.blit(game_instructions, game_instructions_rect)
        # if score is higher than 0 display player score
        else:
            screen.blit(player_score, player_score_rect)

        # On intro screen and game over screen, show the players current high score
        high_score_text = game_font.render(f"High score: {high_score}", False, "Black")
        high_score_rect = high_score_text.get_rect(center=(400, 300))
        screen.blit(high_score_text, high_score_rect)

    # Update display
    pygame.display.update()
    # Set framerate to 60
    clock.tick(60)