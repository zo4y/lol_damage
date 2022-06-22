# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 20:56
# @Author  : zoey7i
# @FileName: utils.py
# @Software: PyCharm
import requests
import psutil


#  消息推送
def send_msg(msg):
    api = "https://api.day.app/"
    bark_key = ""  # bark推送key
    title, group = "英雄联盟慈善家推送", "?group=wegame"
    url = api + "/" + title + "/" + msg + group

    requests.get(url=url)


#  获取游戏进程状态
def get_game_state():

    try:
        pid_list = psutil.pids()
        try:
            for pid in pid_list:
                if psutil.Process(pid).name() == "League of Legends.exe":
                    return True
            else:
                return False
        except Exception as e:
            raise SyntaxError("读取pid列表失败") from e
    except Exception as e:
        raise SyntaxError("获取pid列表失败") from e
