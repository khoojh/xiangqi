# -*- coding: utf-8 -*-

"""

Created on Sat May  6 20:14:57 2017



@author: khoojinghwan

"""



#import piece



"""

Every time a player makes a move, the instruction is first passed through

the referee function (see bottom).

    - Instruction is in the form: piece moved, new location



The referee function:

- Prevents a player from moving opponent's pieces

- Prevents captured pieces from being moved

- Prevents pieces from moving off the board

- Prevents a piece from capturing an ally piece

- Detects when the game is over (general is captured) (or one when player surrenders??)



- Prevent pieces from making certain moves when other pieces are in the way

    - This is done using scanner functions.

    - Pieces with scanner functions are pieces the movement of which is dependent

      on other pieces (eg soldier is free to move forward, but elephant isn't if

      something's in the way. So, elephant needs a scanner function.)

    - Scanner function works by going through possible_moves and eliminating

      invalid ones

    - eg in possible_moves, elephant is free to move diagonally

      to 4 directions (4 possible moves), but if something is in the way in one

      direction, the total possible moves will be reduced. This is what scanners do



After referee is done, board.update_board() will be called

Updated board is then sent to display

"""





# Scanner functions are used to detect invalid movement of context-sensitive pieces

# Called only if these pieces were moved

# Modify possible moves to remove invalid moves (when other pieces are in the way)

    

def chariot_scanner(chariot, board):

# Scan the row or column of a chariot piece.

    x = chariot.get_location()[0]

    y = chariot.get_location()[1]

    

    #eliminate horizontal jump over a piece

    counter = 0

    for i in range(x-1, 0-1, -1):

        if counter > 0:

            chariot.delete_possible_moves([i, y])

        if board[y][i] != 0:

            counter += 1

    

    counter = 0

    for i in range(x+1, 9):

        if counter > 0:

            chariot.delete_possible_moves([i, y])

        if board[y][i] != 0:

            counter += 1



    counter = 0

    for i in range(y-1, 0-1, -1):

        if counter > 0:

            chariot.delete_possible_moves([x, i])

        if board[i][x] != 0:

            counter += 1

    

    counter = 0

    for i in range(y+1, 10):

        if counter > 0:

            chariot.delete_possible_moves([x, i])

        if board[i][x] != 0:

            counter += 1







def cannon_scanner(cannon, board):

    # Scan the row or column of a chariot piece.

    x = cannon.get_location()[0]

    y = cannon.get_location()[1]

    

    #eliminate horizontal jump over a piece

    counter = 0

    for i in range(x-1, 0-1, -1):

        

        if board[y][i] != 0:

            counter += 1

        

        if counter == 2:

            pass

        elif counter > 0:

            cannon.delete_possible_moves([i, y])

    

    counter = 0

    for i in range(x+1, 9):



        if board[y][i] != 0:

            counter += 1

        

        if counter == 2:

            pass

        elif counter > 0:

            cannon.delete_possible_moves([i, y])



    counter = 0

    for i in range(y-1, 0-1, -1):

        

        if board[i][x] != 0:

            counter += 1

        

        if counter == 2:

            pass

        elif counter > 0:

            cannon.delete_possible_moves([x, i])

    

    counter = 0

    for i in range(y+1, 10):

        

        if board[i][x] != 0:

            counter += 1

        

        if counter == 2:

            pass

        elif counter > 0:

            cannon.delete_possible_moves([x, i])



def horse_scanner(horse, board):

    moves = horse.get_possible_moves()

    x = horse.get_location()[0]

    y = horse.get_location()[1]

    for move in moves:

        if (move[0] - x == 2 and board[y][x+1] != 0) or\
           (x - move[0] == 2 and board[y][x-1] != 0) or\
           (move[1] - y == 2 and board[y+1][x] != 0) or\
           (y - move[1] == 2 and board[y-1][x] != 0):
            horse.delete_possible_moves(move)

            



def elephant_scanner(elephant, board):

    moves = elephant.get_possible_moves()

    loc = elephant.get_location()

    for move in moves:

        midpoint = [ int((move[0]+loc[0])/2), int((move[1]+loc[1])/2)  ]

        if board[midpoint[1]][midpoint[0]] != 0:

            elephant.delete_possible_moves(move)



def general_scanner(general, board):

    

    x = general.get_location()[0]

    y = general.get_location()[1]

    

    # Red

    if general.get_color() == "red":

        for i in range (y+1, 9+1):

            if board[i][x] != 0:

                other_piece = board[i][x]

                

                #flying general move is possible

                if other_piece == 32:

                    general.add_possible_moves([x,i])

            

                break

    

    # Black

    if general.get_color() == "black":

        for i in range (y-1, 0-1, -1):

            if board[i][x] != 0:

                other_piece = board[i][x]

                

                #flying general move is possible

                if other_piece == 32:

                    general.add_possible_moves([i,y])

            

                break

    



# referee returns error messages if move is invalid

# turn is a str ("red" or "black")

def referee(turn, piece_moved, new_loc, board, enemy_general):
    
    import piece



    # prevent moving to the same spot

    if piece_moved.get_location() == new_loc:

        return "You have to move from the position you\'re currently standing on!"

    

    # prevent moving opponent's piece

    if turn != piece_moved.get_color():

        return "Don\'t be a traitor and try to kill your own pieces!"

    

    # prevent moving dead pieces

    piece_found = False

    for row in board:

        if piece_moved.get_ID() in row: 

            piece_found = True

            break

    

    if piece_found == False:

        return "Cannot move a dead piece!"

    

    # prevent moving a piece off the board

    if new_loc[0] > 8 or new_loc[1] > 9:

        return "Cannot move a piece off the edge!"



    # prevent capturing ally piece

    x = new_loc[0]

    y = new_loc[1]

    if (turn == "red" and board[y][x] <= 16 and board[y][x] != 0) or\
       (turn == "black" and board[y][x] >= 17 and board[y][x] != 0):

        return "Cannot capture own piece!"

    

    

    

    # prevent context sensitive invalid movements

        #acquire all possible moves

    piece_moved.update_possible_moves()    

    

        #delete invalid moves

    if isinstance(piece_moved, piece.Chariot):

        chariot_scanner(piece_moved, board)

    elif isinstance(piece_moved, piece.Cannon):

        cannon_scanner(piece_moved, board)

    elif isinstance(piece_moved, piece.Horse):

        horse_scanner(piece_moved, board)

    elif isinstance(piece_moved, piece.Elephant):

        elephant_scanner(piece_moved, board)

    elif isinstance(piece_moved, piece.General):

        general_scanner(piece_moved, board)

    

    

    # prevent invalid moves within board

    if new_loc not in piece_moved.get_possible_moves():

        return "Invalid move!"

    

    # game ended. Additional logic needed to bring user out of game state

    if new_loc == enemy_general.get_location():

        return "END"

    

    # if nothing went wrong

    return ""

