# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:06:00 2017

@author: khoojinghwan
"""

# Each piece is initiated with a unique location and ID at the beginning
# of a game
import matplotlib as ply
import referee

class Piece():
    def __init__(self, location, ID):
#        self.status = 1 # 1 means alive, 0 means dead
        self.location = location
        self.ID = ID
        if self.ID >= 0 and self.ID <= 16:
            self.color = "red"
        else:
            self.color = "black"
        self.possible_moves = []
        
#    def get_status(self):
#        return self.status
    
#    def set_status(self, n):
#        self.status = n # n is either 0 or 1
    
    def get_location(self):
        return self.location
    
    def set_location(self, loc):
        self.location = loc
    
    def get_ID(self):
        return self.ID
        
    def get_color(self):
        return self.color
    
    def get_possible_moves(self):
        return self.possible_moves
    
    def add_possible_moves(self, move):
        self.possible_moves.append(move)
    
    def delete_possible_moves(self, move):
        self.possible_moves.remove(move)

        
class Soldier(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)
        
    
    #possible moves are map-blind and piece-blind, meaning they do not take
    #into account the possibility of moving off the map or moving over other
    #pieces. Preventing these will be the job of referee.
    #However, each piece are aware of their own in-map boundaries (eg palace for general)
    
    def update_possible_moves(self):

        loc = self.location[::]
        
        if self.color == "red":
            loc[1] += 1
            self.possible_moves.append(loc) #move forward
        
            #after crossing the river
            if self.location[1] >= 5:
            
                #move right
                loc = self.location[::]
                loc[0] += 1
                self.possible_moves.append(loc)
            
                #move left
                loc = self.location[::]
                loc[0] -= 1
                self.possible_moves.append(loc)
            
        elif self.color == "black":
            loc[1] -= 1
            self.possible_moves.append(loc) #move forward
        
            #after crossing the river
            if self.location[1] <= 4:
            
                #move right
                loc = self.location[::]
                loc[0] += 1
                self.possible_moves.append(loc)
            
                #move left
                loc = self.location[::]
                loc[0] -= 1
                self.possible_moves.append(loc)


class Cannon(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)

    def update_possible_moves(self):  

        loc = self.location[::]
            
        #forward or backward moves
        for i in range(0, 10):
            if loc[1] != i:
                self.possible_moves.append([loc[0], i])
            
        #horizontal moves
        for i in range(0, 9):
            if loc[0] != i:
                self.possible_moves.append([i, loc[1]])
                

class Chariot(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)

    def update_possible_moves(self):  

        loc = self.location[::]
            
        #forward or backward moves
        for i in range(0, 10):
            if loc[1] != i:
                self.possible_moves.append([loc[0], i])
            
        #horizontal moves
        for i in range(0, 9):
            if loc[0] != i:
                self.possible_moves.append([i, loc[1]])


class Horse(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)

    def update_possible_moves(self):  

        loc = self.location[::]
        
        loc = self.location[::]
        loc[0] += 2
        loc[1] += 1
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] += 1
        loc[1] += 2
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] += 2
        loc[1] -= 1
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] += 1
        loc[1] -= 2
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 2
        loc[1] += 1
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 1
        loc[1] += 2
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 2
        loc[1] -= 1
        self.possible_moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 1
        loc[1] -= 2
        self.possible_moves.append(loc)


class Elephant(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)

    def update_possible_moves(self):  
        
        moves = []
        
        loc = self.location[::]
        loc[0] += 2
        loc[1] += 2
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] += 2
        loc[1] -= 2
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 2
        loc[1] += 2
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 2
        loc[1] -= 2
        moves.append(loc)
        
        #Prevent elephant from crossing the river
        
        for move in moves:
            if (self.color == "red" and move[1] <= 4) or \
               (self.color == "black" and move[1] >= 5):
                self.possible_moves.append(move)


class Advisor(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)

    def update_possible_moves(self):  

        loc = self.location[::]
        
        #Since there are only five possible moves, they are hardcoded to avoid complication
        
        # red
        if loc == [3,0] or loc == [5,0] or loc == [3,2] or loc == [5,2]:
            self.possible_moves.append([4,1])
        
        elif loc == [4,1]:
            self.possible_moves.append([3,0])
            self.possible_moves.append([5,0])
            self.possible_moves.append([3,2])
            self.possible_moves.append([5,2])
        
        # black
        if loc == [3,9] or loc == [5,9] or loc == [3,7] or loc == [5,7]:
            self.possible_moves.append([4,8])
        
        elif loc == [4,1]:
            self.possible_moves.append([3,9])
            self.possible_moves.append([5,9])
            self.possible_moves.append([3,7])
            self.possible_moves.append([5,7])
            
        return self.possible_moves


class General(Piece):
    def __init__(self, location, ID):
        super().__init__(location, ID)

    def update_possible_moves(self):  

        moves = []
        
        #horizontal moves        
        
        loc = self.location[::]
        loc[0] -= 1
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] += 1
        moves.append(loc)
        
        #vertical moves        
        
        loc = self.location[::]
        loc[1] -= 1
        moves.append(loc)
        
        loc = self.location[::]
        loc[1] += 1
        moves.append(loc)
        
        #diagonal moves
        
        loc = self.location[::]
        loc[0] += 1
        loc[1] += 1
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] += 1
        loc[1] -= 1
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 1
        loc[1] += 1
        moves.append(loc)
        
        loc = self.location[::]
        loc[0] -= 1
        loc[1] -= 1
        moves.append(loc)
        
        
        #Prevent general from leaving the palace
        for move in moves:
            if self.color == "red":
                if (move[0] >= 3 or move[0] <= 5) and move[1] <= 2:
                    self.possible_moves.append(move)
            
            elif self.color == "black":
                if (move[0] >= 3 or move[0] <= 5) and move[1] >= 7:
                    self.possible_moves.append(move)
        
        return self.possible_moves
        
        


"""
ID's

