#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import argparse
import copy

from card import Card
from player import PlayerHuman, PlayerCPU
from dealer import Dealer
from ui import UI
from field import Field

__version__ = '0.1.0'
__doc__ = 'スカウトゲーム（α版）'

class main():

    def __init__(self, args):

        #引数を受け取る
        self.args = args

        # 変数生成
        self.round_count = 0

        # ゲームを開始する
        self.main_processing()

    def main_processing(self):
        '''メイン処理'''

        # UI生成
        self.ui = self.newUI()
        self.ui.showMessage(__doc__)

        # ゲーム設定
        self.setting()

        # ゲーム開始
        self.game()

        # 最終的な結果を表示
        self.showResult()

    def setting(self):
        '''ゲーム設定'''

        #プレイヤー人数の設定
        if not self.args.player :
            self.num_players = self.ui.getNumberOfPlayers()
        else :
            self.num_players = args.player
        self.ui.showMessage(str(self.num_players)+"人でプレイします")

        #CPU人数の設定
        if self.args.cpu :
            self.num_cpus = self.args.cpu
        else :
            self.num_cpus = self.num_players - 1

        # 各種オブジェクトを生成
        self.deck = self.newCards()
        self.players = self.newPlayers()
        self.dealer = self.newDealer()
        self.field = self.newField()

    def game(self) :
        '''ゲームメイン処理'''

        # 最初の開始位置はランダム
        first_player_index = random.randint(0,len(self.players)-1)

        # 全プレイヤー人数分ラウンド行う
        for round_count in range(len(self.players)) :

            # ラウンド初期化
            self.round_count = round_count + 1
            self.scoutcount = 0

            # UI
            self.ui.showMessage("")
            self.ui.showMessage("第"+str(self.round_count)+"ラウンド開始")
            self.ui.showMessage("")

            # ラウンド開始
            self.round(first_player_index)

            # ラウンド結果出力
            self.showRounndResult()
            first_player_index += 1
            if first_player_index == len(self.players) :
                first_player_index = 0


    def round(self, first_player_index):
        '''ラウンド処理'''

        # カードを配布する
        self.dealCards()

        # カードの上下を選択する
        self.selectAboveOrBelow()

        # 選択後の手札を表示
        if self.args.debug :
            for player in self.players :
                self.showPlayersCards(player)

        # 開始位置
        player_index = first_player_index

        # ゲームのループ開始
        while True :

            # 次のplayerのindexを予め設定する
            next_player_index = player_index + 1
            # 末尾だったら0に戻る
            if next_player_index == len(self.players) :
                next_player_index = 0

            # プレイヤー設定
            player = self.players[player_index]

            # スカウト回数を確認し自分以外スカウトしたらラウンド終了する
            if self.scoutcount == len(self.players) - 1 :
                player.win = True
                self.ui.showMessage(player.name+"がショーをしたカードに対して他の全員がスカウトしたのでラウンドを終了します")
                break

            # 場とプレーヤーの情報表示
            self.ui.showMessage("")
            self.ui.showMessage(player.name+"のターン")
            self.ui.showPlayerInfo(player)
            self.ui.showField(self.field)
            if self.args.debug :
                self.ui.showCardsTop(player.cards, player.name)
            else :
                if player.type == "hum" :
                    self.ui.showCardsTop(player.cards, player.name)
                else :
                    pass

            # プレイヤーのアクション
            self.playersAction(player)

            # プレイヤーが手札を全て出し切ったらラウンド終了
            if len(player.cards) == 0 :
                player.win = True
                self.ui.showMessage(player.name+"がショーをして手札を出し切ったのでラウンドを終了します")
                break

            # 順番を回す
            player_index = next_player_index

    def newCards(self):
        '''トランプのカードを作成する'''

        cards = []

        for i in range(1,11) :  # マークの種類は4
            for j in range(i+1,11) :  # 数字の種類は13

                # カードを作成
                if self.num_players == 3 :
                    if i == 10 or j == 10 :
                        continue
                elif self.num_players == 4 or 2:
                    if i == 9 and j == 10 :
                        continue
                card = Card(i, j)
                cards.append(card)

        if self.args.debug :
            self.ui.showCards(cards, "デッキ")

        return cards

    def newPlayers(self):
        '''プレイヤーを作成する'''

        players = []

        num_humans = self.num_players-self.num_cpus

        for id in range(0,num_humans):

            # プレイヤー(human)を作成
            player = PlayerHuman(id, "プレイヤー"+str(id))
            players.append(player)

        for id in range(num_humans,self.num_players):

            # プレイヤー(CPU)を作成
            player = PlayerCPU(id, "CPU"+str(id))
            players.append(player)

        return players

    def newDealer(self):
        '''ディーラー作成する'''

        return Dealer()

    def newUI(self):
        '''UIを作成する'''

        return UI()

    def newField(self):
        '''場を作成する'''

        return Field()

    def dealCards(self):
        '''カードを配布する'''

        # プレイヤー情報クリア
        for player in self.players :
            player.cards = []  # プレイヤーの手札を回収
            player.showpoint = 0 # プレーヤーのショーポイント回収
            player.scoutpoint = 0 # プレーヤーのスカウトポイント回収
            player.scout_and_show_chip = True # scout&showチップを配る
            player.win = False # ラウンドで勝ったかどうか回収

        # 場札情報クリア
        self.field.cards = []
        self.field.state = "blank"
        self.field.owner = None

        # dealerにカードを配ることを依頼
        self.dealer.cards = copy.copy(self.deck)
        self.dealer.players = self.players
        self.dealer.dealCards()

        self.ui.showMessage("カードが配られました")

        # 配布後の手札を表示
        for player in self.players :
            if self.args.debug :
                self.ui.showCards(player.cards, player.name)
            else :
                if player.type == "hum" :
                    self.ui.showCards(player.cards, player.name)
                else :
                    pass

    def selectAboveOrBelow(self):
        '''カードの上下を選択する'''

        for player in self.players :
            player.selectAboveOrBelow()

    def showPlayersCards(self, player):
        '''プレイヤーカードを表示する'''

        # プレイヤーカードの表示をUIに依頼
        self.ui.showCardsTop(player.cards, player.name+"（選択後）")

    def playersAction(self, player):
        '''各プレイヤーのアクション'''

        action =  player.playersAction(self.field)

        if action == "scout" :
            self.scoutcount += 1
        else :
            self.scoutcount = 0

    def showResult(self):
        '''最終結果を表示する'''

        self.ui.showResult(sorted(self.players, key=lambda x:(x.totalpoint),reverse=True))

    def showRounndResult(self):
        '''ラウンド結果を表示する'''

        # 点数計算
        for player in self.players :
            point = player.scoutpoint + player.showpoint
            if not player.win :
                point -= len(player.cards)
            player.totalpoint += point
            player.point.append(point)

        self.ui.showRoundResult(sorted(self.players, key=lambda x:(x.totalpoint),reverse=True),self.round_count)


if __name__ == "__main__":
    # パーサを作成
    parser = argparse.ArgumentParser(description=__doc__)
    # 受け取る引数を追加していく
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Show version of this game and exit.')
    parser.add_argument('-d', '--debug', action='store_true', help='Show debug log.')
    parser.add_argument('-p', '--player', type=int, help='Specify number of players.')
    parser.add_argument('-c', '--cpu', type=int, help='Specify the number of CPUs.')
    # 引数を解析
    args = parser.parse_args()
    main(args)