from config import *


class Manager:

    def __init__(self, surface):
        self.surface = surface
        self.boards = []
        self.set_up()
        self.once = True

    def set_up(self):
        board = Board(self, [], [])
        row = 0
        number_in_row = 1
        while row <= 4:
            place = 0
            board.board.append([])
            for i in range(number_in_row):
                slot = Slot(self, row, place)
                place += 1
                board.board[row].append(slot)
            row += 1
            number_in_row += 1
        board.board[0][0].remove()
        board.pegs -= 1
        print "first board:"
        print board
        self.boards.append(board)

    def jump(self):
        for board in self.boards:
            for row in board.board:
                # jumping left and right
                if len(row) >= 3:
                    for slot in row:
                        if slot.has_peg:
                            # to the right
                            if slot.place <= len(row)-3 and row[slot.place+1].has_peg and not row[slot.place+2].has_peg:
                                thing = Board(self, board.board, board.move_list)
                                thing.jump(1, slot)
                                self.boards.append(thing)
                                board.has_move = True
                            # to the left
                            if slot.place >= 2 and row[slot.place-1].has_peg and not row[slot.place-2].has_peg:
                                thing = Board(self, board.board, board.move_list)
                                thing.jump(2, slot)
                                self.boards.append(thing)
                                board.has_move = True
                # jumping down
                if len(row) <= 3:
                    for slot in row:
                        if slot.has_peg:
                            # down to the left
                            if board.board[slot.row+1][slot.place].has_peg and not board.board[slot.row+2][slot.place].has_peg:
                                thing = Board(self, board.board, board.move_list)
                                thing.jump(3, slot)
                                self.boards.append(thing)
                                board.has_move = True
                            # down to the right
                            if board.board[slot.row+1][slot.place+1].has_peg and not board.board[slot.row+2][slot.place+2].has_peg:
                                thing = Board(self, board.board, board.move_list)
                                thing.jump(4, slot)
                                self.boards.append(thing)
                                board.has_move = True
                # jumping up
                if len(row) >= 3:
                    for slot in row:
                        if slot.has_peg:
                            # up to the left
                            if slot.place >= 2:
                                if board.board[slot.row-1][slot.place-1].has_peg and not board.board[slot.row-2][slot.place-2].has_peg:
                                    thing = Board(self, board.board, board.move_list)
                                    thing.jump(5, slot)
                                    self.boards.append(thing)
                                    board.has_move = True
                            # up to the right
                            if slot.place <= slot.row-2:
                                if board.board[slot.row-1][slot.place].has_peg and not board.board[slot.row-2][slot.place].has_peg:
                                    print "Making move 6"
                                    print "old board: "
                                    print board
                                    thing = Board(self, board.board, board.move_list)
                                    thing.jump(6, slot)
                                    self.boards.append(thing)
                                    board.has_move = True
                                    print "new board: "
                                    print thing

            if not board.has_move:
                board.finish()
            self.boards.remove(board)

    def update(self):
        self.jump()
        if len(self.boards) == 0:
            sys.exit(0)


class Board:

    def __init__(self, manager, board, moves):
        self.manager = manager
        self.board = []
        self.pegs = 0
        self.has_move = False
        self.move_list = moves
        self.set_up(board)

    def __str__(self):
        string = ""
        string += str(self.board[0][0].has_peg)
        for row in self.board:
            for col in row:
                string += " " + str(col.has_peg)
            string += ","
        return string

    def jump(self, move, slot):
        if move == 1:
            slot.move(self.board[slot.row][slot.place + 1], self.board[slot.row][slot.place + 2])
        elif move == 2:
            slot.move(self.board[slot.row][slot.place - 1], self.board[slot.row][slot.place - 2])
        elif move == 3:
            slot.move(self.board[slot.row + 1][slot.place], self.board[slot.row + 2][slot.place])
        elif move == 4:
            slot.move(self.board[slot.row + 1][slot.place + 1], self.board[slot.row + 2][slot.place + 2])
        elif move == 5:
            slot.move(self.board[slot.row - 1][slot.place - 1], self.board[slot.row - 2][slot.place - 2])
        elif move == 6:
            slot.move(self.board[slot.row - 1][slot.place], self.board[slot.row - 2][slot.place])

        self.pegs -= 1
        row = slot.row
        place = slot.place
        string = ((row, place), move)
        self.move_list.append(string)

    def finish(self):
        if self.pegs == 2:
            string = "end, pegs left:" + str(self.pegs)
            self.move_list.append(string)
            print self.move_list

    def set_up(self, board):
        row = 0
        place = 0
        for array in board:
            self.board.append([])
            for slot in array:
                self.board[row].append(Slot(self.manager, row, place))
                self.pegs += 1
                if not slot.has_peg:
                    self.board[row][place].remove()
                    self.pegs -= 1
                place += 1
            row += 1
            place = 0


class Slot:

    def __init__(self, manager, row, place):
        self.manager = manager
        self.row = row
        self.place = place
        self.has_peg = True

    def remove(self):
        self.has_peg = False

    def add_peg(self):
        self.has_peg = True

    def move(self, jumped, end):
        self.remove()
        jumped.remove()
        end.add_peg()
