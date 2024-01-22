# Team A: Rithwik Bhardwaj (117687224), Tibor Mester (117977318), Henry
import numpy as np


def main():
    # holding the layout of the board
    # 0 = Empty
    # 1 = Your Side
    # 2 = Opponent
    # inf = Padding
    board = read_board()

    play_best_move(board)


# read the standard in to create np array board
# 0 = Empty
# 1 = Your Side
# 2 = Opponent
# inf = Padding
def read_board():
    board = np.zeros((8, 14))

    # Get input reversi board
    for i in range(8):
        # check if full width board
        if i == 3 or i == 4:
            board[i] = np.array(list(map(int, str(input()).split(" "))))

        # pad top of board
        elif i < 3:
            padd = 3 - i
            # add padding to both ends of row
            board[i] = np.concatenate(
                [
                    np.full((1, padd), np.inf).flatten(),
                    np.array(list(map(int, str(input()).split(" ")))),
                    np.full((1, padd), np.inf).flatten(),
                ]
            )

        # pad bottom of board
        else:
            padd = i % 4
            # add padding to both ends of row
            board[i] = np.concatenate(
                [
                    np.full((1, padd), np.inf).flatten(),
                    np.array(list(map(int, str(input()).split(" ")))),
                    np.full((1, padd), np.inf).flatten(),
                ]
            )

    return board


# returns tuple of (my score, opponeents score)
def get_score(board):
    return np.count_nonzero(board == 1), np.count_nonzero(board == 2)


# given the board and a cell determine if the cell is a valid move
# valid moves need to be next to sandwiched an opponent's piece
# diagonals not implemented yet

##I don't think the horizontal or vertical checking is ideal since it finds the first of our pieces and checks that the rest of the pieces are theres until our location
#In the case that a row is 1 1 2 2 0, this would mark the 0 spot as invalid despite being valid
#instead, I think the best way to check all directions at once is to check from our spot along a line of other team's pieces until we reach either our piece, padding, or the edge
def test_line(board, row : int, col : int, delta_row : int = 0, delta_col : int = 0, acc : int = 0)-> int:
    #check if we have exceeded the bounds of the board, then this isn't a sandwich so we return zero
    if row < 0 or row >= board.shape[0] or col < 0 or col >= board.shape[1]:
        return 0
    #also if the spot isn't taken or is inf, we have a line but no sandwich so we return 0
    elif  board[row,col] == 0 or board[row,col] == np.inf:
        return 0
    #The base case is that we have reached another of our pieces and return the #of sandwhiched pieces
    #note that two adjacent pieces return a line of length 0 so that would be an invalid move
    elif board[row,col] == 1:
        return acc
    #if it is a line, keep testing along the same direction, noting that we are flipping one tile
    elif board[row,col] == 2:
        return test_line(board, row + delta_row, col + delta_col, delta_row, delta_col, acc + 1)
    #should probably never reach this point
    return acc

#gets the number of pieces flipped by the move, if this is greater than 0 it is a valid move
def is_valid_move(board, row : int, col : int):
    #Note that this tests for rays in all 8 directions from the point, all we requires is a single positive result
    #Negative values are not possible
    return (test_line(board, row + 1, col + 1, 1, 1) + #right up
               test_line(board, row - 1, col + 1, -1, 1) + #left up
               test_line(board, row - 1, col - 1, -1, -1) + #down left
               test_line(board, row + 1, col - 1, 1, -1) + #down right
               test_line(board, row, col - 1, 0, -1) + #down
               test_line(board, row, col + 1, 0, 1) + #up
               test_line(board, row - 1, col, -1, 0) + #left
               test_line(board, row + 1, col, 1, 0))# Right

# Plays first available move
def play_first_move(board):
    rows, cols = board.shape
    # Nothing is played, go in center
    if np.all((board == 0) | (board == np.inf)):
        print(f"{rows // 2} {cols // 2}")
        return 0
    for i in range(rows):
        for j in range(cols):
            if board[i,j] == 0 :
                if is_valid_move(board, i, j) > 0:
                    print(f"{i + 1} {j + 1}")
                    return 0
            
#iterates through all the spaces, checking for #tiles flipped, 
def play_best_move(board):
    best_value = 0
    best_row = -1
    best_col = -1
    rows, cols = board.shape
    for row in range(rows):
        for col in range(cols):
            if board[row,col] == 0 :
                value = is_valid_move(board, row, col)
                #TODO: Implement code to prioritize (add value) to securing a corner that can't be flipped back
                if value > best_value :
                    best_value = value
                    best_row = row
                    best_col = col
    #incase nothing is valid we don't want to throw errors
    if best_row != -1 and best_col != -1:
        
        #need to unpad the row and column, basically the row is the same, but based on the row the column needs to be shrunk
        # check if full width board
        padd : int
        if best_row == 3 or best_row == 4:
            padd = 0
            
        # pad top of board
        elif best_row < 3:
            padd = 3 - best_row
        # pad bottom of board
        else:
            padd = best_row % 4
        #apply the padding to the column
        best_col -= padd
        print(f"{best_row + 1} {best_col + 1}")
    return 0


if __name__ == "__main__":
    main()
