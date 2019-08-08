# -*- coding: utf-8 -*-
# @Author : 3zz
# @Time   : 2019-08-08 19:19
# @File   : usercf.py
from __future__ import division
import reader
import math
import operator


def transfer_user_click(user_click):
    """
    get item by user_click
    :param user_click: key userid, value: [itemid1, itemid2]
    :return: dict, key itemid value:[userid1, userid2]
    """
    item_click_by_user = {}
    for user in user_click:
        item_list = user_click[user]
        for itemid in item_list:
            item_click_by_user.setdefault(itemid, [])
            item_click_by_user[itemid].append(user)
    return item_click_by_user


def base_contribution_score():
    """
    base usercf user contribution score
    :return: 1
    """
    return 1


def update_contributio_score(item_user_click_count):
    """
    usercf user contribution score update v1
    :param item_user_click_count: how many user have clicked this item
    :return: contribution score
    """
    return 1 / math.log10(1 + item_user_click_count)


def update_two_contribution_score(click_time_one, click_time_two):
    """
    user cf user contribution score update v2
    :param click_time_one: different user action time to the same item
    :param click_time_two: time two
    :return: contribution score
    """
    delta_time = abs(click_time_two - click_time_one)
    norm_num = 60 * 60 * 24
    delta_time = delta_time / norm_num
    return 1 / (1 + delta_time)


def cal_user_sim(item_click_by_user, user_click_time):
    """
    get user sim info
    :param item_click_by_user:
    :param user_click_time:
    :return:
    """
    co_appear = {}
    user_click_count = {}
    for itemid, user_list in item_click_by_user.items():
        for index_i in range(len(user_list)):
            user_i = user_list[index_i]
            user_click_count.setdefault(user_i, 0)
            user_click_count[user_i] += 1
            if user_i + "_" + itemid not in user_click_time:
                click_time_one = 0
            else:
                click_time_one = user_click_time[user_i + "_" + itemid]
            for index_j in range(index_i, len(user_list)):
                user_j = user_list[index_j]
                if user_j + "_" + itemid not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user_j + "_" + itemid]
                co_appear.setdefault(user_i, {})
                co_appear[user_i].setdefault(user_j, 0)
                co_appear[user_i][user_j] += update_two_contribution_score(click_time_one, click_time_two)
                co_appear.setdefault(user_j, {})
                co_appear[user_j].setdefault(user_i, 0)
                co_appear[user_j][user_i] += update_two_contribution_score(click_time_one, click_time_two)

    user_sim_info = {}
    user_sim_info_sorted = {}
    for user_i, relate_user in co_appear.items():
        user_sim_info.setdefault(user_i, {})
        for user_j, cotime in relate_user.items():
            user_sim_info[user_i].setdefault(user_j, 0)
            user_sim_info[user_i][user_j] = cotime / math.sqrt(user_click_count[user_i] * user_click_count[user_j])
    for user in user_sim_info:
        user_sim_info_sorted[user] = sorted(user_sim_info[user].items(), key=operator.itemgetter(1), reverse=True)
    return user_sim_info_sorted


def cal_recom_result(user_click, user_sim):
    """
    recome by usercf algo
    :param user_click: dict, key: userid , value: [itemid1, itemid2]
    :param user_sim: key: userid, value: [(useridj, score1),(useridk, score2)]
    :return: dict, key: userid, value: dict; value_key: itemid, value_value: recom_score
    """
    recome_result = {}
    topk_user = 3
    item_num = 5
    for user, item_list in user_click.items():
        tmp_dict = {}
        for itemid in item_list:
            tmp_dict.setdefault(itemid, 1)
        recome_result.setdefault(user, {})
        for combine in user_sim[user][:topk_user]:
            userid_j, sim_score = combine
            if userid_j not in user_click:
                continue
            for itemid_j in user_click[userid_j][:item_num]:
                recome_result[user].setdefault(itemid_j, sim_score)
    return recome_result


def debug_user_sim(user_sim):
    """
    print user sim result
    :param user_sim: key:userid, value: [(userid1, score1),(userid2, score2)]
    :return: None
    """
    topk = 5
    fix_user = "1"
    if fix_user not in user_sim:
        print("invalid user")
        return
    for combine in user_sim[fix_user][:topk]:
        userid, score = combine
        print(fix_user + "\tsim_user" + userid + "\t" + str(score))


def debug_recom_result(item_info, recom_result):
    """
    print recom result for user
    :param item_info: key:itemid, value:[title, genres]
    :param recom_result: key: userid, value:dict; value_key:itemid, value_value:recom_score
    :return: None
    """
    fix_user = "1"
    if fix_user not in recom_result:
        print("invalid user for recoming result")
        return
    for itemid in recom_result["1"]:
        if itemid not in item_info:
            continue
        recom_score = recom_result["1"][itemid]
        print("recom_result:" + ",".join(item_info[itemid]) + "\t" + str(recom_score))


def main_flow():
    """
    main flow
    :return:
    """
    user_click, user_click_time = reader.get_user_click("../data/ratings.txt")
    item_info = reader.get_item_info("../data/movies.txt")
    item_click_by_user = transfer_user_click(user_click)
    user_sim = cal_user_sim(item_click_by_user, user_click_time)
    debug_user_sim(user_sim)


if __name__ == "__main__":
    main_flow()
