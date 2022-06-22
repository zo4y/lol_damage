# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 19:15
# @Author  : zoey7i
# @FileName: Wegame.py
# @Software: PyCharm
import time

import requests
from urllib.parse import unquote

headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "trpc-caller": "wegame.pallas.web.LolBattle",
    "Origin": "https://www.wegame.com.cn",
    "Referer": "https://www.wegame.com.cn/helper/lol/record/profile.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.124 Safari/537.36 qblink wegame.exe WeGame/5.3.2.5230 QBCore/3.70.107.400 QQBrowser/9.0.2524.400",
    "Cookie": ""  # 需填写cookie  网页版wegame抓包cookie也可以
}


class WeGame:

    def __init__(self, qq_uin, game_nick):
        self.qq_uin = qq_uin
        self.end_time = ""
        self.game_nick = game_nick

    #  获取历史战绩列表
    def get_game_list(self):
        url = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleList"

        data = {
            "account_type": 1,
            "id": self.qq_uin,  # 需查询的qq号
            "area": 1,  # 大区 艾欧尼亚
            "offset": 0,
            "count": 7,
            "filter": "",
            "from_src": "lol_helper"
        }

        resp = requests.post(url=url, json=data, headers=headers).json()

        if resp['result']['error_message'] == "success":
            return resp
        else:
            print("获取战绩列表失败")
            return {"msg": "error"}

    #  获取指定对局id游戏详情
    def get_battle_detail(self, game_id):
        url = "https://www.wegame.com.cn/api/v1/wegame.pallas.game.LolBattle/GetBattleDetail"

        data = {
            "account_type": 1,
            "id": self.qq_uin,
            "area": 1,
            "game_id": game_id,
            "from_src": "lol_helper"
        }

        resp = requests.post(url=url, json=data, headers=headers).json()

        return resp

    #  获取最近一局游戏
    def get_last_battle(self, game_list):

        # game_start_time  游戏开始时间  1654879773456
        #  game_time_played  游戏进行时长  906/秒
        last_battle_id = game_list['battles'][0]['game_id']
        game_start_time = game_list['battles'][0]['game_start_time']
        game_time_played = game_list['battles'][0]['game_time_played']

        game_end_time = time.localtime((int(game_start_time) + game_time_played * 1000) / 1000)
        game_end_time = time.strftime("%Y-%m-%d %H:%M:%S", game_end_time)
        self.end_time = game_end_time

        return last_battle_id

    #  获取本局我方team_id
    def get_this_team_id(self, user_dict):

        #  返回本局team_id
        battle_team_id = 0
        for i in range(len(user_dict)):
            if unquote(user_dict[i]['name'], 'utf-8') == self.game_nick:
                battle_team_id = user_dict[i]['teamId']
                break

        return battle_team_id

    #  获取战绩中用户战绩详情
    def get_user_info(self, battle_data):

        user_dict = battle_data['battle_detail']['player_details']
        #  获取本局我方team_id
        team_id = self.get_this_team_id(user_dict)

        user_info_dict = []
        for i in range(len(user_dict)):
            # physicalDamageToChampions  物理伤害
            # magicDamageToChampions  魔法伤害
            # trueDemageToChampions  真实伤害
            # totalDamageToChampions  总伤害
            if user_dict[i]['teamId'] == team_id:
                user_name = unquote(user_dict[i]['name'], 'utf-8')
                user_damage = user_dict[i]['totalDamageToChampions']
                if user_dict[i]['battleHonour']['isMvp'] == 1:
                    user_is_mvp = "MVP"
                else:
                    user_is_mvp = "菜鸡"
                user_team_id = user_dict[i]['teamId']
                # print(user_team_id, user_name, user_damage, user_is_mvp)
                user_info = UserInfo(user_name, user_damage, user_is_mvp, user_team_id)
                user_info_dict.append(user_info)

        return user_info_dict

    #  按用户伤害数进行排序
    def get_sort_damage(self, user_info_dict):

        user_info_dict.sort(key=lambda x: x.user_damage, reverse=False)
        msg_data = "|" + self.end_time + "|"
        for userinfo in user_info_dict:
            print(userinfo.user_name, userinfo.user_damage, userinfo.user_is_mvp)

            user_data = userinfo.user_name + ":" + str(userinfo.user_damage) + "(" + str(userinfo.user_is_mvp) + ")|"

            msg_data = msg_data + user_data

        return msg_data


class UserInfo:

    def __init__(self, user_name, user_damage, user_is_mvp, user_team_id):
        self.user_name = user_name
        self.user_damage = user_damage
        self.user_is_mvp = user_is_mvp
        self.user_team_id = user_team_id


if __name__ == '__main__':
    wg = WeGame("", "")

    battle = wg.get_battle_detail(wg.get_last_battle(wg.get_game_list()))

    wg.get_sort_damage(wg.get_user_info(battle))
