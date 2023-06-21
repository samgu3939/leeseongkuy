import turtle
import math
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Collision Detection by @TokyoEdtech")
width = 600
height =600
wn.setup(width, height)
wn.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

class Sprite():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    def render(self, pen):
        pen.goto(self.x, self.y)
        pen.shape(self.image)
        pen.stamp()

    def is_overlapping_collision(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def is_distance_collision(self, other):
        distance = (((self.x-other.x) ** 2) + ((self.y-other.y) ** 2)) ** 0.5
        if distance < (self.width + other.width)/2.0:
            return True
        else:
            return False

    def is_aabb_collision(self, other):
        x_collision = (math.fabs(self.x - other.x) * 2) < (self.width + other.width)
        y_collision = (math.fabs(self.y - other.y) * 2) < (self.height + other.height)
        return (x_collision and y_collision)

class Character(Sprite):
    def __init__(self, x, y, width, height, image, jump=False):
        super().__init__(x, y, width, height, image)
        self.jump = jump

    def hop(self, distance=300):
        if self.jump == True:
            self.x += distance

    def move_randomly(self):
        direction = random.choice(["up", "down", "left", "right"])
        distance = 5
        new_x = self.x      # 화면 밖에 나가는 것을 막기 위해 이동 후 새로운 좌표 지정
        new_y = self.y

        if direction == "up":
            new_y += distance
        elif direction == "down":
            new_y -= distance
        elif direction == "left":
            new_x -= distance
        elif direction == "right":
            new_x += distance

        if new_x > width / 2 or new_x < -width / 2 or new_y > height / 2 or new_y < -height / 2:
            return  # 이동을 취소함

        self.x = new_x
        self.y = new_y


shapes = ["goblin.gif", "pacman.gif", "x.gif"]

for shape in shapes:
    wn.register_shape(shape)

pacman_1 = Character(-30, 0, 50, 50, "pacman.gif")
pacman_2 = Character(0, -30, 50, 50, "pacman.gif")
goblin = Sprite(128, 200, 30, 50, "goblin.gif")

def move_goblin_left():
    goblin.x -= 15

def move_goblin_right():
    goblin.x += 15

def move_goblin_up():
    goblin.y += 15

def move_goblin_down():
    goblin.y -= 15

wn.listen()
wn.onkeypress(move_goblin_left, "Left")
wn.onkeypress(move_goblin_right, "Right")
wn.onkeypress(move_goblin_up, "Up")
wn.onkeypress(move_goblin_down, "Down")

sprites = [goblin, pacman_1, pacman_2]

while True:
    for sprite in sprites:
        sprite.render(pen)

        if isinstance(sprite, Character):      # sprite만 랜덤하게 이동
            sprite.move_randomly()

    # 충돌 감지 방법 1: 두 스프라이트의 중심이 일치할 때 충돌 발생  
    if goblin.is_overlapping_collision(pacman_1):
        goblin.image = "x.gif"
      
    # 충돌 감지 방법 2: 두 스프라이트 사이의 거리가 두 객체의 너비의 평균값 보다 작을 때 충돌 발생
    if pacman_1.is_distance_collision(goblin):    
        goblin.image = "x.gif"

    # 충돌 감지 방법 3: 각각의 스프라이트를 둘러썬 경계상자가 겹칠 때 충돌 발생
    if goblin.is_aabb_collision(pacman_2):   
        goblin.image = "x.gif"

    wn.update()
    pen.clear()
