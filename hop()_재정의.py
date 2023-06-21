import turtle
import math

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech")
wn.setup(800, 800)
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

shapes = ["wizard.gif", "goblin.gif", "pacman.gif", "cherry.gif", "bar.gif", "ball.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)

class Sprite():

    ## 생성자: 스프라이트의 위치, 가로/세로 크기, 이미지 지정

    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    ## 스프라이트 메서드

    # 지정된 위치로 스프라이트 이동 후 도장 찍기
    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    # 충돌 감지 방법 1: 두 스프라이트의 중심이 일치할 때 충돌 발생
    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    # 충돌 감지 방법 2: 두 스프라이트 사이의 거리가 두 객체의 너비의 평균값 보다 작을 때 충돌 발생
    def is_distance_collision(self, other):
        distance = (((self.x-other.x) ** 2) + ((self.y-other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width)/2.0:
            return True
        else:
            return False

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Character(Sprite):
    def __init__(self, x, y, width, height, image, jump=False):
        super().__init__(x, y, width, height, image)
        self.jump = jump
        self.gravity = 0.01                                                

    def hop(self, distance=300, height=100, speed=0.01):
      if self.jump:                                                             # jump = True 일때만 작동
          angle = math.radians(45)                                              # 포물선의 각도 설정 (여기서는 45도로 설정)
          x_velocity = distance * speed * math.cos(angle)                       # x축으로 이동하는 속도
          y_velocity = height * speed * math.sin(angle)                         # y축으로 이동하는 속도
          initial_y_velocity = y_velocity                                       # 초기 상승 속도

          while self.y >= 0:                                                    # 바닥에 닿을 때까지 반복
              self.x += x_velocity
              self.y += y_velocity

              y_velocity -= self.gravity                                        # 점프 중인 캐릭터의 상승 및 하강에 중력을 적용하는 부분
              if y_velocity < -initial_y_velocity:                              # y축으로 이동하는 속도가 초기 상승 속도의 반대방향 보다 작으면
                  y_velocity = -initial_y_velocity                              # y축으로 이동하는 속도를 초기 상승 속도로 바꾼다.
                  break

              self.render(pen)                                                  # 이동할 때 현재 캐릭터를 화면에 그린다.
              wn.update()

wizard = Character(-128, 200, 128, 128, "wizard.gif")
goblin = Sprite(128, 200, 108, 128, "goblin.gif")

pacman = Character(-128, 0, 128, 128, "pacman.gif", jump=True)
cherry = Sprite(128, 0, 128, 128, "cherry.gif")

bar = Sprite(0, -400, 128, 24, "bar.gif")
ball = Sprite(0,-200, 32, 32, "ball.gif")

# 스프라이트 모음 리스트
sprites = [wizard, goblin, pacman, cherry, bar, ball]

# 고블린 이동
def move_goblin():
    goblin.x -= 64

# 팩맨 이동
def move_pacman():
    pacman.x += 30

# 팩맨 점프
def jump_pacman(distance=300, height=100, speed=0.01):
    pacman.hop(distance)

# 야구공 이동
def move_ball():
    ball.y -= 24

# 이벤트 처리
wn.listen()
wn.onkeypress(move_goblin, "Left")  # 왼쪽 방향 화살표 입력
wn.onkeypress(move_pacman, "Right") # 오른쪽 방향 화살표 입력
wn.onkeypress(jump_pacman, "space") # 스페이크 키 입력
wn.onkeypress(move_ball, "Down")    # 아래방향 화살표 입력

while True:

    # 각 스프라이트 위치 이동 및 도장 찍기
    for sprite in sprites:
        sprite.render(pen)

    # 충돌 여부 확인
    if wizard.is_overlapping_collision(goblin):
        wizard.image = "x.gif"

    if pacman.is_distance_collision(cherry):
        cherry.image = "x.gif"

    if bar.is_aabb_collision(ball):
        ball.image = "x.gif"

    wn.update() # 화면 업데이트
    pen.clear() # 스프라이트 이동흔적 삭제