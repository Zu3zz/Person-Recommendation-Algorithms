# -*- coding: utf-8 -*-
# @Author : 3zz
# @Time   : 2019-07-06 13:46
# @File   : itemcf.py
from __future__ import division

import reader
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
    calculate item similarity
    :param user_click: dict, {'userId1': [itemId1, itemId2...],'userId2': [...]...}
    :return:  dict, {'userId1_itemId2': timestamp...}
    """
    co_appear = {}
    item_user_click_time = {}
    # user = 1, itemlist = [1,2,3,4....]
    for user, itemlist in user_click.items():
        # 在itemlist长度里面遍历
        for index_i in range(0, len(itemlist)):
            # 获取item的id 此时item是用户i的
            itemid_i = itemlist[index_i]
            # 先设置默认时间为0 类似这种{1:0,2:0....}
            item_user_click_time.setdefault(itemid_i, 0)
            # 如果有 就+1
            item_user_click_time[itemid_i] += 1
            for index_j in range(index_i + 1, len(itemlist)):
                itemid_j = itemlist[index_j]
                if user + "_" + itemid_i not in user_click_time:
                    click_time_one = 0
                else:
                    click_time_one = user_click_time[user + "_" + itemid_i]
                if user + "_" + itemid_j not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user + "_" + itemid_j]
                co_appear.setdefault(itemid_i, {})
                co_appear[itemid_i].setdefault(itemid_j, 0)
                co_appear[itemid_i][itemid_j] += update_two_contribute_score(click_time_one, click_time_two)

                co_appear.setdefault(itemid_j, {})
                co_appear[itemid_j].setdefault(itemid_i, 0)
                co_appear[itemid_j][itemid_i] += update_two_contribute_score(click_time_one, click_time_two)
    item_sim_score = {}
    item_sim_score_sorted = {}
    for itemid_i, relate_item in co_appear.items():
        for itemid_j, co_time in relate_item.items():
            sim_score = co_time / math.sqrt(item_user_click_time[itemid_i] * item_user_click_time[itemid_j])
            item_sim_score.setdefault(itemid_i, {})
            item_sim_score[itemid_i].setdefault(itemid_j, 0)
            item_sim_score[itemid_i][itemid_j] = sim_score
    for itemid in item_sim_score:
        item_sim_score_sorted[itemid] = sorted(item_sim_score[itemid].items(), key=operator.itemgetter(1),
                                               reverse=True)
    return item_sim_score_sorted


def cal_recom_result(sim_info, user_click):
    """
    calculate recommendation result by itemCF
    :param sim_info: dict: {item, similarity}
    :param user_click: dict:{user click}
    :return: dict, {key: userId ,value: dict{key:itemId, value: recommendation_score}}
    """
    recent_click_num = 3
    topk = 5
    recom_info = {}
    for user in user_click:
        click_list = user_click[user]
        recom_info.setdefault(user, {})
        for itemid in click_list[:recent_click_num]:
            if itemid not in sim_info:
                continue
            for item_sim_combine in sim_info[itemid][:topk]:
                itemsimid = item_sim_combine[0]
                item_sim_score = item_sim_combine[1]
                recom_info[user][itemsimid] = item_sim_score
    return recom_info


def debug_itemsim(item_info, sim_info):
    """
    show itemsim info
    Args:
        item_info: dict, key itemid value:[title, genres]
        sim_info: dict key itemid , value dict,  key [(itemid1, simscore), (itemdi2, simscore)]
    """
    fixed_itemid = "1"
    if fixed_itemid not in item_info:
        print("invalid itemid")
        return
    [title_fix, genres_fix] = item_info[fixed_itemid]
    for zuhe in sim_info[fixed_itemid][:5]:
        itemid_sim = zuhe[0]
        sim_score = zuhe[1]
        if itemid_sim not in item_info:
            continue
        [title, genres] = item_info[itemid_sim]
        print(title_fix + "\t" + genres_fix + "\tsim:" + title + "\t" + genres + "\t" + str(sim_score))


def debug_recomresult(recom_result, item_info):
    """
    debug recomresult
    Args:
        recom_result: key userid value:dict , value_key:itemid , value_value:recom_score
       item_info: dict, key itemid  value:[title, genre]

    """
    user_id = "1"
    if user_id not in recom_result:
        print("invalid result")
        return
    for zuhe in sorted(recom_result[user_id].items(), key=operator.itemgetter(1), reverse=True):
        itemid, score = zuhe
        if itemid not in item_info:
            continue
        print(",".join(item_info[itemid]) + "\t" + str(score))


def main_flow():
    """
    main flow of itemcf
    """
    user_click, user_click_time = reader.get_user_click("../data/ratings.txt")
    item_info = reader.get_item_info("../data/movies.txt")
    sim_info = cal_item_sim(user_click, user_click_time)
    debug_itemsim(item_info, sim_info)
    # recom_result = cal_recom_result(sim_info, user_click)
    # print recom_result["1"]
    # debug_recomresult(recom_result, item_info)


if __name__ == "__main__":
    main_flow()
