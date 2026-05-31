import pygame
from sys import exit
import os
import map
import background
import random

TILE_SIZE = 32
ROW_COUNT = 16
COLUMN_COUNT = 16
GAME_WIDTH = TILE_SIZE * COLUMN_COUNT
GAME_HEIGHT = TILE_SIZE * ROW_COUNT
GAME_MAP = map.GAME_MAP
BACKGROUND = background.BACKGROUND

MAP_START_Y = 7680

PLAYER_X = GAME_WIDTH / 16
PLAYER_Y = MAP_START_Y * 2.05
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 32
PLAYER_DISTANCE = 5

GRAVITY = 0.5
FRICTION = 1
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -9

checkpoint_x = PLAYER_X
checkpoint_y = PLAYER_Y

death_count = 0
jump_count = 0
dash_count = 0

#Camera shake
shake_timer = 0

#Images
def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("images", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

menu_image = load_image("menu.png", (250, 250))
background_image = load_image("pico8.png")

player_image_right = load_image("player_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("player_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

player_image_walk_1_right = load_image("player_walk_1_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_walk_2_right = load_image("player_walk_2_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_walk_1_left = load_image("player_walk_1_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_walk_2_left = load_image("player_walk_2_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

player_image_jump_right = load_image("player_jump_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_left = load_image("player_jump_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

player_image_climb_right = load_image("player_climb_right.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_climb_left = load_image("player_climb_left.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

player_image_jump_right_blue = load_image("player_jump_right_blue.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_left_blue = load_image("player_jump_left_blue.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

player_image_climb_right_blue = load_image("player_climb_right_blue.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_climb_left_blue = load_image("player_climb_left_blue.png", (PLAYER_WIDTH, PLAYER_HEIGHT))

#tiles
spike_image = load_image("spike.png", (TILE_SIZE, TILE_SIZE))
flag_image = load_image("flag.png", (TILE_SIZE, TILE_SIZE))

tile_1 = load_image("tile_1.png", (TILE_SIZE, TILE_SIZE))
tile_2 = load_image("tile_2.png", (TILE_SIZE, TILE_SIZE))
tile_3 = load_image("tile_3.png", (TILE_SIZE, TILE_SIZE))
tile_4 = load_image("tile_4.png", (TILE_SIZE, TILE_SIZE))
tile_5 = load_image("tile_5.png", (TILE_SIZE, TILE_SIZE))
tile_6 = load_image("tile_6.png", (TILE_SIZE, TILE_SIZE))
tile_7 = load_image("tile_7.png", (TILE_SIZE, TILE_SIZE))
tile_8 = load_image("tile_8.png", (TILE_SIZE, TILE_SIZE))
tile_9 = load_image("tile_9.png", (TILE_SIZE, TILE_SIZE))

ice_1 = load_image("ice_1.png", (TILE_SIZE, TILE_SIZE))
ice_2 = load_image("ice_2.png", (TILE_SIZE, TILE_SIZE))
ice_3 = load_image("ice_3.png", (TILE_SIZE, TILE_SIZE))
ice_4 = load_image("ice_4.png", (TILE_SIZE, TILE_SIZE))

inner_ice = load_image("inner_ice.png", (TILE_SIZE, TILE_SIZE))

row_1 = load_image("row_1.png", (TILE_SIZE, TILE_SIZE))
row_2 = load_image("row_2.png", (TILE_SIZE, TILE_SIZE))
row_3 = load_image("row_3.png", (TILE_SIZE, TILE_SIZE))

col_1 = load_image("col_1.png", (TILE_SIZE, TILE_SIZE))
col_2 = load_image("col_2.png", (TILE_SIZE, TILE_SIZE))
col_3 = load_image("col_3.png", (TILE_SIZE, TILE_SIZE))

ball = load_image("ball.png", (TILE_SIZE, TILE_SIZE))

one_way_1 = load_image("tile_1.png", (TILE_SIZE, TILE_SIZE))
one_way_2 = load_image("tile_2.png", (TILE_SIZE, TILE_SIZE))
one_way_3 = load_image("tile_3.png", (TILE_SIZE, TILE_SIZE))

background_1 = load_image("background_1.png", (TILE_SIZE, TILE_SIZE))
background_2 = load_image("background_2.png", (TILE_SIZE, TILE_SIZE))
background_3 = load_image("background_3.png", (TILE_SIZE, TILE_SIZE))
background_4 = load_image("background_4.png", (TILE_SIZE, TILE_SIZE))
background_5 = load_image("background_5.png", (TILE_SIZE, TILE_SIZE))
background_6 = load_image("background_6.png", (TILE_SIZE, TILE_SIZE))
background_7 = load_image("background_7.png", (TILE_SIZE, TILE_SIZE))
background_8 = load_image("background_8.png", (TILE_SIZE, TILE_SIZE))
background_9 = load_image("background_9.png", (TILE_SIZE, TILE_SIZE))

#Sounds
pygame.mixer.init()
def load_sound(sound_name):
    sound = pygame.mixer.Sound(os.path.join("sounds", sound_name))
    return sound

button_sfx = load_sound("button.ogg")
end_button_sfx = load_sound("end_screen_button.ogg")

jump_sfx = [
    load_sound("jump.ogg"),
    load_sound("jump_wall_right.ogg"),
    load_sound("jump_wall_left.ogg")]

dash_sfx = [
    load_sound("dash_red_right.ogg"),
    load_sound("dash_red_left.ogg"),
    load_sound("dash_pink_right.ogg"),
    load_sound("dash_pink_left.ogg")]

death_sfx = load_sound("death.ogg")

walk_sfx = [
    load_sound("foot_04_snow_01.ogg"),
    load_sound("foot_04_snow_02.ogg"),
    load_sound("foot_04_snow_03.ogg"),
    load_sound("foot_04_snow_04.ogg"),
    load_sound("foot_04_snow_05.ogg"),
    load_sound("foot_04_snow_06.ogg"),
    load_sound("foot_04_snow_07.ogg")]

ending_sfx = load_sound("ending.ogg")

#Musics
def load_music(music_name):
    music = pygame.mixer.Sound(os.path.join("musics", music_name))
    return music

musics = [
    load_music("dont ever forget that I love you.ogg"),
    load_music("I_ve-been-dreaming-of-you-lately.ogg"),
    load_music("maybe-in-another-life-128-ytshorts.savetube.me.ogg"),
    load_music("snow-days-to-remember.ogg"),
    load_music("the-dream-that-ends-too-soon.ogg"),
    load_music("The-snow-cat-of-our-dreams.ogg"),
    load_music("tomorrow-is-another-day_-but-I-want-to-stay-here.ogg"),
    load_music("we_ll-be-in-the-snow-if-you-need-us.ogg"),
    load_music("when-you-find-yourself-in-a-memory.ogg"),
    load_music("winter-dream.ogg")
]

for i in range(10):
    musics[i].set_volume(0.25)

music_channel = pygame.mixer.Channel(7) 
song_queue = []

def handle_music():
    global song_queue
    if not music_channel.get_busy():
        if not song_queue:
            song_queue = list(musics)
            random.shuffle(song_queue)
        music_channel.play(song_queue.pop())

pygame.init()

window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("celeste")   
pygame.display.set_icon(player_image_right)
clock = pygame.time.Clock() 
game_over = False

# Snow Class
class Snowflake:
    def __init__(self):
        self.x = random.randint(0, GAME_WIDTH)
        self.y = random.randint(0, GAME_HEIGHT)
        self.speed_y = random.uniform(1, 3)
        self.speed_x = random.uniform(-1, 1)
        self.radius = random.randint(1, 3)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        if self.y > GAME_HEIGHT:
            self.y = -5
            self.x = random.randint(0, GAME_WIDTH)
        if self.x > GAME_WIDTH: self.x = 0
        elif self.x < 0: self.x = GAME_WIDTH

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius)

def show_menu():
    menu_running = True
    font_small = pygame.font.Font('pico-8.ttf', 28)
    font_smaller = pygame.font.Font('pico-8.ttf', 24)
    font_smallest = pygame.font.Font('pico-8.ttf', 16)

    while menu_running:
        handle_music() 
        window.fill("#000000")
        
        image_x = GAME_WIDTH // 2 - menu_image.get_width() // 2
        image_y = 50 
        window.blit(menu_image, (image_x, image_y))

        credit = font_smallest.render("Trinh Van Tuan TH30.04\n3025127196", True, (150, 150, 150))
        tutorial = font_smaller.render("A D or < > to Move\nW or ^ to Jump\nJump twice to Double Jump\nRight or Left-Shift to Dash\n", True, (150, 150, 150))
        start_surf = font_small.render("Press [SPACE] to Start", True, (150, 150, 150))
        
        window.blit(credit, (GAME_WIDTH//4 - start_surf.get_width()//2, GAME_HEIGHT//2 + 225))
        window.blit(tutorial, (GAME_WIDTH//2 - start_surf.get_width()//2, GAME_HEIGHT//2))
        window.blit(start_surf, (GAME_WIDTH//2 - start_surf.get_width()//2, GAME_HEIGHT//2 + 175))

        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False 
                    button_sfx.set_volume(0.2)
                    button_sfx.play()

def show_end_screen():
    end_running = True
    font_large = pygame.font.Font('pico-8.ttf', 36)
    font_small = pygame.font.Font('pico-8.ttf', 24)
    
    while end_running:
        handle_music() 
        window.fill("#000000")
        
        win_surf = font_large.render("LEVEL COMPLETE!", True, (255, 204, 0))
        stats = font_small.render(f"Jumps: {jump_count}\nDashes: {dash_count}\nDeaths: {death_count}", True, (150, 150, 150))
        restart_surf = font_small.render("Press SPACE for Menu", True, (150, 150, 150))
        
        window.blit(win_surf, (GAME_WIDTH//2 - win_surf.get_width()//2, GAME_HEIGHT//2 - 50))
        window.blit(stats, (GAME_WIDTH//2 - stats.get_width()//2, GAME_HEIGHT//2 + 20))
        window.blit(restart_surf, (GAME_WIDTH//2 - restart_surf.get_width()//2, GAME_HEIGHT//2 + 100))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    end_running = False
                    end_button_sfx.set_volume(0.1)
                    end_button_sfx.play()
                    player.y = PLAYER_Y
                    player.x = PLAYER_X

class Particle:
    def __init__(self, x, y, effect_type="dash", direction="right"):
        self.x = x
        self.y = y
        self.radius = random.randint(4, 7)
        
        if effect_type == "dash":
            if direction == "right":
                self.velocity_x = random.uniform(-4, -1)
            else:
                self.velocity_x = random.uniform(1, 4)
            self.velocity_y = random.uniform(-1, 1)
            
        elif effect_type == "jump":
            self.velocity_x = random.uniform(-3, 3)
            self.velocity_y = random.uniform(-2, 0)
            self.radius = random.randint(3, 5) 
            
        self.shrink_rate = random.uniform(0.3, 0.6)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.radius -= self.shrink_rate

class Player(pygame.Rect):
    def __init__(self, x, y): 
        pygame.Rect.__init__(self, x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_y = 0
        self.velocity_x = 0
        self.direction = "right"
        self.jumping = False
        self.jumps_left = 2
        
        #Animation
        self.walk_index = 0
        self.walk_timer = 0
        
        #wall jump & slide
        self.on_wall = False
        self.wall_direction = None
        self.wall_jump_timer = 0

        #dash
        self.can_dash = True
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_direction = "right"
        
        #health
        self.max_health = 1
        self.health = self.max_health

    def update_image(self):
        #Jumping animation
        if self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        
        #Walking animation
        elif self.velocity_x != 0 and not self.on_wall:
            self.walk_timer += 1
            if self.walk_timer >= 10:
                self.walk_timer = 0
                self.walk_index = (self.walk_index + 1) % 2
            
            if self.direction == "right":
                self.image = player_image_walk_1_right if self.walk_index == 0 else player_image_walk_2_right
            else:
                self.image = player_image_walk_1_left if self.walk_index == 0 else player_image_walk_2_left
        
        #Idle
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left
        
        #Climbing animation
        if self.on_wall:
            if self.direction == "right":
                self.image = player_image_climb_right
            elif self.direction == "left":
                self.image = player_image_climb_left

        #Blue hair when can not dash
        if self.can_dash == False:
            if self.direction == "right":
                if self.jumping:
                    self.image = player_image_jump_right_blue
                elif self.on_wall:
                    self.image = player_image_climb_right_blue
            elif self.direction == "left":
                if self.jumping:
                    self.image = player_image_jump_left_blue
                elif self.on_wall:
                    self.image = player_image_climb_left_blue

                    
class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    for row in range(len(GAME_MAP)):
        for column in range(len(GAME_MAP[row])):
            map_code = GAME_MAP[row][column]
            x = column * TILE_SIZE
            y = (row * TILE_SIZE) + MAP_START_Y 
            if map_code == 0:
                continue
            
            elif map_code == 4:
                one_way_platforms.append(Tile(x, y, one_way_1))
            elif map_code == 5:
                one_way_platforms.append(Tile(x, y, one_way_2))
            elif map_code == 6:
                one_way_platforms.append(Tile(x, y, one_way_3))

            elif map_code == 14:
                tiles.append(Tile(x, y, tile_1))
            elif map_code == 15:
                tiles.append(Tile(x, y, tile_2))
            elif map_code == 16:
                tiles.append(Tile(x, y, tile_3))
            elif map_code == 27:
                tiles.append(Tile(x, y, tile_4))
            elif map_code == 28:
                tiles.append(Tile(x, y, tile_5))
            elif map_code == 29:
                tiles.append(Tile(x, y, tile_6))
            elif map_code == 40:
                tiles.append(Tile(x, y, tile_7))
            elif map_code == 41:
                tiles.append(Tile(x, y, tile_8))
            elif map_code == 42:
                tiles.append(Tile(x, y, tile_9))

            elif map_code == 17:
                tiles.append(Tile(x, y, row_1))
            elif map_code == 18:
                tiles.append(Tile(x, y, row_2))
            elif map_code == 19:
                tiles.append(Tile(x, y, row_3))

            elif map_code == 20:
                tiles.append(Tile(x, y, ball))
            
            elif map_code == 33:
                tiles.append(Tile(x, y, col_1))
            elif map_code == 46:
                tiles.append(Tile(x, y, col_2))
            elif map_code == 59:
                tiles.append(Tile(x, y, col_3))

            elif map_code == 53:
                tiles.append(Tile(x, y, ice_1))
            elif map_code == 54:
                tiles.append(Tile(x, y, ice_2))
            elif map_code == 66:
                tiles.append(Tile(x, y, ice_3))
            elif map_code == 67:
                tiles.append(Tile(x, y, ice_4))

            elif map_code == 30:
                tiles.append(Tile(x, y, inner_ice))

            elif map_code == 131:
                spikes.append(Tile(x, y, spike_image))
                
            elif map_code == 248:
                flags.append(Tile(x, y, flag_image))

def background():
    for row in range(len(BACKGROUND)):
        for column in range(len(BACKGROUND[row])):
            bg_code = BACKGROUND[row][column]
            x = column * TILE_SIZE
            y = (row * TILE_SIZE) + MAP_START_Y 
            if bg_code == 0:
                continue
            
            elif bg_code == 634:
                background_tiles.append(Tile(x, y, background_1))
            elif bg_code == 632:
                background_tiles.append(Tile(x, y, background_2))
            elif bg_code == 633:
                background_tiles.append(Tile(x, y, background_3))
            elif bg_code == 645:
                background_tiles.append(Tile(x, y, background_4))
            elif bg_code == 646:
                background_tiles.append(Tile(x, y, background_5))
            elif bg_code == 658:
                background_tiles.append(Tile(x, y, background_6))
            elif bg_code == 659:
                background_tiles.append(Tile(x, y, background_7))
            elif bg_code == 660:
                background_tiles.append(Tile(x, y, background_8))
            elif bg_code == 672:
                background_tiles.append(Tile(x, y, background_9))


def reset_game():
    global player, tiles, background_tiles, spikes, game_over, particles, shake_timer, one_way_platforms, flags, reached_end
    player = Player(checkpoint_x, checkpoint_y) 
    tiles = []
    background_tiles = []
    spikes = []
    particles = [] 
    one_way_platforms = []
    flags = []
    shake_timer = 0
    reached_end = False
    background()
    create_map()
    game_over = False

def check_tile_collision():
    for tile in tiles:
        if player.colliderect(tile):
            return tile
    return None

def check_tile_collision_x():
    player.on_wall = False  
    tile = check_tile_collision()
    if tile is not None:
        if player.velocity_x < 0:
            player.x = tile.x + tile.width
            player.on_wall = True
            player.wall_direction = "left"
        elif player.velocity_x > 0:
            player.x = tile.x - player.width
            player.on_wall = True
            player.wall_direction = "right"
        player.velocity_x = 0

def check_tile_collision_y():
    global checkpoint_x, checkpoint_y
    tile = check_tile_collision()
    if tile is not None:
        if player.velocity_y < 0:
            player.y = tile.y + tile.height
        elif player.velocity_y > 0:
            player.y = tile.y - player.height
            player.jumping = False
            player.jumps_left = 2
            player.can_dash = True 
            player.on_wall = False  
        player.velocity_y = 0

    if player.velocity_y > 0 and not player.is_dashing:
        for platform in one_way_platforms:
            if player.colliderect(platform):
                if (player.y - player.velocity_y + player.height) <= platform.bottom + PLAYER_HEIGHT:
                    player.y = platform.y - PLAYER_HEIGHT
                    player.jumping = False
                    player.jumps_left = 2
                    player.can_dash = True 
                    player.on_wall = False  
                    player.velocity_y = 0
                    checkpoint_x = platform.x
                    checkpoint_y = platform.y - player.height
                    break

def move():
    global game_over, shake_timer, reached_end, death_count
    
    if shake_timer > 0:
        shake_timer -= 1

    if player.is_dashing:
        player.dash_timer -= 1
        player.velocity_y = 0
        for _ in range(2): 
            rand_y = player.centery + random.randint(-10, 10)
            particles.append(Particle(player.centerx, rand_y, "dash", player.dash_direction))

        if player.dash_direction == "right":
            player.velocity_x = 15
        else:
            player.velocity_x = -15
        
        if player.dash_timer <= 0:
            player.is_dashing = False
            player.velocity_x = 0

    if not player.is_dashing:
        if player.wall_jump_timer == 0:
            if player.direction == "left" and player.velocity_x < 0:
                player.velocity_x += FRICTION
            elif player.direction == "right" and player.velocity_x > 0:
                player.velocity_x -= FRICTION
            else:
                player.velocity_x = 0
    player.x += player.velocity_x
    
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > GAME_WIDTH:
        player.x = GAME_WIDTH - player.width

    check_tile_collision_x()
    
    if not player.is_dashing:
        player.velocity_y += GRAVITY    
    
    if player.on_wall and player.velocity_y > 2:
        player.velocity_y = 2  
    
    player.y += player.velocity_y

    check_tile_collision_y()

    for spike in spikes:
        if player.colliderect(spike):
            death_sfx.set_volume(0.05)
            death_sfx.play()
            death_count += 1
            player.health = 0
            
    for flag in flags:
        if player.colliderect(flag):
            reached_end = True
            ending_sfx.set_volume(0.2)
            ending_sfx.play()

    if player.health <= 0:
        game_over = True

    for particle in particles[:]:
        particle.update()
        if particle.radius <= 0:
            particles.remove(particle)

def draw():
    shake_x, shake_y = 0, 0
    if shake_timer > 0:
        shake_x = random.randint(-4, 4)
        shake_y = random.randint(-4, 4)

    camera_y = -(player.y // GAME_HEIGHT) * GAME_HEIGHT
    draw_offset_x = shake_x
    draw_offset_y = shake_y + camera_y

    window.fill("#000000")
    window.blit(background_image, (100 + shake_x, 100 + shake_y))

    for tile in background_tiles:
        window.blit(tile.image, (tile.x + draw_offset_x, tile.y + draw_offset_y))

    for platform in one_way_platforms:
        window.blit(platform.image, (platform.x + draw_offset_x, platform.y + draw_offset_y))

    for tile in tiles:
        window.blit(tile.image, (tile.x + draw_offset_x, tile.y + draw_offset_y)) 

    for spike in spikes:
        window.blit(spike.image, (spike.x + draw_offset_x, spike.y + draw_offset_y))
        
    for flag in flags:
        window.blit(flag.image, (flag.x + draw_offset_x, flag.y + draw_offset_y))

    for particle in particles:
        pygame.draw.circle(window, (255, 255, 255), (int(particle.x + draw_offset_x), int(particle.y + draw_offset_y)), int(particle.radius))

    player.update_image()
    window.blit(player.image, (player.x + draw_offset_x, player.y + draw_offset_y))

    for flake in snowflakes:
        flake.update()
        flake.draw(window)

#start game
player = Player(PLAYER_X, PLAYER_Y)
tiles = []
background_tiles = []
spikes = []
particles = [] 
one_way_platforms = []
flags = []
reached_end = False
snowflakes = [Snowflake() for _ in range(100)] 
background()
create_map()

show_menu()

while True:
    handle_music() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if player.on_wall and player.velocity_y > 0: 
                    player.velocity_y = PLAYER_VELOCITY_Y
                    player.wall_jump_timer = 10
                    if player.wall_direction == "right":
                        player.velocity_x = -PLAYER_VELOCITY_X
                        player.direction = "left"
                        jump_count += 1
                    elif player.wall_direction == "left":
                        player.velocity_x = PLAYER_VELOCITY_X
                        player.direction = "right"
                        jump_count += 1
                    for _ in range(7):
                        sfx = random.choice(walk_sfx)
                        sfx.set_volume(0.05)
                        sfx.play()
                    player.jumping = True
                    player.on_wall = False
                    for _ in range(8):
                        particles.append(Particle(player.centerx, player.bottom, "jump"))
                    for _ in range(3):
                        sfx = random.choice(jump_sfx)
                        sfx.set_volume(0.1)
                        sfx.play()
                elif player.jumps_left > 0:
                    player.velocity_y = PLAYER_VELOCITY_Y
                    player.jumping = True
                    player.jumps_left -= 1
                    for _ in range(10):
                        particles.append(Particle(player.centerx, player.bottom, "jump"))
                    for _ in range(3):
                        sfx = random.choice(jump_sfx)
                        sfx.set_volume(0.1)
                        sfx.play()
                    jump_count += 1 
        
            if (event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT) and player.can_dash:
                player.is_dashing = True
                player.can_dash = False
                player.dash_timer = 10
                player.dash_direction = player.direction
                player.velocity_y = 0
                shake_timer = 10
                for _ in range(12):
                    rand_y = player.centery + random.randint(-15, 15)
                    particles.append(Particle(player.centerx, rand_y, "dash", player.direction))
                for _ in range(4):
                    sfx = random.choice(dash_sfx)
                    sfx.set_volume(0.05)
                    sfx.play()
                dash_count += 1

    keys = pygame.key.get_pressed()

    if player.wall_jump_timer > 0:
        player.wall_jump_timer -= 1  
    else:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velocity_x = -PLAYER_VELOCITY_X
            player.direction = "left"
            if player.jumping == False:
                for _ in range(7):
                    sfx = random.choice(walk_sfx)
                    sfx.set_volume(0.05)
                    sfx.play()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velocity_x = PLAYER_VELOCITY_X
            player.direction = "right"
            if player.jumping == False:
                for _ in range(7):
                    sfx = random.choice(walk_sfx)
                    sfx.set_volume(0.05)
                    sfx.play()

    if game_over:
        reset_game()
        
    if reached_end:
        show_end_screen()
        reset_game()
        jump_count = 0
        dash_count = 0
        death_count = 0
        show_menu()
        player.y = PLAYER_Y
        player.x = PLAYER_X
        
    if not game_over and not reached_end:
        move()
        draw()
        pygame.display.update()
        clock.tick(60)