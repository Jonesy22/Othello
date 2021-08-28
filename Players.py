'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import math
MAX_VALUE = math.inf

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
       

    def is_terminal_state(self, board):
        if (board.has_legal_moves_remaining('X') == False) and (board.has_legal_moves_remaining('O') == False):
            return True
        return False

    def utility(self, board):
        return board.count_score(self.oppSym) - board.count_score(self.symbol)


    
    def getSuccessors(self, board, symbol):
        successors = []
        rows = 4
        cols = 4
        for row in range(rows):
            for col in range(cols):
                if board.is_legal_move(col, row, symbol):
                    successors.append((col, row))
        return successors

    def max_value(self,board):
        if self.is_terminal_state(board):
            return self.utility(board)

        best_move = []
        v = -MAX_VALUE
        successors = self.getSuccessors(board, self.oppSym)
        if not successors:
            utility_value = max(v, self.min_value(board))
            v = utility_value

        else:
            for best_move in successors:
                newBoard = board.cloneOBoard()
                newBoard.play_move(best_move[0], best_move[1], self.oppSym)
                utility_value = max(v, self.min_value(newBoard))
                v = utility_value
        return v
        
    def min_value(self,board):
        if self.is_terminal_state(board):
            return self.utility(board) 
            
        best_move = []
        v = MAX_VALUE
        successors = self.getSuccessors(board, self.symbol)
        if not successors:
            utility_value = min(v, self.max_value(board))
            v = utility_value

        else:
            for best_move in successors:
                newBoard = board.cloneOBoard()
                newBoard.play_move(best_move[0], best_move[1], self.symbol)
                utility_value = min(v, self.max_value(newBoard))
                v = utility_value
        return v
       


    def minimax_decision(self, board):
        successors = self.getSuccessors(board, self.symbol)
        best_move = []
        maximum = MAX_VALUE
        for best_move in successors:
            newBoard = board.cloneOBoard()
            newBoard.play_move(best_move[0], best_move[1], self.symbol)
            utility = self.max_value(newBoard)
            if utility < maximum:
                maximum = utility
                optimal = best_move

        return optimal
    
    def get_move(self,board):
        return self.minimax_decision(board)