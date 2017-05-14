#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:51:20 2017

@author: ricardo
"""

import piece
def ID_to_Chinese_name(self, IDD):
    
    Chinese_names = [ '兵_1', '兵_2', '兵_3', '兵_4' \
                   ,'兵_5', '炮_1','炮 _2','俥_1' \
                   ,'俥_2', '傌_1','傌_2','相_1' \
                   ,'相_2', '仕_1', '仕_2',' 帥 ' \
                   ,'卒_1', '卒_2', '卒_3', '卒_4' \
                   ,'卒_5', '砲_1','砲_2', '車_1' \
                   ,'車_2','馬_1','馬_2','象_1' \
                   ,'象_2','士_1', '士_2' ,' 將 ']
    ID_to_name_dict = {}        
    for ID in range(1,33):
        ID_to_name_dict[ID] = Chinese_names[ID - 1]
    return ID_to_name_dict[IDD]

 
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
                print_board += '{:>4} '.format(self.ID_to_Chinese_name(item))
            else:
                print_board += '{:>4} '.format(str(item))
        print_board += ']|\n'
    print_board += '-|-----------------------------------------------|\n'
    print_board += ' |  '
    for i in label_x_axis:
        print_board += '  {:^1} |'.format(i)
    print_board += '\n-|-----------------------------------------------|\n'

b,p = piece.initialize_game()
print(print_board(b]))