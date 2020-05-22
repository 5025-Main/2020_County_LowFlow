# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:27:54 2020

@author: alex.messina
"""

# Python program to find Excel column name from a  
# given column number 
  
def xl_columnrow(col,row=''):
    """ Convert given row and column number to an Excel-style cell name. """
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    while col:
        col, rem = divmod(col-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result)+str(row)
#xl_columnrow(93,2)