RED
Soldier: 1, 2, 3, 4, 5
Cannon: 6, 7
Chariot: 8, 9
Horse: 10, 11
Elephant: 12, 13
Advisor: 14, 15
General: 16

BLACK
Soldier: 17, 18, 19, 20, 21
Cannon: 22, 23
Chariot: 24, 25
Horse: 26, 27
Elephant: 28, 29
Advisor: 30, 31
General: 32

--> Might need a dict to map ID's to pieces

"""

        
class Board():
    def __init__(self):
        # board with unique ID's encoded
        self.board = [   #0   1   2   3   4   5   6   7   8
                        [ 8, 10, 12, 14, 16, 15, 13, 11,  9], #0
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0], #1
                        [ 0,  6,  0,  0,  0,  0,  0,  7,  0], #2
                        [ 1,  0,  2,  0,  3,  0,  4,  0,  5], #3
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0], #4
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0], #5
                        [17,  0, 18,  0, 19,  0, 20,  0, 21], #6
                        [ 0, 22,  0,  0,  0,  0,  0, 23,  0], #7
                        [ 0,  0,  0,  0,  0,  0,  0,  0,  0], #8
                        [24, 26, 28, 30, 32, 31, 29, 27, 25]  #9
                        ]
    
    def get_board(self):
        return self.board

    def update_board(self, piece, new_loc):
        x = piece.get_location()[0]
        y = piece.get_location()[1]
        self.board[y][x] = 0
        piece.set_location(new_loc)
        new_x = new_loc[0]
        new_y = new_loc[1]
        self.board[new_y][new_x] = piece.get_ID()

    def ID_to_Chinese_name(self, IDD):
        
        Chinese_names = [ '兵秩一', '兵秩二', '兵秩三', '兵秩四' \
                       ,'兵秩五', '炮秩一','炮秩二','俥秩一' \
                       ,'俥秩二', '傌秩一','傌秩二','相秩一' \
                       ,'相秩二', '仕秩一', '仕秩二','秩帥秩' \
                       ,'卒秩一', '卒秩二', '卒秩三', '卒秩四' \
                       ,'卒秩五', '砲秩一','砲秩二', '車秩一' \
                       ,'車秩二','馬秩一','馬秩二','象秩一' \
                       ,'象秩一','士秩一', '士秩二' ,'秩將秩']
        ID_to_name_dict = {}        
        for ID in range(1,33):
            ID_to_name_dict[ID] = Chinese_names[ID - 1]
        return ID_to_name_dict[IDD]
        
    def ID_to_English_names(self, IDD):
        piece_names = [ 'r_soldier_1', 'soldier_2', 'r_soldier_3', 'r_soldier_4' \
                       ,'r_soldier_5', 'r_cannon_1','r_cannon_2','r_chariot_1' \
                       ,'r_chariot_2', 'r_horse_1','r_horse_2','r_elephant_1' \
                       ,'r_elephant_2', 'r_advisor_1', 'r_advisor_2','r_general' \
                       ,'b_soldier_1', 'b_soldier_2', 'b_soldier_3', 'b_soldier_4' \
                       ,'b_soldier_5', 'b_cannon_1','b_cannon_2', 'b_chariot_1' \
                       ,'b_chariot_2','b_horse_1','b_horse_2','b_elephant_1' \
                       ,'b_elephant_2','b_advisor_1', 'b_advisor_2' ,'b_general']
        abbrvts = ['rs1','rs2','rs3','rs4','rs5','rp1','rp2','rc1','rc2','rh1','rh2','re1','re2','ra1'\
                   ,'ra2','grl','bs1','bs2','bs3','bs4','bs5','bp1','bp2','bc1','bc2','bh1','bh2','be1'\
                   ,'be2','ba1','ba2','grl']
        ID_to_name_dict = {}        
        for ID in range(1,33):
            ID_to_name_dict[ID] = abbrvts[ID - 1]
        return ID_to_name_dict[IDD]
# OG VERSION THAT WORKS
    def print_board(self):
        print_board = ''
        # Wabba Opt
        label_x_axis = ['A','B','C','D','E','F','G','H','I ']
        label_y_axis = [i for i in range(10)]
        count_y = 0
        #Wabba Opt
        print_board += '-|-----------------------------------------------|\n'
        print_board += ' |                   {:<12}                |\n'.format('GAME BOARD')
        print_board += '-|-----------------------------------------------|\n'
        for row in self.board:
            print_board += '{}|['.format(label_y_axis[count_y])
            count_y += 1
            for item in row:
                if item == row[-1]:
                    print_board += '{:>4} '.format(str(item))
                else:
                    print_board += '{:>4} '.format(str(item))
            print_board += ']|\n'
        print_board += '-|-----------------------------------------------|\n'
        print_board += ' |  '
        for i in label_x_axis:
            print_board += '  {:^1} |'.format(i)
        print_board += '\n-|-----------------------------------------------|\n'
        return print_board
#--------------------
#GONNA TRY FIGURE THIS ONE OUT
#-----------------------------
#    def print_board(self):
#        print_board = ''
#        # Wabba Opt
#        label_x_axis = ['A','B','C','D','E','F','G','H','I ']
#        label_y_axis = [i for i in range(10)]
#        count_y = 0
#        #Wabba Opt
#        print_board += '-|-----------------------------------------------|\n'
#        print_board += ' |                   {:<12}                |\n'.format('GAME BOARD')
#        print_board += '-|-----------------------------------------------|\n'
#        for row in self.board:
#            print_board += '{}|['.format(label_y_axis[count_y])
#            count_y += 1
#            for item in row:
#                if item == 0:
#                    print_board += '{:^5}'.format('|一一一|')
##                elif item == row[-1]:
#                else:
#                    print_board += '{:^5}'.format('|'+str(self.ID_to_Chinese_name(item)+'|'))
#                else:
#                    print_board += '{:>4} '.format(str(item))
#            print_board += ']|\n'
#        print_board += '-|-----------------------------------------------|\n'
#        print_board += ' |  '
#        for i in label_x_axis:
#            print_board += '  {:^1} |'.format(i)
#        print_board += '\n-|-----------------------------------------------|\n'
#        return print_board
<<<<<<< HEAD
#
#--------------------
#GONNA TRY FIGURE THIS ONE OUT
#-----------------------------
    def print_board(self):
        print_board = ''
        # Wabba Opt
        label_x_axis = ['A','B','C','D','E','F','G','H','I   ']
        label_y_axis = [i for i in range(10)]
        count_y = 0
        #Wabba Opt
        print_board += '-|-----------------------------------------------------------------|\n'
        print_board += ' |                             {:<12}                        |\n'.format('GAME BOARD')
        print_board += '-|-----------------------------------------------------------------|\n'
        for row in self.board:
            print_board += '{}|['.format(label_y_axis[count_y])
            count_y += 1
            for item in row:
                if item == 0:
                    print_board += '{:^5}'.format('|一一一|')
#                elif item == row[-1]:
                else:
                    print_board += '{:^5}'.format('|'+str(self.ID_to_Chinese_name(item)+'|'))
#                else:
#                    print_board += '{:>4} '.format(str(item))
            print_board += ']|\n'
        print_board += '-|-----------------------------------------------------------------|\n'
        print_board += ' |  '
        for i in label_x_axis:
            print_board += '  {:3} |'.format(i)
        print_board += '\n-|-----------------------------------------------------------------|\n'
        return print_board
=======
>>>>>>> d8828532eb8fc2c8a264d800419fed4440a8f959

    def print_reversed_board(self):
        reversed_print_board = ''
        label_x_axis = ['A','B','C','D','E','F','G','H','I']
        label_y_axis = [i for i in range(9,-1,-1)]
        count_y = 0
        #Wabba Opt
        reversed_print_board += '-|-----------------------------------------------|\n'
        reversed_print_board += ' |                   {:<12}                |\n'.format('GAME BOARD')
        reversed_print_board += '-|-----------------------------------------------|\n'
        cop_board = self.board.copy()
        cop_board.reverse()
        for row in cop_board:
            reversed_print_board += '{}|['.format(label_y_axis[count_y])
            count_y += 1
            for item in row:
                if item == row[-1]:
                    reversed_print_board += '{:>4} '.format(str(item))
                else:
                    reversed_print_board += '{:>4},'.format(str(item))
            reversed_print_board += ']|\n'
        reversed_print_board += '-|-----------------------------------------------|\n'
        reversed_print_board += ' |  '
        for i in label_x_axis:
            reversed_print_board += '  {:^1} |'.format(i)
        reversed_print_board += '\n-|-----------------------------------------------|\n'

        return reversed_print_board
"""
This is a simple implementation to make sure that the game works properly



