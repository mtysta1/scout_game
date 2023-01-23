import random

from ui import UI

class Player():

    def __init__(self,name):
        self.name = name #プレイヤーの名前
        self.rank = 0

def showResult(players):
    '''結果を表示する'''
    for player in players :
        if player.rank == 0 :
            player.rank = len(players)

    ui.showResult(sorted(players, key=lambda x:(x.rank)))

ui = UI()

players = []
for var in ["A","B","C","D","E"] :
    players.append(Player(var))

# 開始位置はランダム
player_index = random.randint(0,len(players)-1)
print(player_index)
finish = False

i = 1

while True :

    # 次のplayerのindexを予め設定する
    next_player_index = player_index
    while True :
        next_player_index += 1
        # 末尾だったら0に戻る
        if next_player_index == len(players) :
            next_player_index = 0
        # プレイヤーが上がってたら飛ばす
        if players[next_player_index].rank != 0 :
            continue
        # 一周したらゲーム終了
        if next_player_index == player_index :
            finish = True
        break

    if finish :
        break

    # プレイヤー設定
    player = players[player_index]

    # プレイヤーのアクション
    var = input(player.name + ":")
    if var == "0" :
        player.rank = i
        i += 1

    # 順番を回す
    player_index = next_player_index

# 最終的な結果を表示
showResult(players)