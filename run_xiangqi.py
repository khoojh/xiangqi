#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:17:23 2017

@author: ricardo
"""

import piece
import referee

def start():
    b, piece_dict = piece.initialize_game()
    print(b.print_board())
    return b, piece_dict
if __name__ == "__main__":
    start()

