import pygame
import time
import math
import random

# Initialize the pygame
pygame.init()
pygame.font.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# create the score font

font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(s):
    x, y = 10, 10
    score_r = font.render('Score: ' + str(s), True, (255, 255, 255))
    screen.blit(score_r, (x, y))


def show_txt(text):
    x, y = 370, 200
    win = font.render(text, True, (255, 255, 255))
    screen.blit(win, (x, y))


# background
backround = pygame.transform.scale(pygame.image.load('background.jpg').convert(), (800, 600)).convert()

running = True
# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png').convert()
pygame.display.set_icon(icon)


class Person:
    def __init__(self, image_path, posX, posY, change_rate=0.3):
        img = pygame.image.load(image_path).convert()
        self.img = pygame.transform.scale(img, (32, 32)).convert()
        self.X = posX
        self.Y = posY
        self.rate = change_rate

    def draw(self):
        screen.blit(self.img, (self.X, self.Y))

    def get_x(self):
        return self.X

    def get_y(self):
        return self.Y


class Monster(Person):

    def __init__(self, image_path, posX, posY, change_rate=0.3):
        self.path = image_path
        super(Monster, self).__init__(image_path, posX, posY, change_rate)
        self.draw()

    def move(self):

        self.X += self.rate
        down = 10
        if self.X <= 0:
            self.X = 0
            self.rate = - self.rate
            self.Y += down
        if self.X >= 766:
            self.X = 766
            self.rate = -self.rate
            self.Y += down
        self.draw()

    def respawn(self, change_rate=0.3):
        self.__init__(self.path, random.randint(50, 750),
                      random.randint(50, 350), change_rate=change_rate)

    def hit_floor(self):
        if self.Y >= 600:
            return True
        return False


class Player(Person):
    def __init__(self, path='spaceship.png', x=370, y=480, change_h=0.8, change_v=0.8):
        super(Player, self).__init__(path, x, y)
        self.change_h = change_h
        self.change_v = change_v
        self.h = 0
        self.v = 0
        self.lifes = 3

    def move(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.h -= self.change_h
                if event.key == pygame.K_UP:
                    self.v -= self.change_v
                if event.key == pygame.K_DOWN:
                    self.v += self.change_v
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.h += self.change_v
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.h = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.v = 0

        self.X += self.h
        self.Y += self.v
        if self.X <= 0:
            self.X = 0
        if self.X >= 766:
            self.X = 766
        if self.Y <= 0:
            self.Y = 0
        if self.Y >= 566:
            self.Y = 566

    def collision(self, object):
        distance = math.sqrt((self.X - object.get_x()) * (self.X - object.get_x()) \
                             + (self.Y - object.get_y()) * (self.Y - object.get_y()))
        if distance < 10:
            self.lifes -= 1
            return True
        else:
            return False

    def get_lifes(self):
        return self.lifes


class Bullet:
    def __init__(self, path, x, y):
        img = pygame.image.load(path).convert()
        self.img = pygame.transform.scale(img, (32, 32)).convert()
        self.x = x + 16
        self.y = y + 10
        self.speed = -0.6
        self.draw()

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def fire(self):
        self.y += self.speed
        self.draw()

    def collision(self, object):
        distance = math.sqrt((self.x - object.get_x()) * (self.x - object.get_x()) \
                             + (self.y - object.get_y()) * (self.y - object.get_y()))
        if distance < 20:
            return True
        else:
            return False


monsters = []
for i in range(5):
    monsters.append(Monster('monster.png', random.randint(50, 750), random.randint(50, 300)))
for m in monsters:
    m.draw()
player = Player()
# Game Loop
bu = []
score = 0
lost = False
while running:
    # RGB
    screen.fill((0, 0, 0))
    screen.blit(backround, (0, 0))
    events = pygame.event.get()
    player.move(events)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bu.append(Bullet('bullet.png', player.get_x(), player.get_y()))
    if not bu:
        pass
    else:
        for b in bu:
            b.fire()
            for monster in monsters:
                if b:
                    if b.collision(monster) is True:
                        if (0.3 + (score * 0.04)) < 1:
                            e = (0.3 + (score * 0.1))
                        else:
                            e = 1
                        monster.respawn(change_rate=e)
                        score += 1
                        print(score)
                        bu.remove(b)
    for monster in monsters:
        monster.move()

    player.draw()
    show_score(score)
    for m in monsters:
        if player.collision(m):
            print('You lost a life, now you are at' + str(player.get_lifes()))
        if m.hit_floor():
            lost = True
            break
    if player.get_lifes() <= 0 or lost:
        txt = 'Your Score is:' + str(score)
        show_txt(txt)
        running = False
        pygame.display.update()
        time.sleep(3)

    pygame.display.update()
