from core import TheGame

g = TheGame()
players = (1, 2)
turn = 0
g.show()
while not g.is_over():
    move, x, y = map(int, input(f'Player {players[0]}, enter your move:').split())
    try:
        g.make_a_move(players[0], (move, (x, y)))
    except Exception as e:
        print(e)
    else:
        turn += 1
    g.show()
    if turn == 3:
        players = (players[1], players[0])
        turn = 0
