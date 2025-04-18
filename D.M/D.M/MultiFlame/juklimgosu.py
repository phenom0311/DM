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
pygame.display.set_caption("배신져스") #게임 이름

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
# 원형 스테이지 불러오기
circ_sur = pygame.Surface((600,600))
h_circ = 300 # 반지름
circ = pygame.draw.circle(background, (255, 255, 255), (700, 400), h_circ)
circle = circ_sur.convert()
circle_x, circle_y = 700, 400 



# 시계 띄우기
font = pygame.font.Font(None, 40)
font_color = pygame.Color('black')
timer_started = True
passed_time = 0

# 캐릭터 불러오기
h_player = pygame.image.load(os.path.join(image_path, "character_1p.png"))
h_player_size = h_player.get_rect().size 
h_player_width = h_player_size[0]  
h_player_height = h_player_size[1]
h_player_x_pos = screen_width / 2
h_player_y_pos = screen_height / 2 - h_player_height / 2


# 캐릭터 이동 방향 1p
h_player_to_x_LEFT = 0
h_player_to_x_RIGHT = 0
h_player_to_y_UP = 0
h_player_to_y_DOWN = 0

# 캐릭터 이동 속도
h_player_speed = 10.0

# 스테이지 레벨 설정
total_score = 0 # 경계값에 도달하는 화염(피한 화염)의 개수 = 점수
total_level = 0 # total_score 에 따른 레벨, 레벨이 증가할 때마다 화염의 개수 증가 (처음 레벨 = 0)
total_level_list = [10, 100, 200, 300, 400, 500] # 점수가 얼마냐에 따라 레벨 설정
flame_count = 20 # 처음 화염의 개수 = 20개

# 화염 설정 
flame_list = list()

#flame_class로 flam_list에 객체 정보 저장
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
        self.flame_speed = random.choice([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]) # 화염의 속도 랜덤 지정
        self.flame_spawn = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']) # 상하좌우 중 랜덤하게 화염이 생성되어 플레이어가 있는 원형경기장 안으로 들어오게 설정

        # 스폰 지점
        if self.flame_spawn == 'LEFT':  # 왼쪽에서 생성되었을 때
            self.flame_x_pos = 380 # 화염 x좌표 (고정)
            self.flame_y_pos = random.randint((screen_height / 2) - h_circ - self.flame_height , (screen_height / 2) + h_circ + 1) # 화염 y좌표 랜덤 선택
            self.flame_rad = random.choice([(1, 2), (2, 2), (2, 1),  (1, -2), (2, -2), (2, -1)]) # 무조건 오른쪽으로 가도록
        elif self.flame_spawn == 'RIGHT':  # 오른쪽에서 생성되었을 때 
            self.flame_x_pos = 1000   # 화염 x좌표 (고정)
            self.flame_y_pos = random.randint((screen_height / 2) - h_circ- self.flame_height , (screen_height / 2) + h_circ + 1) # 화염 y좌표 랜덤 선택 
            self.flame_rad = random.choice([(-1, 2), (-2, 2), (-2, 1), (-1, -2), (-2, -2), (-2, -1)]) # 무조건 왼쪽으로 가도록
        elif self.flame_spawn == 'DOWN':  # 아래쪽에서 생성되었을 때
            self.flame_x_pos = random.randint((screen_width / 2) - h_circ - self.flame_width, (screen_width / 2) + h_circ + 1) # 화염 x좌표 랜덤 선택
            self.flame_y_pos = (screen_height / 2) - h_circ -  self.flame_height # 화염 y좌표 (고정)
            self.flame_rad = random.choice([(2, 1), (2, 2), (1, 2),(-2, 1), (-2, 2), (-1, 2)]) # 무조건 위로 가도록
        elif self.flame_spawn == 'UP':  # 위쪽에서 생성되었을 때
            self.flame_x_pos = random.randint((screen_width / 2) - h_circ - self.flame_width , (screen_width / 2) + h_circ + 1) # 화염 x좌표 랜덤 선택
            self.flame_y_pos = (screen_height / 2) + h_circ   # 화염 y좌표 (고정)
            self.flame_rad = random.choice([(2, -1), (2, -2), (1, -2), (-2, -1), (-2, -2), (-1, -2)]) # 무조건 아래로 가도록



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



