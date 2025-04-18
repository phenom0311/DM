# 게임 승리 조건
# - 적을 쏴서 죽인다
# 게임 실패 조건
# - 총알에 맞아 죽는다.


import os
import pygame

#################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() 


# 화면 크기 설정
screen_width = 1400 #가로 크기
screen_height = 800 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Dual") #게임 이름

# FPS
clock = pygame.time.Clock()
#################################################################

# 1. 사용자 게임 초기화 (배경, 게임 이미지, 좌표, 속도, 캐릭터, 폰트 등)

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환


# 폰트
game_font = pygame.font.Font(None, 100)
total_time = 30
start_ticks = pygame.time.get_ticks() # 시작 시간 정의

# 배경 이미지 불러오기
background2 = pygame.image.load(os.path.join(image_path, "background2.png"))


# 바 만들기
dualbar = pygame.image.load(os.path.join(image_path, "dualbar.png"))
dualbar_size = dualbar.get_rect().size

# 캐릭터(스프라이트) --1-- 불러오기

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size # 이미지의 크기 구하기
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치 (가로)
character_y_pos = screen_height / 2 - 200 






# 캐릭터(스프라이트) --2-- 불러오기

character2 = pygame.image.load(os.path.join(image_path, "character2.png"))
character2_size = character2.get_rect().size # 이미지의 크기 구하기
character2_width = character2_size[0] # 캐릭터의 가로 크기
character2_height = character2_size[1] # 캐릭터의 세로 크기
character2_x_pos = (screen_width / 2) - (character2_width / 2) # 화면 가로의 절반 크기에 해당하는 곳에 위치 (가로)
character2_y_pos = screen_height / 2 + 200 




# 캐릭터 이동 방향 1P
character_to_x_LEFT = 0
character_to_x_RIGHT = 0
character_to_y_UP = 0
character_to_y_DOWN = 0


# 캐릭터 이동 방향 2P
character2_to_x_LEFT = 0
character2_to_x_RIGHT = 0
character2_to_y_UP = 0
character2_to_y_DOWN = 0


# 캐릭터 이동 속도
character_speed = 5
character2_speed = 5


########################## ~무기~ ############################


# 무기 만들기
at1 = pygame.image.load(os.path.join(image_path, "at1.png"))
at1_size = at1.get_rect().size
at1_width = at1_size[0]

# 무기2P 만들기
at2 = pygame.image.load(os.path.join(image_path, "at2.png"))
at2_size = at2.get_rect().size
at2_width = at2_size[0]

# 무기는 한 번에 여러 발 발사 가능
at1x = []
at2x = []

# 무기 이동 속도
at1_speed = 8
at2_speed = 8



# Time Over(시간 초과 - 무승부)
game_result = "Easter Egg"



