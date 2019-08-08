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
        return {},{}
    fp = open(rating_file)
    num = 0
    user_click = {}
    user_click_time = {}
    for line in fp:
        if num == 0:
            num += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        [userid, itemid, rating, timestamp] = item
        if userid + '_' + itemid not in user_click_time:
            user_click_time[userid + "_" + itemid] = int(timestamp)
        if float(rating) < 3.0:
            continue
        if userid not in user_click:
            user_click[userid] = []
        user_click[userid].append(itemid)
    fp.close()
    return user_click, user_click_time


def get_item_info(item_file):
    """
    get item info[title,genres]
    :param item_file: input iteminfo file
    :return: a dict, key itemid, value[item, genres]
    """
    if not os.path.exists(item_file):
        return {}
    num = 0
    item_info = {}
    fp = open(item_file)
    for line in fp:
        if num == 0:
            num += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        if len(item) == 3:
            [itemid, title, genres] = item
        elif len(item) > 3:
            itemid = item[0]
            genres = item[-1]
            title = ",".join(item[1:-1])
        if itemid not in item_info:
            item_info[itemid] = [title, genres]
    fp.close()
    return item_info


if __name__ == "__main__":
    # user_click, user_click_time = get_user_click("../data/ratings.txt")
    # print len(user_click)
    # print user_click
    # print user_click_time
    item_info = get_item_info("../data/movies.txt")
    print(item_info["5"])
