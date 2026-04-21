# Author: Zachary Fields
# GitHub username: ruy223
# Date: 11/03/26
# Description: Abstract animal board game,
             # in this game there two players on a 7x7 board. Each player controls
             # 4 defined animal pieces that can move a specific number of square
             # in a diagonal or orthogonal direction. If the players "Beluga" is captured they lose the match


#### Pieces and the related classes ###

class Piece:
    """
    Base class for all pieces.
    """
    def __init__(self, color, position):
        """
        Initializes a Piece with its movement attributes.

        """
        self._color = color
        self._position = position

    def get_color(self):
        """
        Returns the color of the piece.

        """
        return self._color

    def get_position(self):
        """
        Returns the position of the piece.
        """
        return self._position

    def set_position(self, position):
        """
        Updates the position of the piece.
        """
        self._position = position


    def is_beluga(self):
        """
        Returns False if not a Beluga piece
        """
        return False


    def get_legal_moves(self, board):
        """
        Returns an empty list of legal moves. Should be overridden by subclasses.
        """
    def _orthogonal_offsets(self):
        """
        returns the 4 orthogonal directions
        """
        move_list = []
        move_list.append((0, 1))
        move_list.append((0, -1))
        move_list.append((-1, 0))
        move_list.append((1, 0))
        return move_list

    def _diagonal_offsets(self):
        """
        returns the 4 diagonal directions
        """
        diagonal_list = []
        diagonal_list.append((-1, 1))
        diagonal_list.append((1, 1))
        diagonal_list.append((1, -1))
        diagonal_list.append((-1, -1))
        return diagonal_list

    def _in_bounds(self, row, col):
        """
        Checks if the piece is within in the 7x7 grid
        """
        return 0 <= row < 7 and 0 <= col < 7


    def _sliding_moves(self, directions, distance, board):
        """
         Generates legal sliding moves given directions and max distance
        """
        sliding_list = []
        col, row = self._position
        for direction in directions:
            for i in range(1, distance + 1):
                colDelta3, rowDelta3 = direction
                colNew = (colDelta3 * i) + col
                rowNew = (rowDelta3 * i) + row

                if not self._in_bounds(rowNew, colNew):
                    break   # stops loop if it goes off board

                if board[rowNew][colNew] == None:
                    sliding_list.append((colNew, rowNew))

                ## Capture enemy piece
                elif self._color != board[rowNew][colNew].get_color():
                    sliding_list.append((colNew, rowNew))
                    break
                ## Same team, skip them
                else:
                    break
        return sliding_list


    def _jumping_moves(self, directions, distance, board):
        """
        Generates legal jumping moves given directions and max distance
        """
        jumping_list = []
        col, row = self._position
        for direction in directions:
            colDelta2, rowDelta2 = direction
            colNew = (colDelta2 * distance) + col
            rowNew = (rowDelta2 * distance) + row

            # Skip
            if not self._in_bounds(rowNew, colNew):
                continue

            #
            if board[rowNew][colNew] == None:
                jumping_list.append((colNew, rowNew))

            elif self._color != board[rowNew][colNew].get_color():
                jumping_list.append((colNew, rowNew))

        return jumping_list


    def _one_square_alt_moves(self, directions, board):
        """
        Generates legal one-square alt moves
        """
        valid_move_list = []
        col, row = self._position
        for direction in directions:
            colDelta, rowDelta = direction
            colNew = col + colDelta
            rowNew = row + rowDelta

            # # skip if off the board
            if not self._in_bounds(rowNew, colNew):
                continue

            ## if square is empty, move is legal
            if board[rowNew] [colNew] == None:
                valid_move_list.append((colNew, rowNew))

            elif self._color != board[rowNew][colNew].get_color():
                valid_move_list.append((colNew, rowNew))

        return valid_move_list # return all legal moves

### Individual pieces

class Pika(Piece):
    """
    Represents the Pika (orthogonal, sliding, distance 4)

    """

    def __init__(self, color, position ):
        """
        Initializes a Pika piece for the given player color.

        """
        super().__init__(color, position)

    def get_legal_moves(self, board):
        """
        control pika's legal moves
        """
        moves_orthogonal = self._sliding_moves(self._orthogonal_offsets(), 4, board)
        moves_diagonal = self._one_square_alt_moves(self._diagonal_offsets(), board)
        move_both = moves_orthogonal + moves_diagonal
        return move_both


class Trilobite(Piece):
    """
    Represents the Trilobite piece (diagonal, sliding, distance 2)

    """

    def __init__(self, color, position):
        """
        Initializes a Trilobite piece for the given player color.

        """
        super().__init__(color, position)


    def get_legal_moves(self, board):
        """
        Controls Trilobite's legal moves
        """
        moves_diagonal = self._sliding_moves(self._diagonal_offsets(), 2, board)
        moves_orthogonal = self._one_square_alt_moves(self._orthogonal_offsets(), board)
        move_both = moves_diagonal + moves_orthogonal
        return move_both

