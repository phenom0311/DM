# 2403 김성균 2417 주현상 합작
# 멀티게임



import os
import pygame
import random
import time
import math
#################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() 

#화면 크기 설정
screen_width = 1400 #가로 크기
screen_height = 800 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("준비하시구!") #게임 이름

# FPS
clock = pygame.time.Clock()
#################################################################

# 1. 사용자 게임 초기화 (배경, 게임 이미지, 좌표, 속도, 캐릭터, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환


#배경 이미지 불러오기
start_image = pygame.image.load(os.path.join(image_path, "start_image.png"))
background = pygame.image.load(os.path.join(image_path, "background.png"))
background_round = pygame.image.load(os.path.join(image_path, "background_round.png"))
background2 = pygame.image.load(os.path.join(image_path, "background2.png"))


# 원형 스테이지 불러오기
circ_sur = pygame.Surface((600,600))
h_circ = 300 # 반지름
circ = pygame.draw.circle(background, (255, 255, 255), (700, 400), h_circ)
circle = circ_sur.convert()
circle_x, circle_y = 700, 400 


# 바 만들기
dualbar = pygame.image.load(os.path.join(image_path, "dualbar.png"))
dualbar_size = dualbar.get_rect().size


# 폰트
game_font = pygame.font.Font(None, 100)
total_time = 30
start_ticks = pygame.time.get_ticks() # 시작 시간 정의


# 시계 띄우기
font = pygame.font.Font(None, 40)
font_color = pygame.Color('black')
timer_started = True
passed_time = 0


################################# Multi Flame###################################

# 캐릭터 불러오기
character_1p = pygame.image.load(os.path.join(image_path, "character_1p.png"))
character_1p_size = character_1p.get_rect().size 
character_1p_width = character_1p_size[0]  
character_1p_height = character_1p_size[1]
character_1p_x_pos = screen_width / 2 - 100
character_1p_y_pos = screen_height / 2 - character_1p_height / 2

character_2p = pygame.image.load(os.path.join(image_path, "character_2p.png"))
character_2p_size = character_2p.get_rect().size
character_2p_width = character_2p_size[0]
character_2p_height = character_2p_size[1]
character_2p_x_pos = screen_width / 2 + 100
character_2p_y_pos = screen_height / 2 - character_2p_height / 2

# 캐릭터 이동 방향 1p
character_1p_to_x_LEFT = 0
character_1p_to_x_RIGHT = 0
character_1p_to_y_UP = 0
character_1p_to_y_DOWN = 0
character_2p_to_x_LEFT = 0
character_2p_to_x_RIGHT = 0
character_2p_to_y_UP = 0
character_2p_to_y_DOWN = 0


# 캐릭터 이동 속도
character_1p_speed = 10.0
character_2p_speed = 10.0

# 스테이지 레벨 설정
total_score = 0 # 경계값에 도달하는 화염(피한 화염)의 개수 = 점수
total_level = 0 # total_score 에 따른 레벨, 레벨이 증가할 때마다 화염의 개수 증가 (처음 레벨 = 0)
total_level_list = [10, 100, 200, 300, 400, 500] # 점수가 얼마냐에 따라 레벨 설정
flame_count = 20 # 처음 화염의 개수 = 20개