#이벤트 루프  
j_running = True # 스타트 화면 실행
j_end = False # 결과창

while j_running: # 죽림고수 실행
    dt = clock.tick(60) #게임 화면의 초당 프레임 수
    pygame.display.set_caption("MultiFlame") # 창의 이름 바꾸기


    # 2. 이벤트 처리 (키보드, 마우스 등)
    print("fps : " + str(clock.get_fps()))
    for event in pygame.event.get():
        # 창이 닫혔을 때
        if event.type == pygame.QUIT:
            running = False 

        # 캐릭터 1p 키 이벤트

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT: 
                h_player_to_x_LEFT -= h_player_speed
            elif event.key == pygame.K_RIGHT: 
                h_player_to_x_RIGHT += h_player_speed
            elif event.key == pygame.K_UP: 
                h_player_to_y_UP -= h_player_speed
            elif event.key == pygame.K_DOWN: 
                h_player_to_y_DOWN += h_player_speed

        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT:
                h_player_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                h_player_to_x_RIGHT = 0
            elif event.key == pygame.K_UP:
                h_player_to_y_UP = 0
            elif event.key == pygame.K_DOWN:
                h_player_to_y_DOWN = 0


    # 3. 게임 캐릭터 위치 정의
    h_player_x_pos += h_player_to_x_LEFT + h_player_to_x_RIGHT  # left right 둘 다 눌렸을 시 이동0, 하나만 눌렀을 시 움직임
    h_player_y_pos += h_player_to_y_DOWN + h_player_to_y_UP     # up down 둘 다 눌렀을 시 이동0, 하나만 눌렀을 시 움직임

    # 화염 생성
    if total_score >= total_level_list[total_level]: # 레벨리스트에 설정되어있는 점수보다 플레이어가 피한 화염의 개수가 더 많을 경우
        total_level += 1 # 레벨 1 추가 -> 화염의 개수도 레벨에 따라 추가됨
    
    if total_level + flame_count >= len(flame_list): # 토탈 레벨과 점수의 합이 flamelist의 값 이상일 때
        flame_list.append(flame_class()) # flamelis에 flameclass(화염)을 하나 더 추가 = 화면에 화염이 한 개 더 생성됨

    if total_level >= 6: # 레벨이 6이 될 경우 게임 끝남
        running = False
        


    # 맵 밖으로 나갈 시 (실패)
    if (h_player_x_pos + h_player_width/2 - 700) ** 2 + (h_player_y_pos + h_player_height / 2 - 400) ** 2> 90000 :
        running = False
      
    # 4. 충돌 처리
    # 1p캐릭터 렉트 설정
    h_player_rect = h_player.get_rect()
    h_player_rect.left = h_player_x_pos
    h_player_rect.top = h_player_y_pos




    # 화염과 캐릭터 충돌 1p
    for i in flame_list: 
        i.flame_coll()
        if h_player_rect.colliderect(i.flame_rect) :
            print("ㅋㅋ")
            print("점수 :", total_score)
            print("레벨 :", total_level)
            running = False

    
    # 5. 화면에 그리기
    
    screen.blit(background, (0, 0))
    screen.blit(h_player, (h_player_x_pos, h_player_y_pos))


    for i in flame_list:
        i.flame_move()
        screen.blit(i.flame_image, (i.flame_x_pos, i.flame_y_pos)) # 화염 움직임에 따라서 flame 화면에 나타내기

    # 화염 가리개
    screen.blit(background_round, (0,0))
    
    # 레벨판
    level = font.render(str(int(total_level)), True, (255, 255, 255))
    screen.blit(level, (screen_width - 100, 20))

    # 점수판
    score = font.render(str(int(total_score)), True, (255, 255, 255))
    screen.blit(score, (screen_width - 100, 60))

    if j_end == True:
        


        break



    pygame.display.update() # 게임화면을 다시 그리기





pygame.time.delay(1000)
#pygame 종료
pygame.quit()