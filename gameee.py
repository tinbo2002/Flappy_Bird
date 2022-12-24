import pygame, sys, random
#Create the functions for game (tạo các hàm cho trò chơi)
#Create the function draw floor (tạo ra hàm vẽ cửa sổ trò chơi)
def draw_floor():
    screen.blit(floor,(floor_x_pos,600))
    screen.blit(floor,(floor_x_pos+432,600))
#Create the function create pipe (tạo ra hàm tạo ra những cái ống)
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 750)) # vị trí để thay đổi khoảng cách giữa 2 ống
    return bottom_pipe, top_pipe
#Create the function move pipe (tạo ra hàm di chuyển ống)
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes 
#Create the function draw pipe (tạo ra hàm vẽ ra ống lên cửa sổ game)
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 678:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
#Create the function check collision (tạo ra hàm xử lí va chạm) 
def check_collison(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >=600:
            return False
    return True
#Create the function rotate bird (tạo ra hàm chuyển động của chim)
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*4, 1)
    return new_bird
#Create the function bird animation (tạo ra hàm animation của chim)
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
#Create the function score display (tạo ra hàm hiển thị điểm ra màn hình)
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 250))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 75))
        screen.blit(high_score_surface, high_score_rect)
#Create the function update score (tạo ra hàm cập nhật điểm)
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512) 
pygame.init()
screen = pygame.display.set_mode((432,678))     #Tạo màn hình game
clock = pygame.time.Clock()                     #Set FPS của game
game_font = pygame.font.Font('Filegame/04B_19.ttf', 40)
#Create variables for game (tạo các biến cho trò chơi)
gravity = 0.2
bird_movement = 0
game_active = True
score = 0
high_score = 0
#Chèn background
bg = pygame.image.load('Filegame/assets/background-night.PNG').convert()
bg = pygame.transform.scale2x(bg)
#Chèn sàn
floor = pygame.image.load('Filegame/assets/floor.PNG').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# Create the bird (tạo chim)
bird_down = pygame.transform.scale2x(pygame.image.load('Filegame/assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('Filegame/assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('Filegame/assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down, bird_mid, bird_up] #0 1 2
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load('Filegame/assets/yellowbird-midflap.PNG').convert_alpha()
#bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 300)) 
#Create timer for bird (tạo timer cho chim)
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
#Create the pipe (tạo ống)
pipe_surface = pygame.image.load('Filegame/assets/pipe-green.PNG').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# Create timer for pipe (tạo timer cho ống)
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1000)      # Vị trí thay đổi thời gian spawn ra ống
pipe_height = [280, 290, 300, 310, 320, 330, 340, 350, 400, 500, 600]       # Vị trí thay đổi chiều cao của ống
#Create the screen game over (tạo màn hình kết thúc trò chơi)
game_over_surface = pygame.transform.scale2x(pygame.image.load('Filegame/assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216, 339))
#Insert sound (chèn âm thanh)
flap_sound = pygame.mixer.Sound('Filegame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('Filegame/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Filegame/sound/sfx_point.wav')
score_sound_countdown = 100
#While loop of the game
while True:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:    
                bird_movement = 0
                bird_movement = -6      # Vị trí thay đổi độ nảy của chim
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0
                score = 0 
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe()) 
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
                
    screen.blit(bg,(0,0))
    if game_active:
        # Bird move (Chim di chuyển)
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collison(pipe_list)
        #Pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score +=0.01
        score_display('main game') 
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else: 
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    # Floor
    floor_x_pos -=1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)