# 화염 설정 (블로그 https://m.blog.naver.com/2020xodn/222009846710 참조함)
flame_list = list() #flame의 리스트fmf 만들어 flame_class 의 객체 하나하나를 담음
class flame_class:
    flame_image = pygame.image.load(os.path.join(image_path, "flame.png"))
    flame_size = flame_image.get_rect().size
    flame_width = flame_size[0]
    flame_height = flame_size[1]
    flame_speed = 0 # 우선 0으로 지정
    flame_x_pos = 0 # 우선 0으로 지정
    flame_y_pos = 0 # 우선 0으로 지정
    flame_rad = 0 # 화염의 이동 방향을 무작위로 지정하는 값
    flame_spawn = None # 우선 None으로 지정

    # 화염 rect 설정
    flame_rect = flame_image.get_rect()
    flame_rect.left = flame_x_pos
    flame_rect.top = flame_y_pos

    def __init__(self):
        # 화염 속도 랜덤으로 지정
        self.flame_speed = random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 4.0]) # 화염의 속도 랜덤 지정
        self.flame_spawn = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']) # 상하좌우 중 랜덤하게 화염이 생성되어 플레이어가 있는 원형경기장 안으로 들어오게 설정

        # 스폰 지점
        if self.flame_spawn == 'LEFT':  # 만약 원의 왼쪽에서 생성되었을 때
            self.flame_x_pos = 380 # 화염 x좌표 (고정)
            self.flame_y_pos = random.randint((screen_height / 2) - h_circ - self.flame_height , (screen_height / 2) + h_circ + 1) # 화염 y좌표 랜덤 선택
            self.flame_rad = random.choice([(1, 2), (2, 2), (2, 1),  (1, -2), (2, -2), (2, -1)]) # 불의 이동 방향 각도 선택 (무조건 오른쪽으로 가도록)
        elif self.flame_spawn == 'RIGHT':  # 만약 원의 오른쪽에서 생성되었을 때 
            self.flame_x_pos = 1000   # 화염 x좌표 (고정)
            self.flame_y_pos = random.randint((screen_height / 2) - h_circ- self.flame_height , (screen_height / 2) + h_circ + 1) # 화염 y좌표 랜덤 선택 
            self.flame_rad = random.choice([(-1, 2), (-2, 2), (-2, 1), (-1, -2), (-2, -2), (-2, -1)]) # 불의 이동 방향 각도 선택 (무조건 왼쪽으로 가도록)
        elif self.flame_spawn == 'DOWN':  # 만약 원의 아래쪽에서 생성되었을 때
            self.flame_x_pos = random.randint((screen_width / 2) - h_circ - self.flame_width, (screen_width / 2) + h_circ + 1) # 화염 x좌표 랜덤 선택
            self.flame_y_pos = (screen_height / 2) - h_circ -  self.flame_height # 화염 y좌표 (고정)
            self.flame_rad = random.choice([(2, 1), (2, 2), (1, 2),(-2, 1), (-2, 2), (-1, 2)]) # 불의 이동 방향 각도 선택(무조건 위로 가도록)
        elif self.flame_spawn == 'UP':  # 만약 원의 위쪽에서 생성되었을 때
            self.flame_x_pos = random.randint((screen_width / 2) - h_circ - self.flame_width , (screen_width / 2) + h_circ + 1) # 화염 x좌표 랜덤 선택
            self.flame_y_pos = (screen_height / 2) + h_circ   # 화염 y좌표 (고정)
            self.flame_rad = random.choice([(2, -1), (2, -2), (1, -2), (-2, -1), (-2, -2), (-1, -2)]) # 불의 이동 방향 각도 선택 (무조건 아래로 가도록)



    #  화염의 움직임과 경계값에 도달했을 시의 점수 등록
    def flame_move(self): # 화염의 좌표에 화염속도와 이동방향을 곱해줌. 즉 
        self.flame_x_pos += self.flame_speed * self.flame_rad[0] # flame_rad의 첫 번째 값을 x스피드에 곱해 화염의 x좌표 속도 조정
        self.flame_y_pos += self.flame_speed * self.flame_rad[1] # flame_rad의 첫 번째 값을 y스피드에 곱해 화염의 x좌표 속도 조정
        global total_score

        # 경계값 설정 = 경계에 도달하면 화염이 사라지고 새로운 화염 생성. 동시에 스코어값 +1
        def score_boundary_UP(): # 위쪽 경계
            if self.flame_y_pos > screen_height/2 + 400:
                return True

        def score_boundary_DOWN(): # 아래쪽 경계
            if self.flame_y_pos < screen_height/2 - 400 :
                return True

        def score_boundary_LEFT(): # 왼쪽 경계
            if self.flame_x_pos < screen_width/2 - 400:
                return True

        def score_boundary_RIGHT(): # 오른쪽 경계
            if self.flame_x_pos > screen_width/2 + 400:
                return True

        if self.flame_spawn == 'UP' : # 위에서 태어난 화염은 좌-우-하의 경계에만 반응
            if score_boundary_LEFT() or score_boundary_RIGHT() or score_boundary_DOWN() :
                flame_list.remove(self)
                total_score += 1

        if self.flame_spawn == 'DOWN' : # 아래에서 태어난 화염은 좌-우-상의 경계에만 반응
            if score_boundary_LEFT() or score_boundary_RIGHT() or score_boundary_UP() :
                flame_list.remove(self)
                total_score += 1

        if self.flame_spawn == 'LEFT' : # 왼쪽에서 태어난 화염은 우-상-하의 경계에만 반응
            if score_boundary_UP() or score_boundary_RIGHT() or score_boundary_DOWN() :
                flame_list.remove(self)
                total_score += 1

        if self.flame_spawn == 'RIGHT' : # 오른쪽에서 태어난 화염은 좌-상-하의 경계에만 반응
            if score_boundary_LEFT() or score_boundary_UP() or score_boundary_DOWN() :
                flame_list.remove(self)
                total_score += 1

    def flame_coll(self): # 화염의 rect를 실시간으로 업데이트(각각의 화염에게 모두 적용됨)
        self.flame_rect = self.flame_image.get_rect()
        self.flame_rect.left = self.flame_x_pos
        self.flame_rect.top = self.flame_y_pos



