from Players import *




# ==============================================# The main game loop #==============================================#

open = True
def main_game():

    global Current_Missile_X,a,b
    clock = pygame.time.Clock()
    main_window = pygame.display.set_mode((900, 900))
    move_rate = 15
    pygame.mouse.set_visible(False)


    #=====================================================# Music #=====================================================#



    pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.9)
    music_li = random.randint(1,4)
    if music_li == 1:
        pygame.mixer.music.load(r'assets\music\all star.mp3')
    elif music_li == 2:
        pygame.mixer.music.load(r'assets\music\what is love 8 bit.mp3')
    elif music_li == 3:
        pygame.mixer.music.load(r'assets\music\feel good.mp3')
    else:
        pygame.mixer.music.load(r'assets\music\remove.mp3')

    pygame.mixer.music.play(0)

#==============================================# Objects and images #===============================================#

    # Objects
    Player1Obj = Players(450, 750, 100, r'assets\player 1\player1.png', 58, 61)

    # Images
    backgroundIMG = pygame.image.load(r'assets\main background.png')            # Loading the image before the loop is a must in regards to FPS
    twoLives = pygame.image.load(r'assets\lives\2 lives.png')
    oneLife = pygame.image.load(r'assets\lives\1 life.png')
    zeroLives = pygame.image.load(r'assets\lives\0 lives.png')

#==========================================# Loops for spawning objects #===========================================#

    enemies = []
    for i in range(8): # put 8 here
        mob = Enemy()
        enemies.append(mob)

    for i in range(10):
        Missiles = Missile(Player1Obj, main_window)
        Player1Obj.missiles.append(Missiles)



#==============================================# Main game #==============================================#

    while open:

#============================================# Taking lives awae #==================================================#



        if Player1Obj.lives == 3:
            main_window.blit(backgroundIMG, (0, 0))
        if Player1Obj.lives == 2:
            main_window.blit(twoLives, (0, 0))
        if Player1Obj.lives == 1:
            main_window.blit(oneLife, (0, 0))
        if Player1Obj.lives == 0:
            main_window.blit(zeroLives, (0, 0))
        if Player1Obj.lives < 0:
            main_window.blit(zeroLives, (0, 0))  # put pygame.quit() after done with testing
            pygame.time.wait(1000)
            pygame.quit()

#=============================================# Key Listeners #=====================================================#

        key_listener = pygame.key.get_pressed()
        if (key_listener[pygame.K_LEFT] or key_listener[pygame.K_a]) and Player1Obj.x > 30:
            Player1Obj.x -= move_rate

        elif (key_listener[pygame.K_RIGHT] or key_listener[pygame.K_d]) and Player1Obj.x < 855:
            Player1Obj.x += move_rate

#============================================# Blitting images #====================================================#

        main_window.blit(Player1Obj.imgP1, (Player1Obj.x - 20, Player1Obj.y))

        textSurface = pygame.font.SysFont('comicsansms', 28).render(str(Player1Obj.score), True, (255, 255, 255))
        main_window.blit(textSurface, (100,50))




#===========================================# Updating enemies #====================================================#

        for enemy in enemies:
            main_window.blit(enemy.imgProj, (enemy.x, enemy.y))
            enemy.Update(Player1Obj)

#===========================================# Updating missile #====================================================#

        for missile in Player1Obj.missiles:
            if missile.state == 'shot':
                missile.shoot()

# ==============================================# Collision #=======================================================#

        for missile in Player1Obj.missiles:
            a = missile.getCoords()
            if a == None:
                pass
            if a == None:
                pass
            else:
                for enemy in enemies:
                    b = enemy.SendCoordinates()
                    if missile.state == 'ready':
                        break
                    if b[1] - 20 <= a[1] <= b[1] + 20 and b[0] - 30 < a[0] <= b[0] + 80:
                        missile.y = 700
                        missile.state = 'ready'
                        enemy.y = random.randint(-1000, 0)
                        Player1Obj.Increase_Score()
                    else:
                        pass


# ==============================================# Space input, shoot #==============================================#

        pygame.display.update()


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


#=================================================#      End      #=================================================#