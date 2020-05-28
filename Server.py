import socket
from _thread import *
import _pickle as PICKLE_RICK
import random

# ===============================================# Server establishment #==============================================#

Soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# The custom port
port = 50007

# The host and the ip of the host
host = socket.gethostname()
ip = socket.gethostbyname(host)

# Trying out to see whehter can start or not
try:
    Soket.bind((ip, port))
except socket.error as e:
    print(str(e))
    print('Server could not start')
    quit()

# Open socket on port 50007 listening
Soket.listen(2) # Listening for 2 connections

# Connections and ids of the incoming connections
_id = 0
connections = 0

print(f'Started server with ip {ip}')


# ========================================# Variables accessed by both threads #=======================================#

Player1_Enemies = [0,0]
Player2_Enemies = [0,0]
Players = []
li1 = []
li2 = []
Change1 = False
Change2 = False

# ========================================# The methods for both threads #=============================================#

def Player_Coords(id, x_position):
    if id == 0:
        li1.append(x_position)
        if len(li1) > 1:
            li1.remove(li1[0])
        if li2 == []:
            return 1000
        else:
            return li2[0]
    elif id == 1:
        li2.append(x_position)
        if len(li2) > 1:
            li2.remove(li2[0])
        if li1 == []:
            return 1000
        else:
            return li1[0]
    else:
        return None

def Update_Enemy(x, y):
    if x == 0 and y == 0:
        x = random.randint(46,900 - 46)
        y = random.randint(-1000, 0)
    speed = random.randint(5,10)
    y += speed
    if y > 900:
        y = 0
        x = random.randint(46,900 - 46)
    return([x,y])

# ======================================# Establishing threads for connections #=======================================#

def threaded_connection(conn, _id):

    # Defining global variables

    global connections, players, Change1, Change2

    # Recieving data

    data = conn.recv(1080)
    name = data.decode('utf-8')
    print(f'{name} connected to the server')
    Players.append(conn)

    # The thread connection
    while True:
        data = conn.recv(32)
        if not data:
            break

        # Data receieved from the thread
        data = PICKLE_RICK.loads(data)

        # if id 0
        if _id == 0:
            Player_coords = [Player_Coords(_id, data[0][0])]
            if Change1 == True:
                Update = Update_Enemy(0,0)
                Player1_Enemies[0] = Update[0]
                Player1_Enemies[1] = Update[1]
                Change1 = False
            else:
                Update = Update_Enemy(data[1][0], data[1][1])
                Player1_Enemies[0] = Update[0]
                Player1_Enemies[1] = Update[1]
                if data[2] == 1:
                    print('Enemy 2 hit')
                    Change2 = True

            #sending reply back to thread id 0
            conn.send(PICKLE_RICK.dumps([Player_coords, Player1_Enemies, Player2_Enemies]))

        # if id = 1
        elif _id == 1:
            Player_coords = [Player_Coords(_id, data[0][0])]
            if Change2 == True:
                Update = Update_Enemy(0, 0)
                Player2_Enemies[0] = Update[0]
                Player2_Enemies[1] = Update[1]
                Change2 = False
            else:
                Update = Update_Enemy(data[1][0], data[1][1])
                Player2_Enemies[0] = Update[0]
                Player2_Enemies[1] = Update[1]
                if data[2] == 1:
                    print('Enemy 1 hit')
                    Change1 = True

            # sending reply back to thread id 1
            conn.send(PICKLE_RICK.dumps([Player_coords, Player1_Enemies, Player2_Enemies]))

        #else send 1000 which does nothing
        else:
            conn.send(str.encode(str(1000)))


# ==============================================# The server loop #====================================================#
while True:

    # accepting host and address
    host, addr = Soket.accept()
    print("[CONNECTION] Connected to:", addr)

    # increment connections start new thread then increment ids
    connections += 1
    host.send(b'Welcome to the server')

    # creating a new thread on the server
    start_new_thread(threaded_connection, (host, _id))
    _id += 1


# ====================================================# END #==========================================================#

