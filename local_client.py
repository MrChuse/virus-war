from core import TheGame
import argparse
def print_help():
    print('To play, write the command into the console')
    print('List of commands:')
    print('help - print this message')
    print('show - show the field again')
    print('place coord_x coord_y - place your virus to place (coord_x, coord_y)')
    print('kill coord_x, coord_y - kill an enemy in place (coord_x, coord_y)')
    print('pass - pass your turn')

parser = argparse.ArgumentParser(description='virus war - small strategy paper game')
parser.add_argument('--field-width', type=int, default=10, help='width of the standart field (default: 10)')
parser.add_argument('--players-number', type=int, default=2, choices=[2, 4], help='number of players: 2 or 4 (default: 2)')
args = parser.parse_args()

g = TheGame()
players = (1, 2)
turn = 0
print('to get help enter "help"')
g.show()
while not g.is_over():
    inp = input(f'Player {players[0]}, enter your move:').split()
    if inp[0] == 'help':
        print_help()
        continue
    elif inp[0] == 'show':
        g.show()
        continue
    elif inp[0] == 'end' or inp[0] == 'break' or inp[0] == 'exit':
        break
    else:
        move, rest = inp[0], list(map(int, inp[1:]))
    if move == 'place':
        move = 0
    elif move == 'kill':
        move = 1
    elif move == 'pass':
        move = 2
    try:
        g.make_a_move(players[0], (move, rest))
    except Exception as e:
        print(e)
    else:
        if move == 2:
            turn = 3
        else:
            turn += 1
    g.show()
    if turn == 3:
        players = (players[1], players[0])
        turn = 0

else:
    winner = g.winner()
    if winner == -1:
        print('Draw!')
    else:
        print('Player', winner, 'won')
