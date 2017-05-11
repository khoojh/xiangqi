# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:56:44 2017

@author: khoojinghwan
"""

import piece
import referee


b = piece.Board()

r_soldier_1 = piece.Soldier([0,3], 1)
r_soldier_2 = piece.Soldier([2,3], 2)
r_soldier_3 = piece.Soldier([4,3], 3)
r_soldier_4 = piece.Soldier([6,3], 4)
r_soldier_5 = piece.Soldier([8,3], 5)

b_soldier_1 = piece.Soldier([0,6], 17)
b_soldier_2 = piece.Soldier([2,6], 18)
b_soldier_3 = piece.Soldier([4,6], 19)
b_soldier_4 = piece.Soldier([6,6], 20)
b_soldier_5 = piece.Soldier([8,6], 21)

r_cannon_1 = piece.Cannon([1,2], 6)
r_cannon_2 = piece.Cannon([7,2], 7)
b_cannon_1 = piece.Cannon([1,7], 22)
b_cannon_2 = piece.Cannon([7,7], 23)

r_chariot_1 = piece.Chariot([0,0], 8)
r_chariot_2 = piece.Chariot([8,0], 9)
b_chariot_1 = piece.Chariot([0,9], 24)
b_chariot_2 = piece.Chariot([8,9], 25)

r_horse_1 = piece.Horse([1,0], 10)
r_horse_2 = piece.Horse([7,0], 11)
b_horse_1 = piece.Horse([1,9], 26)
b_horse_2 = piece.Horse([7,9], 27)

r_elephant_1 = piece.Elephant([2,0], 12)
r_elephant_2 = piece.Elephant([6,0], 13)
b_elephant_1 = piece.Elephant([2,9], 28)
b_elephant_2 = piece.Elephant([6,9], 29)

r_advisor_1 = piece.Advisor([3,0], 14)
r_advisor_2 = piece.Advisor([5,0], 15)
b_advisor_1 = piece.Advisor([3,9], 30)
b_advisor_2 = piece.Advisor([5,9], 31)

r_general = piece.General([4,0], 16)
b_general = piece.General([4,9], 32)

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


# ^This whole chunk of code above have to be implemented every time a game starts
# Or we can put the whole thing into a function and set all the
# variables (r_soldier_1 etc) to global. But idk it feels messy to me


# Call this function to make a move
# Input: Whose turn, piece ID, new location
# Output: Error message or (if no error found) updated board

def move_piece(turn, piece_ID, loc):
    
    piece_moved = piece_dict[piece_ID]

    if turn == "black":
        enemy_general = r_general
    elif turn == "red":
        enemy_general = b_general

    msg = referee.referee(turn, piece_moved, loc, b.get_board(), enemy_general)
    
    if len(msg) == 0:
        b.update_board(piece_moved, loc)
        return b.print_board()
    else:
        return msg
        
"""
EXAMPLE:

print(b.print_board())
msg = move_piece("red", 3, [4,4])
print(msg)
msg = move_piece("black", 19, [4,5])
print(msg)
msg = move_piece("red", 3, [4,5])
print(msg)
msg = move_piece("black", 22, [1,0])
print(msg)
msg = move_piece("red", 7, [7,8])
print(msg)
msg = move_piece("red", 3, [5,5])
print(msg)
msg = move_piece("red", 16, [4,9])
print(msg)
"""