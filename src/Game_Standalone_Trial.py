#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 21:17:05 2017

@author: ricardo
"""

import piece
import referee

w_soldier1 = piece.Soldier([4,3], 3)
b_chariot = piece.Chariot([0,9], 24)
b_cannon = piece.Cannon([7,7], 23)
w_elephant = piece.Elephant([2,0], 12)
w_advisor = piece.Advisor([3,0], 14)
w_general = piece.General([4,0], 16)
w_horse = piece.Horse([1,0], 10)

b = piece.Board()
print(b.print_board())
print('Next move:\n\n\n\n\n\n')

b.update_board(w_soldier1,[4,4])
print(b.print_board())
#b.update_board(player_selection)