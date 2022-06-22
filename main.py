import time
import utils
from Wegame import WeGame

# WeGame("qq号", "游戏昵称")
game = WeGame("", "")


#  1.填写qq号和游戏昵称（大区需单独设置）
#  2.抓包填写cookies
#  3.填写bark推送key

def start():
    # 获取游戏进程状态,进程不存在则查询战绩

    while True:
        print("当前游戏状态:等待获取/未开始游戏")
        # 游戏存在返回True，不存在返回False
        time.sleep(3)
        if utils.get_game_state():

            while utils.get_game_state():
                # 开始监控程序是否结束，结束则发起查询请求
                print("当前游戏状态:游戏中")
                time.sleep(3)
                while not utils.get_game_state():
                    # 游戏已结束，开始查询战绩
                    print("当前游戏状态:游戏结束")
                    time.sleep(3)
                    # 查询成功跳出循环
                    print("当前游戏状态:开始查询战绩")
                    if query_task():
                        break

            # 游戏不存在等待游戏开始


def query_task():
    try:
        # 获取历史战绩列表
        game_list = game.get_game_list()
        # 获取最后一局游戏信息
        last_battle_id = game.get_last_battle(game_list)
        try:
            # 获取战绩详情
            battle_info = game.get_battle_detail(last_battle_id)

            msg = game.get_sort_damage(game.get_user_info(battle_info))

            utils.send_msg(msg)

            return True

        except BaseException as e:

            raise SyntaxError("获取战绩详情失败") from e

    except BaseException as e:

        raise SyntaxError("获取历史战绩列表失败") from e


if __name__ == '__main__':
    start()
