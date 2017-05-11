#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:21:57 2017

@author: ricardo
"""

import piece

b, d = piece.initialize_game()
print(piece.move_piece('red',16,[4,1],b,d))
