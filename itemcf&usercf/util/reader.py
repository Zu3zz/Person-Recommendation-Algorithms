# -*- coding: utf-8 -*-
# @Author : 3zz
# @Time   : 2019-07-06 00:41
# @File   : reader.py

import os


def get_user_click(rating_file):
    """
    get user click list
    :param rating_file: input file
    :return: dict,key: useid, value:[itemid1, itemid2...]
    """
    if not os.path.exists(rating_file):
        return {}
    fp = open(rating_file)
    num = 0
    user_click = {}
    for line in fp:
        if num == 0:
            num+=1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        [userid, itemid, rating, timestamp] = item
        if float(rating) < 3.0:
            continue
        if userid not in user_click:
            user_click[userid] = []
        user_click[userid].append(itemid)
    fp.close()
    return user_click

def get_item_info(item_file):
    """
    get item info[title,genres]
    :param item_file: input iteminfo file
    :return: a dict, key itemid, value[item, genres]
    """
    if not os.path.exists(item_file):
        return {}