class Wombat(Piece):
    """
    Represents the Wombat piece (orthogonal, jumping, distance 1)

    """

    def __init__(self, color, position):
        """
        Initializes a Wombat piece for the given player color.

         """
        super().__init__(color, position) #call parent class with super().


    def get_legal_moves(self, board):
        """
        Controls Wombat piece's legal moves
        """
        moves_orthogonal = self._one_square_alt_moves(self._orthogonal_offsets(), board)
        moves_diagonal = self._one_square_alt_moves(self._diagonal_offsets(), board)
        move_both = moves_orthogonal + moves_diagonal
        return move_both


class Beluga(Piece):
    """
    Represents the Beluga piece (diagonal, jumping, distance 3)

    """

    def __init__(self, color, position):
        """
        Initializes a Beluga piece for the given player color.

        """
        super().__init__(color, position)

    def get_legal_moves(self, board):
        """
        Controls Beluga's legal moves
        """
        moves_diagonal = self._jumping_moves(self._diagonal_offsets(), 3, board)
        moves_orthogonal = self._one_square_alt_moves(self._orthogonal_offsets(), board)
        move_both = moves_diagonal + moves_orthogonal
        return move_both

    def is_beluga(self):
        """
        This be Beluga
        """
        return True

### Basic control classes for player ###

class AnimalGame:
    """
    Manages the overall state of an AnimalGame match on a 7x7 board.
    """
    def __init__(self):
        """
        Initializes the game and generate 7x7 board
        """
        self._board = [[None] * 7 for _ in range(7)] #empty 7x7 grid, 7 lists of 7 None's
        self._turn = "tangerine"
        self._game_state = "UNFINISHED"
        self._setup_board ()

    def _col_to_index(self, col_chars):
        """
        Converts a column into an index
        """
        col_index_dict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6}
        return col_index_dict[col_chars]

    def _row_to_index(self, row_chars):
        """
        Converts a row into an index
        """
        row_index_dict = {"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6}
        return row_index_dict[row_chars]

    def _notation_to_position(self, notation):
        """
        Converts algebraic notation like 'd4' into a (col, row) tuple
        """
        col = self._col_to_index(notation[0])
        row = self._row_to_index(notation[1])
        return col, row

    def _setup_board(self):
        """
        Places all pieces in their starting positions.
        Tangerine pieces go in row 1 (index 0) and amethyst pieces go in row 7 (index 6).
        """
        piece_order = [Pika, Trilobite, Wombat, Beluga, Wombat, Trilobite, Pika]  #pieces order according to isntructions
        for col in range(7):
            self._board[0][col] = piece_order[col]('tangerine', (col, 0))
            self._board[6][col] = piece_order[col]('amethyst', (col, 6))   #opposite side of the board

    def get_game_state(self):
        """
        Returns the current game state.

        """
        return self._game_state

    def make_move(self, from_square, to_square):
        """
        Makes a move.
        """
        if self._game_state != "UNFINISHED":   # Is the game already over?
            return False

        from_col, from_row = self._notation_to_position(from_square)  # convert from algebraic notation
        to_col, to_row = self._notation_to_position(to_square)

        # access peice on the board
        piece = self._board[from_row][from_col]
        if piece is None:
            return False
        if piece.get_color() != self._turn:
            return False

        # check if the move is actually lega
        legal_moves = piece.get_legal_moves(self._board)
        if (to_col, to_row) not in legal_moves:
            return False

        # Execute the move
        execute_move = self._board[to_row][to_col]
        self._board[to_row][to_col] = piece
        self._board[from_row][from_col] = None

        # update piece position
        piece.set_position((to_col, to_row))

        # Is Beluga capture?
        if execute_move is not None:
            if execute_move.is_beluga():
                if execute_move.get_color() == 'tangerine':
                    self._game_state = "AMETHYST_WON"
                else:
                    self._game_state = "TANGERINE_WON"

        # Switch player turns
        if self._turn == "tangerine":
            self._turn = "amethyst"
        else:
            self._turn = "tangerine"

        return True

# Test
#game = AnimalGame()

#print(game.make_move('a1', 'a4'))  # True
#print(game.make_move('a1', 'a4'))  # False - not your turn
#print(game.make_move('a7', 'a5'))  # True
#print(game.make_move('a4', 'a5'))  # True - capture
#print(game.get_game_state())       # UNFINISHED

# Win the game
#game2 = AnimalGame()
#game2.make_move('d1', 'g4')
#game2.make_move('a7', 'a6')
#game2.make_move('g4', 'd7')        # capture amethyst beluga
#print(game2.get_game_state())      # TANGERINE_WON
