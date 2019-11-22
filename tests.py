#!py

import unittest
from core import TheGame, Field, InvalidMoveError, OutOfBoundsError, CellOccupiedError, KillWrongCellError, NoNeighbourAlliesError


class CoreTest(unittest.TestCase):

    def test_invalid_init(self):
        with self.assertRaises(NotImplementedError):
            TheGame(3, 18)

    def test_valid_init(self):
        TheGame()
        TheGame(4, 10)
        TheGame(2, 15)

    def test_invalid_move(self):
        g = TheGame()

    def test_next_player(self):
        g = TheGame()
        self.assertEqual([1, 0], g.players_turn)

        g.next_player(0)
        self.assertEqual([1, 1], g.players_turn)
        g.next_player(0)
        self.assertEqual([1, 2], g.players_turn)
        g.next_player(0)
        self.assertEqual([2, 0], g.players_turn)

        g.next_player(0)
        self.assertEqual([2, 1], g.players_turn)
        g.next_player(0)
        self.assertEqual([2, 2], g.players_turn)
        g.next_player(0)
        self.assertEqual([1, 0], g.players_turn)

        g.next_player(1)
        self.assertEqual([1, 1], g.players_turn)
        g.next_player(1)
        self.assertEqual([1, 2], g.players_turn)
        g.next_player(1)
        self.assertEqual([2, 0], g.players_turn)

        g.next_player(1)
        self.assertEqual([2, 1], g.players_turn)
        g.next_player(1)
        self.assertEqual([2, 2], g.players_turn)
        g.next_player(1)
        self.assertEqual([1, 0], g.players_turn)

        g.next_player(2)
        self.assertEqual([2, 0], g.players_turn)
        g.next_player(2)
        self.assertEqual([1, 0], g.players_turn)
        g.next_player(2)
        self.assertEqual([2, 0], g.players_turn)

    def test_move(self):
        g = TheGame(2, 2)
        g.make_a_move(1, (0, (0, 1)))
        g.make_a_move(1, (0, (1, 0)))
        with self.assertRaises(CellOccupiedError):
            g.make_a_move(1, (0, (1, 1)))
        g.make_a_move(1, (1, (1, 1)))

class FieldTest(unittest.TestCase):

    def test_field_init(self):
        f = Field(2, 2)
        self.assertEqual([[1, 0], [0, 2]], f.field)
        f = Field(2, 3)
        self.assertEqual([[1, 0, 0],
                          [0, 0, 0],
                          [0, 0, 2]],
                         f.field
        )
        f = Field(4, 2)
        self.assertEqual([[1, 3], [4, 2]], f.field)
        f = Field(4, 3)
        self.assertEqual([[1, 0, 3],
                          [0, 0, 0],
                          [4, 0, 2]],
                         f.field
        )

    def test_field_place(self):
        f = Field(2, 3)
        f.place(1, (0, 1))
        self.assertEqual([[1, 1, 0],
                          [0, 0, 0],
                          [0, 0, 2]],
                         f.field
        )
        f.place(2, (2, 1))
        self.assertEqual([[1, 1, 0],
                          [0, 0, 0],
                          [0, 2, 2]],
                         f.field
        )

    def test_field_kill(self):
        f = Field(2, 3)
        f.kill(1, (0, 1))
        self.assertEqual([[1, -1, 0],
                          [0, 0, 0],
                          [0, 0, 2]],
                         f.field
        )
        f.kill(2, (2, 1))
        self.assertEqual([[1, -1, 0],
                          [0, 0, 0],
                          [0, -2, 2]],
                         f.field
        )

    def test_field_is_possible(self):
        f = Field(2, 3)
        f.place(1, (0, 1))
        self.assertEqual([[1, 1, 0],
                          [0, 0, 0],
                          [0, 0, 2]],
                         f.field
        )
        f.kill(2, (2, 1))
        self.assertEqual([[1, 1, 0],
                          [0, 0, 0],
                          [0, -2, 2]],
                         f.field
        )


        with self.assertRaises(TypeError):
            f.is_possible(1, (0, (-1, 1, 5)))
        with self.assertRaises(OutOfBoundsError):
            f.is_possible(1, (0, (-1, 4)))
        with self.assertRaises(OutOfBoundsError):
            f.is_possible(1, (0, (3, 1)))
        with self.assertRaises(OutOfBoundsError):
            f.is_possible(2, (1, (-1, 2)))
        with self.assertRaises(OutOfBoundsError):
            f.is_possible(2, (1, (0, 3)))

        self.assertTrue(f.is_possible(1, (0, (0, 2))))
        self.assertTrue(f.is_possible(2, (0, (0, 2))))
        self.assertTrue(f.is_possible(1, (0, (1, 2))))
        self.assertTrue(f.is_possible(2, (0, (1, 2))))

        with self.assertRaises(CellOccupiedError):
            f.is_possible(1, (0, (0, 0)))
        with self.assertRaises(CellOccupiedError):
            f.is_possible(2, (0, (0, 0)))
        with self.assertRaises(CellOccupiedError):
            f.is_possible(1, (0, (2, 1)))
        with self.assertRaises(CellOccupiedError):
            f.is_possible(2, (0, (2, 1)))

        f.place(1, (1, 1))
        self.assertEqual([[1, 1, 0],
                          [0, 1, 0],
                          [0, -2, 2]],
                         f.field
        )

        with self.assertRaises(KillWrongCellError):
            f.is_possible(1, (1, (0, 2)))
        with self.assertRaises(KillWrongCellError):
            f.is_possible(2, (1, (0, 2)))
        with self.assertRaises(KillWrongCellError):
            f.is_possible(1, (1, (1, 1)))
        with self.assertRaises(KillWrongCellError):
            f.is_possible(1, (1, (0, 0)))
        with self.assertRaises(NoNeighbourAlliesError):
            self.assertFalse(f.is_possible(2, (1, (0, 0))))
        with self.assertRaises(KillWrongCellError):
            f.is_possible(1, (1, (2, 1)))
        with self.assertRaises(KillWrongCellError):
            f.is_possible(2, (1, (2, 1)))

        self.assertTrue(f.is_possible(2, (1, (1, 1))))

if __name__ == '__main__':
    unittest.main()
