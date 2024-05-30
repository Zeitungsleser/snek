import socket
import random

TCP_IP = '151.216.74.213'
TCP_PORT = 4000
BUFFER_SIZE = 1024

width = 0
height = 0
player_id = 0

posx = 0
posy = 0

covered_spaces = []

def checkDirections():
    possible_directions = [b'left', b'up', b'right', b'down']
    if posx == 0 and [width-1,posy] in covered_spaces:
        possible_directions.remove(b'left')
    if posy == 0 and [posx, height-1] in covered_spaces:
        possible_directions.remove(b'up')
    if posx == width-1 and [0,posy] in covered_spaces:
        possible_directions.remove(b'right')
    if posy == height-1 and [posx,0] in covered_spaces:
        possible_directions.remove(b'down')
    
    if posx > 0 and [posx-1,posy] in covered_spaces:
        possible_directions.remove(b'left')
    if posy > 0 and [posx, posy-1] in covered_spaces:
        possible_directions.remove(b'up')
    if posx < width-1 and [posx+1,posy] in covered_spaces:
        possible_directions.remove(b'right')
    if posy < height-1 and [posx,posy+1] in covered_spaces:
        possible_directions.remove(b'down')

    return possible_directions


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
#if not "documentation" in str(s.recv(BUFFER_SIZE)):
#    print("Komische Antwort vom Server hmmm")
f = open('pwd').read()
s.send(b'join|daddy_soeder|' + str.encode(f) + b'\n')
while True:
    msg = s.recv(BUFFER_SIZE)
    msgs = msg.split(b'\n')
    for m in msgs:
        print(m)
        if m.startswith(b'game'):
            game = m.split(b'|')
            width = int(game[1])
            height = int(game[2])
            player_id = int(game[3])
        elif m.startswith(b'pos'):
            pos = m.split(b'|')
            covered_spaces.append([int(pos[2]), int(pos[3])])
            if int(pos[1]) == player_id:
                posx = int(pos[2])
                posy = int(pos[3])
        elif m.startswith(b'tick'):
            possible_directions = checkDirections()
            if possible_directions != []:
                s.send(b'move|' + random.choice(possible_directions) + b'\n')
            else:
                s.send(b'move|left\n')
            print('MOVE SENDED')
        elif m.startswith(b'lose') or m.startswith (b'win'):
            alive = False