# 반복문
g2_running = True
while g2_running:
    dt = clock.tick(60)
    
    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            g2_running = False 
        

    ##########################키보드 #########################

        # 캐릭터 1p 키 이벤트
        if event.type == pygame.KEYDOWN: # 누를때
            if event.key == ord('a'): 
                character_to_x_LEFT -= character_speed
            elif event.key == ord('d'):
                character_to_x_RIGHT += character_speed
            elif event.key == ord('w'):
                character_to_y_UP -= character_speed
            elif event.key == ord('s'):
                character_to_y_DOWN += character_speed
            elif event.key == ord('g'): # 무기 발사
                at1_x_pos = character_x_pos + (character_width / 2) - (at1_width / 2)
                at1_y_pos = character_y_pos
                at1x.append([at1_x_pos, at1_y_pos])

        if event.type == pygame.KEYUP: # 뗄때
            if event.key == ord('a'):
                character_to_x_LEFT = 0
            elif event.key == ord('d'):
                character_to_x_RIGHT = 0
            elif event.key == ord('w'):
                character_to_y_UP = 0
            elif event.key == ord('s'):
                character_to_y_DOWN = 0


        # 캐릭터 2P 키 이벤트
        if event.type == pygame.KEYDOWN: # 누를때
            if event.key == pygame.K_LEFT: 
                character2_to_x_LEFT -= character2_speed
            elif event.key == pygame.K_RIGHT:
                character2_to_x_RIGHT += character2_speed
            elif event.key == pygame.K_UP:
                character2_to_y_UP -= character2_speed
            elif event.key == pygame.K_DOWN:
                character2_to_y_DOWN += character2_speed
            elif event.key == ord('.'): # 무기 발사
                at2_x_pos = character2_x_pos + (character2_width / 2) - (at2_width / 2)
                at2_y_pos = character2_y_pos
                at2x.append([at2_x_pos, at2_y_pos])


        if event.type == pygame.KEYUP: # 뗄때
            if event.key == pygame.K_LEFT:
                character2_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character2_to_x_RIGHT = 0
            elif event.key == pygame.K_UP:
                character2_to_y_UP = 0
            elif event.key == pygame.K_DOWN:
                character2_to_y_DOWN = 0

    # 1P 가로 경계 값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 1P 세로 경계 값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > 330:
        character_y_pos = 330


    # 2P 가로 경계 값 처리
    if character2_x_pos < 0:
        character2_x_pos = 0
    elif character2_x_pos > screen_width - character2_width:
        character2_x_pos = screen_width - character2_width

    # 2P 세로 경계 값 처리
    if character2_y_pos > 800 - character2_height:
        character2_y_pos = 800 - character2_height
    elif character2_y_pos < 450:
        character2_y_pos = 450

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT
    character_y_pos += character_to_y_DOWN + character_to_y_UP
    character2_x_pos += character2_to_x_LEFT + character2_to_x_RIGHT
    character2_y_pos += character2_to_y_DOWN + character2_to_y_UP



    # 무기 위치 조정

    ##################### 1P #################      ㄹㅈㄷ !!!!!
    at1x = [ [w[0], w[1] + at1_speed] for w in at1x] # 무기 위치를 아래로

    ################### 2P #######################
    at2x = [ [w[0], w[1] - at1_speed] for w in at2x] # 무기 위치를 위로


    
    
    # 4. 충돌 처리  ############ 7. text 참조
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    character2_rect = character2.get_rect()
    character2_rect.left = character2_x_pos
    character2_rect.top = character2_y_pos



    ########### 2P 총알 -> 1P 부딪힘
    for at1_idx, at1_val in enumerate(at1x):
        at1_pos_x = at1_val[0]
        at1_pos_y = at1_val[1]

        # 무기 rect 정보 업데이트
        at1_rect = at1.get_rect()
        at1_rect.left = at1_pos_x
        at1_rect.top = at1_pos_y

        if character2_rect.colliderect(at1_rect):
            game_result = "1P Win"
            g2_running = False

    ########### 1P 총알 -> 2P 부딪힘
    for at2_idx, at2_val in enumerate(at2x):
        at2_pos_x = at2_val[0]
        at2_pos_y = at2_val[1]

        # 무기 rect 정보 업데이트
        at2_rect = at1.get_rect()
        at2_rect.left = at2_pos_x
        at2_rect.top = at2_pos_y

        if character_rect.colliderect(at2_rect):
            game_result = "2P Win"
            g2_running = False




    # 5. 화면에 그리기
    # 배경 + 캐릭터 + 무기
    screen.blit(background2, (0, 0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(character2, (character2_x_pos, character2_y_pos))
    screen.blit(dualbar, (0, 0 + 350))
    for at1_x_pos, at1_y_pos in at1x:
        screen.blit(at1, (at1_x_pos, at1_y_pos))
    for at2_x_pos, at2_y_pos in at2x:
        screen.blit(at2, (at2_x_pos, at2_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("TIME : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 367))


    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Draw"
        g2_running = False

    pygame.display.update() # 게임화면 다시 그리기



# 게임 오버 메시지
msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()


# 2초 대기
pygame.time.delay(2000)

pygame.quit() # 종료