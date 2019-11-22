from core import TheGame

g = TheGame()
players = (1, 2)
turn = 0
g.show()
while not g.is_over():
    inp = input(f'Player {players[0]}, enter your move:').split()
    if inp[0] == 'pass':
        move = 2
        x = 0
        y = 0
    else:
        move, x, y = inp
    if move == 'place':
        move = 0
    elif move == 'kill':
        move = 1
    elif move == 'pass':
        move = 2
    x, y = int(x), int(y)
    try:
        g.make_a_move(players[0], (move, (x, y)))
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
winner = g.winner()
if winner == -1:
    print('Draw!')
else:
    print('Player', winner, 'won')
