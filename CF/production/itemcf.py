# -*- coding: utf-8 -*-
# @Author : 3zz
# @Time   : 2019-07-06 13:46
# @File   : itemcf.py
from __future__ import division
import sys

sys.path.append("../util")
import util.reader as reader
import math
import operator


def base_contribute_score():
    """
    return item base similarity contribution score by user
    :return: 1
    """
    return 1


def update_one_contribute_score(user_total_click_num):
    """
    item cf update similarity score by user
    :param user_total_click_num:
    :return: 1/log(1 + input)
    """
    return 1 / math.log10(1 + user_total_click_num)


def update_two_contribute_score(click_time_one, click_time_two):
    """
    item cf update tow similarity contribution by user
    :param click_time_one: first click time
    :param click_time_two: second click time
    :return: a weight that put time into consider
    """
    delta_time = abs(click_time_one - click_time_two)
    total_sec = 60 * 60 * 24
    delta_time = delta_time / total_sec
    return 1 / (1 + delta_time)


def cal_item_sim(user_click, user_click_time):
    """

    :param user_click: dict, key userId value[itemId1, itemId2]
    :return:  dict, key: itemId_i,
    """
    co_appear = {}
    item_user_click_time = {}
    for user, itemlist in user_click.items():
        for index_i in range(0, len(itemlist)):
            itemid_i = itemlist[index_i]
            item_user_click_time.setdefault(itemid_i, 0)
            item_user_click_time[itemid_i] += 1
            for index_j in range(index_i + 1, len(itemlist)):
                itemid_j = itemlist[itemid_j]
                if user + "_" + itemid_i not in user_click_time:
                    click_time_one = 0
                else:
                    click_time_one = user_click_time[user + "_" + itemid_i]
                if user + "_" + itemid_j not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user + "_" + itemid_j]
                co_appear.setdefault(itemid_i, {})
                co_appear[itemid_i].setfault(itemid_j, 0)
                co_appear[itemid_i][itemid_j] += update_one_contribute_score(click_time_one, click_time_two)


def cal_recom_result():


def main_flow():
    """
    main flow of itemcf
    :return:
    """
    user_click, user_click_time = reader.get_user_click("../data/ratings.txt")
    sim_info = cal_item_sim(user_click, user_click_time)
    recom_result = cal_recom_result(sim_info, user_click)
