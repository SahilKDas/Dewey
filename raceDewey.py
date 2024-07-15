# I know this is not an ESOLANG
import pygame
import time
import math
from utils import scale_image, blit_rotate_center

pygame.mixer.init()
pygame.mixer.music.load("mainTheme.wav")
pygame.mixer.music.play(-1)

GRASS = scale_image(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale_image(pygame.image.load('imgs/Track1/track.png'), 0.9)

TRACK_BORDER = scale_image(pygame.image.load('imgs/Track1/track-border.png'), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load('imgs/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

ENEMY_CAR = scale_image(pygame.image.load('imgs/purple-car.png'), 0.55)
ENEMY_CAR_SPEED = 3

PLAYER_CAR = scale_image(pygame.image.load('imgs/white-car.png'), 0.55)
PLAYER_CAR_SPEED = 2*ENEMY_CAR_SPEED

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60
PATH = [(163, 86), (67, 89), (61, 484), (337, 743), (436, 485), (593, 507), (631, 738), (739, 724), (723, 367), (387, 350), (417, 258), (716, 254), (720, 92), (288, 83), (272, 411), (172, 414), (177, 258)]

class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()
    
    def get_level_time(self):
        if not self.started:
            return 0
        return self.level_start_time - time.time()

class AbstractCar:
    IMG = PLAYER_CAR
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel


    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    
    def move_backward(self):
        self.vel = min(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x-x), int(self.y-y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = PLAYER_CAR
    START_POS = (180, 200)
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()

class ComputerCar(AbstractCar):
    IMG = ENEMY_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5)

    def draw(self, win):
        super().draw(win)
        # the following code is used for drawing the points on the computer's path
        'self.draw_points(win)'
    
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi
        
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()
        super().move()


def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def move_player(player_car):    
    keys = pygame.key.get_pressed()
    moved = False
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def handle_collision(player_car, computer_car):
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        print('enemy done')
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
            print('bonk')
        else:
            player_car.reset()
            computer_car.reset()
            print('finish')

run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION), (TRACK_BORDER,(0,0))]
player_car = PlayerCar(PLAYER_CAR_SPEED, PLAYER_CAR_SPEED)
computer_car = ComputerCar(ENEMY_CAR_SPEED, ENEMY_CAR_SPEED, PATH)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
        # The following code is used to draw the path of the computer car with simple clicks.
        '''
            if event.type == pygame.MOUSEBUTTONDOWN:     
                pos = pygame.mouse.get_pos()
                computer_car.path.append(pos)
        '''

    move_player(player_car)
    computer_car.move()

    handle_collision(player_car, computer_car)

    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()


# the print statement below is used for debugging the computer car path
print(computer_car.path)
pygame.quit()