################################# Dual ###################################

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


######### ~무기~ #########


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
game_result = None




######################### 게임 실행 #########################

#이벤트 루프  
running = True # 스타트 화면 실행
g1_running = False # 게임1 화면, 키1을 누르면 실행
g2_running = False # 게임2 화면, 키2를 누르면 실행


while running:
    dt = clock.tick(1000) #게임 화면의 초당 프레임 수
    start_ticks = pygame.time.get_ticks()


    print("fps : " + str(clock.get_fps()))
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가 
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가
            running = False # 게임이 진행중이 아님 = 끝남


        # 1을 눌렀을 때 -> MultiFlame 실행
        if event.type == pygame.KEYDOWN: # 키 눌러졌는지 확인!
            if event.key == ord('1'):  # 키 '1'이 눌러졌을 시
                running = False # 현재 화면 종료
                g1_running = True # 멀티플레임 실행

            elif event.key == ord('2'):  # 키 '2'가 눌러졌을 시
                running = False # 현재 화면 종료
                g2_running = True # 듀얼 실행



    # 5. 화면에 그리기
    # start image 나타내기
    screen.blit(start_image, (0, 0))

    pygame.display.update() # 게임화면을 다시 그리기!(매번)(반드시 해야함)


####################### Multi Flame 실행 ##########################
while g1_running:
    dt = clock.tick(1000) #게임 화면의 초당 프레임 수
    pygame.display.set_caption("MultiFlame") # 창의 이름 바꾸기


    # 2. 이벤트 처리 (키보드, 마우스 등)
    print("fps : " + str(clock.get_fps()))
    for event in pygame.event.get(): #어떤 이벤트가 발생하였는가 
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가
            g1_running = False # 게임이 진행중이 아님 = 끝남

        # 캐릭터 2P 키 이벤트
        if event.type == pygame.KEYDOWN: # 키 눌러졌는지 확인!
            if event.key == pygame.K_LEFT: 
                character_2p_to_x_LEFT -= character_2p_speed # 왼쪽으로 이동
            elif event.key == pygame.K_RIGHT: 
                character_2p_to_x_RIGHT += character_2p_speed # 오른쪽으로 이동
            elif event.key == pygame.K_UP:
                character_2p_to_y_UP -= character_2p_speed # 위로 이동
            elif event.key == pygame.K_DOWN:
                character_2p_to_y_DOWN += character_2p_speed # 아래로 이동
        if event.type == pygame.KEYUP: # 거북이 펜 업과 같은 개념 (키보드 뗌)
            if event.key == pygame.K_LEFT:
                character_2p_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_2p_to_x_RIGHT = 0
            elif event.key == pygame.K_UP:
                character_2p_to_y_UP = 0
            elif event.key == pygame.K_DOWN:
                character_2p_to_y_DOWN = 0
        # 캐릭터 1p 키 이벤트

        if event.type == pygame.KEYDOWN: # 키 눌러졌는지 확인! 캐릭터 1은 wasd 로 키 설정
            if event.key == ord('a'): # 키 a 를 눌렀을 때
                character_1p_to_x_LEFT -= character_1p_speed
            elif event.key == ord('d'): # 키 d 를 눌렀을 때
                character_1p_to_x_RIGHT += character_1p_speed
            elif event.key == ord('w'): # 키 w 를 눌렀을 때
                character_1p_to_y_UP -= character_1p_speed
            elif event.key == ord('s'): # 키 s 를 눌렀을 때
                character_1p_to_y_DOWN += character_1p_speed
        if event.type == pygame.KEYUP: # 거북이 펜 업과 같은 개념 (키보드 뗌)
            if event.key == ord('a'):
                character_1p_to_x_LEFT = 0
            elif event.key == ord('d'):
                character_1p_to_x_RIGHT = 0
            elif event.key == ord('w'):
                character_1p_to_y_UP = 0
            elif event.key == ord('s'):
                character_1p_to_y_DOWN = 0


    # 3. 게임 캐릭터 위치 정의
    character_1p_x_pos += character_1p_to_x_LEFT + character_1p_to_x_RIGHT  # left right 둘 다 눌렸을 시 이동0, 하나만 눌렀을 시 움직임
    character_1p_y_pos += character_1p_to_y_DOWN + character_1p_to_y_UP     # up down 둘 다 눌렀을 시 이동0, 하나만 눌렀을 시 움직임
    character_2p_x_pos += character_2p_to_x_LEFT + character_2p_to_x_RIGHT  # 동일
    character_2p_y_pos += character_2p_to_y_DOWN + character_2p_to_y_UP     # 동일

    # 화염 생성
    if total_score >= total_level_list[total_level]: # 레벨리스트에 설정되어있는 점수보다 플레이어가 피한 화염의 개수가 더 많을 경우
        total_level += 1 # 레벨 1 추가 -> 화염의 개수도 레벨에 따라 추가됨
    
    if total_level + flame_count >= len(flame_list): # 토탈 레벨과 점수의 합이 flamelist의 값 이상일 때
        flame_list.append(flame_class()) # flamelist에 flameclass(화염)을 하나 더 추가 = 화면에 화염이 한 개 더 생성됨

    if total_level >= 6: # 레벨이 6이 될 경우 게임 끝남
        g1_running = False
        


    # 맵 밖으로 나갈 시 (실패)
    if (character_1p_x_pos + character_1p_width/2 - 700) ** 2 + (character_1p_y_pos + character_1p_height / 2 - 400) ** 2> 90000 :
        g1_running = False
    elif (character_2p_x_pos +character_2p_width/2- 700) ** 2 + (character_2p_y_pos + character_1p_height - 400) ** 2> 90000 :
        g1_running = False
    
    
    
    # 4. 충돌 처리
    # 1p캐릭터 렉트 설정
    character_1p_rect = character_1p.get_rect()
    character_1p_rect.left = character_1p_x_pos
    character_1p_rect.top = character_1p_y_pos

    # 2p 설정
    character_2p_rect = character_2p.get_rect()
    character_2p_rect.left = character_2p_x_pos
    character_2p_rect.top = character_2p_y_pos


    # 캐릭터끼리 충돌
    if character_1p_rect.colliderect(character_2p_rect):
        g1_running = False
        break


    # 화염과 캐릭터 충돌 1p
    for i in flame_list: 
        i.flame_coll()
        if character_1p_rect.colliderect(i.flame_rect) :
            print("ㅋㅋ")
            print("점수 :", total_score)
            print("레벨 :", total_level)
            g1_running = False

    # 화염과 캐릭터 충돌 2p
    for i in flame_list:
        i.flame_coll()
        if character_2p_rect.colliderect(i.flame_rect) :
            print("ㅋㅋ")
            print("점수 :", total_score)
            print("레벨 :", total_level)
            g1_running = False




    
    # 5. 화면에 그리기
    # 배경 + 캐릭터 + 화염 
    screen.blit(background, (0, 0))
    screen.blit(character_1p, (character_1p_x_pos, character_1p_y_pos))
    screen.blit(character_2p, (character_2p_x_pos, character_2p_y_pos))


    for i in flame_list:
        i.flame_move()
        screen.blit(i.flame_image, (i.flame_x_pos, i.flame_y_pos)) # 화염 움직임에 따라서 flame 화면에 나타내기

    # 화염 가리개
    screen.blit(background_round, (0,0))
    
    # 레벨판(?)
    level = font.render(str(int(total_level)), True, (255, 255, 255))
    screen.blit(level, (screen_width - 100, 20))

    # 점수판
    score = font.render(str(int(total_score)), True, (255, 255, 255))
    screen.blit(score, (screen_width - 100, 60))

    pygame.display.update() # 게임화면을 다시 그리기!(매번)(반드시 해야함)



####################### Dual 실행 ##########################
while g2_running:
    dt = clock.tick(60)
    pygame.display.set_caption("Dual") # 창의 이름 바꾸기

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_result = "Easter Egg"
            g2_running = False 
        

    #####키보드 #####

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
    start_ticks == start_ticks
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("TIME : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 367))


    # 시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_result = "Draw"
        g2_running = False




    # 게임 오버 메시지
    msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
    msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)


    pygame.display.update() # 게임화면 다시 그리기









pygame.time.delay(2000)
#pygame 종료
pygame.quit()