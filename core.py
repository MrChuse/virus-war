class NotYourTurnError(RuntimeError):
    pass

class InvalidMoveError(RuntimeError):
    pass

class OutOfBoundsError(RuntimeError):
    pass

class KillWrongCellError(RuntimeError):
    pass

class CellOccupiedError(RuntimeError):
    pass

class NoNeighbourAlliesError(RuntimeError):
    pass

class move_ids:
    PLACE = 0
    KILL = 1
    PASS = 2



class Field:
    def __init__(self, players_num, field_size):
        self.field_size = field_size
        self.field = [[0]*field_size for i in range(field_size)]
        if not (players_num == 2 or players_num == 4):
            raise NotImplementedError("can't handle that number of players")
        self.field[0][0] = 1
        self.field[-1][-1] = 2
        if players_num == 4:
            self.field[0][-1] = 3
            self.field[-1][0] = 4

    def fill(self, value, coords):
        self.field[coords[0]][coords[1]] = value

    def place(self, player, coords):
        self.fill(player, coords)

    def kill(self, player, coords):
        self.fill(-player, coords)

    def out_of_bounds(self, x, y):
        return not (0 <= x < self.field_size and 0 <= y < self.field_size)

    def is_possible(self, player, move):
        move_id, coords = move
        if len(coords) != 2:
            raise TypeError('coords should be length 2')
        if self.out_of_bounds(coords[0], coords[1]):
            raise OutOfBoundsError('coords shoud be from 0 to field_size')
        #print(player)
        if move_id == move_ids.PLACE: #can place on free spots
            if self.field[coords[0]][coords[1]] == 0:
                return True
            else:
                raise CellOccupiedError('Can place only in free cells')
        elif move_id == move_ids.KILL: #cant kill dead viruses and allies
            if (self.field[coords[0]][coords[1]] <= 0 or self.field[coords[0]][coords[1]] == player):
                raise KillWrongCellError('You should kill opponents cells')
            else:
                #print('inside the Else', player, move)
                for i in (-1, 0, 1):
                    for j in (-1, 0, 1):
                        #print(f'i={i}  j={j}')
                        if not (self.out_of_bounds(coords[0] + i, coords[1] + j)):
                            if self.field[coords[0] + i][coords[1] + j] == player:
                                return True
                            #else:
                                #print(f'for player {player} False')
                        #else:
                            #print('inside the else in the prev else')
                #print('just before the raise')
                raise NoNeighbourAlliesError("can't kill cells without touching them")

                #return any([(not (self.out_of_bounds(coords[0] + i, coords[1] + j)) and self.field[coords[0] + i][coords[1] + j] == player and ) for i in (-1, 0, 1) for j in (-1, 0, 1)])
        elif move_id == move_ids.PASS: #always can pass
            return True

    def show(self):
        for row in self.field:
            print(row)

    def get_state(self, coords):
        return self.field[coords[0]][coords[1]]

class TheGame:
    def __init__(self, players_num=2, field_size=10, max_moves=3, std_field=True, field=None):
        self.players_num = players_num
        self.field_size = field_size
        self.max_moves = max_moves
        if std_field:
            self.field = Field(self.players_num, self.field_size)
        else:
            self.field = field

        self.players_turn = [1, 0]
        self.scores = [1] * (players_num + 1)

    def whose_turn(self):
        return self.players_turn[0]

    def is_possible(self, move):
        if move[0] == move_ids.PASS:
            return True
        if len(move) != 2: # if not pass, move is move_id and coords
            raise TypeError('move should be length 2')
        if not(move[0] == move_ids.PLACE or move[0] == move_ids.KILL): #move_id should exist
            raise TypeError('move_id should exist')
        #that's all what The Game cares about
        return self.field.is_possible(self.players_turn[0], move) #field class must decide here because behaviour
                                                    #can change (not only near your allies but anywhere)

    def next_player(self, move_id):
        self.players_turn[1] += 1

        if move_id == move_ids.PASS:
            self.players_turn[0] += 1
            self.players_turn[1] = 0

        if self.players_turn[1] == self.max_moves:
            self.players_turn[0] += 1
            self.players_turn[1] = 0

        if self.players_turn[0] > self.players_num:
            self.players_turn[0] = 1

    def make_a_move(self, player, move):
        if self.whose_turn() != player:
            raise NotYourTurnError('Not your turn')
        if not self.is_possible(move):
            raise InvalidMoveError('Pick a possible move') #all logic is in is_possible

        move_id, coords = move

        if move_id == move_ids.PLACE: #place a virus
            self.pass_counter = 0
            self.scores[player] += 1
            self.field.place(player, coords)
        elif move_id == move_ids.KILL: #kill a neighbour
            self.pass_counter = 0
            self.scores[self.field.get_state(coords)] -= 1
            self.field.kill(player, coords)
        elif move_id == move_ids.PASS:
            self.pass_counter += 1

        self.next_player(move_id)

    def is_over(self):
        counter = 0
        for score in self.scores[1:]:
            if score > 0:
                counter += 1
        return counter == 1

    def winner(self):
        if self.is_over():
            return max(self.scores)



    def show(self):
        self.field.show()
