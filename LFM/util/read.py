# -*- coding: utf-8 -*-
# @Author : 3zz
# @Time   : 2019-07-06 20:32
# @File   : read.py
import os


def get_item_info(input_file):
    """
    get item info:[title, genre]
    :param input_file: item info file
    :return: a dict: key itemId, value:[title, genre]
    """
    if not os.path.exists(input_file):
        return {}
    item_info = {}
    linenum = 0
    fp = open(input_file)
    for line in fp:
        if linenum == 0:
            linenum+=1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue

if __name__ == "__main__":
    print(123)