import pygame
import random
import os
import socket
import _pickle as pickle

#================================================= The connection part ================================================#

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "192.168.56.1"
        self.port = 50007
        self.addr = (self.host, self.port)

    def connect(self, name):
        self.client.connect(self.addr)
        self.client.send(str.encode(name))
        val = self.client.recv(1024)
        return print(val)

    def send(self, data, pick=False):
        try:
            if pick:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(2048*4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)
            return reply
        except socket.error as e:
            print(e)

#===================================================== The classes ====================================================#

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
    def __init__(self, init_x = 0, init_y = 0):
        self.imgProj = pygame.image.load(r'assets\enemies\enemy1better.png')
        self.x = init_x
        self.y = init_y
        self.speed = random.randint(5,10)
        self.id = id

    def remove_life(self, playerObj):
        playerObj.lives -= 1
        return playerObj.lives

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

#=================================================== The game method ==================================================#

# Move speed of the bullet
move_speed = 15

# =============================================== The pygame innit #===================================================#

def lan_game():

    # Moving the player2 object on the screen
    def move_Player2(data):
        if int(data) == 1000:
            pass
        else:
            Player2Obj.x = int(data)

# ============================================== Establishing connection #=============================================#

    Server = Network()
    Server.connect('Player2')

# =============================================== The pygame innit #===================================================#

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    main_window = pygame.display.set_mode((900, 900))

    clock = pygame.time.Clock()
    move_rate = 15
    pygame.mouse.set_visible(False)

    backgroundIMG = pygame.image.load(r'assets\main background.png')

# ===================================================# ALL OBJECTS #===================================================#

    # Players

    Player1Obj = Players(400, 750, 100, r'assets\player 1\player1.png', 58, 61)
    Player2Obj = Players(600, 750, 100, r'assets\player 1\player1.png', 58, 61)

    # Enemies

    Bob = Enemy()
    Martin = Enemy()

    # Missiles

    for i in range (0,2):
        missile = Missile(Player1Obj, main_window)
        Player1Obj.missiles.append(missile)

# =================================================# Sound and Music #=================================================#

    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.90)
    music_li = random.randint(1, 4)
    if music_li == 1:
        pygame.mixer.music.load(r'assets\music\all star.mp3')
    elif music_li == 2:
        pygame.mixer.music.load(r'assets\music\what is love 8 bit.mp3')
    elif music_li == 3:
        pygame.mixer.music.load(r'assets\music\feel good.mp3')
    else:
        pygame.mixer.music.load(r'assets\music\remove.mp3')

    pygame.mixer.music.play(0)

    # the hit variable - used when the player 1 hits an enemy of the other player
    global hit

# ================================================ The main game loop #================================================#

    while open:

        # KEY LISTENERS

        key_listener = pygame.key.get_pressed()
        if (key_listener[pygame.K_LEFT] or key_listener[pygame.K_a]) and Player1Obj.x > 30:
            Player1Obj.x -= move_rate

        elif (key_listener[pygame.K_RIGHT] or key_listener[pygame.K_d]) and Player1Obj.x < 855:
            Player1Obj.x += move_rate

        # Blitting main images, background, players
        main_window.blit(backgroundIMG, (0, 0))
        main_window.blit(Player1Obj.imgP1, (Player1Obj.x - 20, Player1Obj.y))
        main_window.blit(Player2Obj.imgP1, (Player2Obj.x - 20, Player2Obj.y))

        # Looping over the missiles
        for missile in Player1Obj.missiles:
            if missile.state == 'shot':
                missile.shoot()

        # Setting hit to default 0
        hit = 0

        # Looping over missile and collision
        for missile in Player1Obj.missiles:
            a = missile.getCoords()
            if a == None:
                pass
            if a == None:
                pass
            else:
                if missile.state == 'ready':
                    break
                if Martin.y - 20 <= a[1] <= Martin.y + 20 and Martin.x - 30 < a[0] <= Martin.x + 80:
                    print('Martin')
                    missile.state = 'ready'
                    missile.y = 700
                    Martin.x = 0
                    Martin.y = 0
                elif Bob.y - 20 <= a[1] <= Bob.y + 20 and Bob.x - 30 < a[0] <= Bob.x + 80:
                    print('Bob')
                    missile.state = 'ready'
                    missile.y = 700
                    hit = 1

# ================================================# Server connection #================================================#

        response = Server.send([[Player1Obj.x], Martin.SendCoordinates(), hit], pick=True)
        print(response)

        Bob.x = response[1][0]
        Bob.y = response[1][1]
        Martin.x = response[2][0]
        Martin.y = response[2][1]

        main_window.blit(Bob.imgProj, (Bob.x, Bob.y))
        main_window.blit(Martin.imgProj, (Martin.x, Martin.y))

        # calling move_Player2 with the response we got from the server
        move_Player2(response[0][0])

        pygame.display.update()

        # KEY LISTENERS PART 2
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if key_listener[pygame.K_SPACE]:
                    Current_Missile_X = Player1Obj.x
                    for missile in Player1Obj.missiles:
                        if missile.state == 'ready':
                            missile.ChangeState()
                            missile.onFire(Current_Missile_X)
                            break

# ========================================================# END #======================================================#

lan_game()