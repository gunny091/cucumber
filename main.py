# - 팀: 차돌코코아
# 파이썬 버전: 3.10.7
# pygame 버전: 2.1.2
# windows 10 64비트 / pycharm
# - 게임을 만들 때 참고한 것들 https://youtu.be/Dkx8Pl6QKW0 (파이썬 무료 게임 만들기 강의)
# https://stackoverflow.com/questions/51060894/adding-a-data-file-in-pyinstaller-using-the-onefile-option/51061279#51061279 (상대 경로 계산)
# 폰트는 나눔고딕체를 사용했습니다.
# - 컴파일 명령어
# pyinstaller.exe -w -F --add-data="data/*;data" --add-data="data/img/*;data/img" --ico="data/cucumber.ico" -n cucumber main.py
import pygame
import random
import os
import sys

pygame.init()  # 초기화


# 스프라이트 클래스
class Sprite:
    def __init__(self, image_path: str, pos=None, sprite_speed=0.5):
        if pos is None:  # 좌표를 입력하지 않으면 0, 0으로
            pos = (0, 0)
        self.image = pygame.image.load(resource_path(image_path))  # 이미지 설정
        self.width, self.height = self.image.get_rect().size  # 크기 설정
        self.x_pos = pos[0]  # 좌표 설정
        self.y_pos = pos[1]
        self.to_x = 0  # 움직임 설정
        self.to_y = 0
        self.speed = sprite_speed  # 속도 설정

    # 움직이기
    def move(self, screen_collision=True):
        self.x_pos += self.to_x  # 움직이기
        self.y_pos += self.to_y
        # 화면 밖으로 넘어가지 않게
        if screen_collision:
            # x좌표
            if self.x_pos < 0:
                self.x_pos = 0
            if self.x_pos > screen_width - self.width:
                self.x_pos = screen_width - self.width
            # y좌표
            if self.y_pos < 0:
                self.y_pos = 0
            if self.y_pos > screen_height - self.height:
                self.y_pos = screen_height - self.height

    # 화면에 그리기
    def blit(self):
        global screen
        screen.blit(self.image, (self.x_pos, self.y_pos))  # 그리기

    # rect 계산
    def get_rect(self):
        rect = self.image.get_rect()  # 크기 계산
        rect.left, rect.top = self.x_pos, self.y_pos  # 위치 계산

        self.width, self.height = rect.size  # 크기 적용

        return rect  # 결과 리턴

    # 충돌 계산
    def collide_rect(self, other):
        # 충돌 처리를 위한 rect 업데이트
        a_rect = self.get_rect()
        b_rect = other.get_rect()

        # 충돌 확인하고 리턴
        return a_rect.colliderect(b_rect)


# 텍스트 클래스
class Text:
    def __init__(self, content="", pos=None, font=None, size=60, color=None):
        self.content = str(content)
        if font:
            font = resource_path(font)
        self.font = pygame.font.Font(font, size)
        if color is None:
            color = (0, 0, 0)
        self.color = color
        if pos is None:
            pos = (0, 0)
        self.x_pos = pos[0]
        self.y_pos = pos[1]

    def set_content(self, content):
        self.content = str(content)

    def render(self):
        global screen
        screen.blit(self.font.render(self.content, True, self.color), (self.x_pos, self.y_pos))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# 화면 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 크기 설정
pygame.display.set_caption("Cucumber Game")  # 제목 설정
pygame.display.set_icon(pygame.image.load(resource_path("data/cucumber.ico")))

# FPS
clock = pygame.time.Clock()
delta = 0

# 최고 점수
best_score = 0

# 게임 플레이 무한반복
game_quit = False
while not game_quit:

    # 배경 설정
    background = Sprite("data/img/background.png")

    # 캐릭터 설정
    character = Sprite("data/img/character.png")
    character.x_pos = (screen_width - character.width) / 2
    character.y_pos = screen_height - character.height  # 좌표를 가운데 아래로 설정

    # 똥 캐릭터 설정
    cucumbers = list()
    cucumber_cycle = 1500
    cucumber_start_tick = pygame.time.get_ticks()

    # 점수판 설정
    scoreboard = Text("Score: 0", (10, 10), "data/NanumGothicBold.ttf",
                      40, (153, 219, 164))
    score = 0  # 점수는 0

    # 최고 점수판 설정
    best_scoreboard = Text("Best Score: 0", (10, 60), "data/NanumGothicBold.ttf",
                           25, (173, 186, 219))

    # 키보드 정보
    keyboard = dict()

    # 이벤트 루프
    running = True  # 게임 진행 상태
    while running:
        # 60FPS
        delta = clock.tick(60)
        # 현재 틱
        now_tick = pygame.time.get_ticks()
        # 이벤트 체크
        for event in pygame.event.get():
            # 창을 닫으면 게임을 종료
            if event.type == pygame.QUIT:
                running = False
                game_quit = True

            # 키보드를 누르면 키보드 정보에 True로 표시
            if event.type == pygame.KEYDOWN:
                keyboard[event.key] = True

            # 키보드를 떼면 키보드 정보에 False로 표시
            if event.type == pygame.KEYUP:
                keyboard[event.key] = False

        # screen.fill((102, 104, 255))  # 단색 배경 그리기
        background.blit()  # 이미지 배경 그리기

        character.to_x = 0
        if keyboard.get(pygame.K_LEFT):
            character.to_x -= character.speed * delta
        if keyboard.get(pygame.K_RIGHT):
            character.to_x += character.speed * delta

        character.move()  # 캐릭터 움직이기
        character.blit()  # 캐릭터 그리기

        if (now_tick - cucumber_start_tick) > cucumber_cycle:
            cucumber = Sprite("data/img/cucumber.png")
            cucumber.x_pos = random.randint(0, screen_width - cucumber.width)  # 가로는 랜덤
            cucumber.y_pos = 0  # 맨 위
            cucumber.speed = 0.4
            cucumbers.append(cucumber)

            cucumber_start_tick = now_tick
            if cucumber_cycle > 600:
                cucumber_cycle *= 0.99  # 600까지 점점 빠르게
            else:
                cucumber_cycle = 600  # 600보다 작아지면 600으로 고정

        new_cucumbers = []
        for cucumber in cucumbers:
            cucumber.to_y = cucumber.speed * delta
            cucumber.move(False)
            cucumber.blit()  # 적 그리기

            # 충돌 확인
            if character.collide_rect(cucumber):
                running = False  # 충돌하면 게임 종료

            # 바닥을 넘어가지 않았으면 new_cucumbers에 추가, 넘어갔으면 점수 추가 후 삭제
            if not (cucumber.y_pos > screen_height):
                new_cucumbers.append(cucumber)
            else:
                score += 1

        cucumbers = new_cucumbers  # cucumbers 리스트 업데이트

        if score > best_score:
            best_score = score

        scoreboard.set_content("Score: " + str(score))
        scoreboard.render()

        best_scoreboard.set_content("Best Score: " + str(best_score))
        best_scoreboard.render()

        pygame.display.update()  # 화면 업데이트

    # 게임이 끝나면 큰 오이 표시
    background.blit()

    game_over = Sprite("data/img/game_over.png")
    game_over.blit()

    scoreboard.set_content("Score: " + str(score))
    scoreboard.render()

    best_scoreboard.set_content("Best Score: " + str(best_score))
    best_scoreboard.render()

    # 게임오버 화면 표시하기
    pygame.display.update()
    # 게임 종료가 아니면 1초 기다리기
    if not game_quit:
        pygame.time.delay(2000)

# 종료
pygame.quit()
