import pygame
import random




class Players:
    def __init__(self, x, y , health, image, width, height):
        self.imgP1 = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y
        self.health = health
        self.image = image
        self.width = width
        self.height = height
        self.missiles = []
        self.score = 0
        self.lives = 3

    def add_Missile(self, MissleObj):
        self.missiles.append(MissleObj)

    def position(self):
        return (self.x, self.y)

    def Increase_Score(self):
        self.score += 100

class Enemy:
    def __init__(self):
        self.imgProj = pygame.image.load(r'assets\enemies\enemy1better.png')
        self.x = random.randint(46,900 - 46)
        self.y = random.randint(-1000, 0)
        self.speed = random.randint(5,10)
        self.id = id

    def remove_life(self, playerObj):
        playerObj.lives -= 1
        return playerObj.lives

    def Update(self, playerObj):
        self.y += self.speed
        if self.y > 900:
            self.y = 0
            self.x = random.randint(46,900 - 46)
            self.speed = random.randint(5,10)
            self.remove_life(playerObj)

    def SendCoordinates(self):
        return [self.x, self.y]

class Missile:
    def __init__(self, player1Obj, mainwindow):
        self.imgMissile1 = pygame.image.load(r'assets\laser.png').convert_alpha()
        self.shoot_speed = 15
        self.playerObj = player1Obj
        self.y = 700
        self.window = mainwindow
        self.imgMissile2 = pygame.transform.scale(self.imgMissile1, (40, 80))
        self.state = 'ready'
        self.currentx = []

    def ChangeState(self):
        self.state = 'shot'

    def onFire(self, CurrentX):
        self.currentx.append(CurrentX)

    def shoot(self):
        if len(self.currentx) > 1:
            self.currentx.remove(self.currentx[0])

        self.window.blit(self.imgMissile2, (self.currentx[-1] - 15, self.y))
        self.y -= self.shoot_speed

        if self.y < 0:
            self.y = 700
            self.state = 'ready'

    def getCoords(self):
        if self.currentx == []:
            pass
        else:
            return [self.currentx[0], self.y]