#################################
b = Board()                     #
print(b.print_board())          #
b.update_board(soldier,[4,4])   #
print(b.print_board())          #
#################################

"""

def initialize_game():
    
    b = Board()
    
    r_soldier_1 = Soldier([0,3], 1)
    r_soldier_2 = Soldier([2,3], 2)
    r_soldier_3 = Soldier([4,3], 3)
    r_soldier_4 = Soldier([6,3], 4)
    r_soldier_5 = Soldier([8,3], 5)
    
    b_soldier_1 = Soldier([0,6], 17)
    b_soldier_2 = Soldier([2,6], 18)
    b_soldier_3 = Soldier([4,6], 19)
    b_soldier_4 = Soldier([6,6], 20)
    b_soldier_5 = Soldier([8,6], 21)
    
    r_cannon_1 = Cannon([1,2], 6)
    r_cannon_2 = Cannon([7,2], 7)
    b_cannon_1 = Cannon([1,7], 22)
    b_cannon_2 = Cannon([7,7], 23)
    
    r_chariot_1 = Chariot([0,0], 8)
    r_chariot_2 = Chariot([8,0], 9)
    b_chariot_1 = Chariot([0,9], 24)
    b_chariot_2 = Chariot([8,9], 25)
    
    r_horse_1 = Horse([1,0], 10)
    r_horse_2 = Horse([7,0], 11)
    b_horse_1 = Horse([1,9], 26)
    b_horse_2 = Horse([7,9], 27)
    
    r_elephant_1 = Elephant([2,0], 12)
    r_elephant_2 = Elephant([6,0], 13)
    b_elephant_1 = Elephant([2,9], 28)
    b_elephant_2 = Elephant([6,9], 29)
    
    r_advisor_1 = Advisor([3,0], 14)
    r_advisor_2 = Advisor([5,0], 15)
    b_advisor_1 = Advisor([3,9], 30)
    b_advisor_2 = Advisor([5,9], 31)
    
    r_general = General([4,0], 16)
    b_general = General([4,9], 32)
    
    piece_list = [r_soldier_1, r_soldier_2, r_soldier_3, r_soldier_4, \
                  r_soldier_5, b_soldier_1, b_soldier_2, b_soldier_3, \
                  b_soldier_4, b_soldier_5, \
                  r_cannon_1, r_cannon_2, b_cannon_1, b_cannon_2, \
                  r_chariot_1, r_chariot_2, b_chariot_1, b_chariot_2, \
                  r_horse_1, r_horse_2, b_horse_1, b_horse_2, \
                  r_elephant_1, r_elephant_2, b_elephant_1, b_elephant_2, \
                  r_advisor_1, r_advisor_2, b_advisor_1, b_advisor_2, \
                  r_general, b_general]
    
    piece_dict = {}
    for p in piece_list:
        piece_dict[p.get_ID()] = p
        
    return b, piece_dict



# ^This whole chunk of code above have to be implemented every time a game starts
# Or we can put the whole thing into a function and set all the
# variables (r_soldier_1 etc) to global. But idk it feels messy to me


# Call this function to make a move
# Input: Whose turn, piece ID, new location
# Output: True or False
def move_piece(turn, piece_ID , loc, b, dictionary):
    
    piece_moved = dictionary[piece_ID]

    if turn == "black":
        enemy_general = dictionary[16]
    elif turn == "red":
        enemy_general = dictionary[32]

    msg = referee.referee(turn, piece_moved, loc, b.get_board(), enemy_general)
    
    
#    if msg == "END":
#        return msg

    if len(msg) == 0:
        b.update_board(piece_moved, loc)
        return True
    
    else:
        return msg



