#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import argparse
import copy

from card import Card
from player import PlayerHuman, PlayerCPU
from dealer import Dealer
from field import Field
from ui import UI
from scout_play import main

__version__ = '0.1.0'
__doc__ = 'スカウトゲーム（CPUシミュレーション版）'

class cpu_simulation(main):

    def __init__(self, args, statistics):
        #継承
        super().__init__(args)

        self.statistics = statistics

    def setting(self):
        '''ゲーム設定'''

        # プレイヤー人数の設定
        self.num_players = self.args.player

        # プレイヤーはすべてCPU
        self.num_cpus = self.num_players

        # 各種オブジェクトを生成
        self.deck = self.newCards()
        self.players = self.newPlayers()
        self.dealer = self.newDealer()
        self.field = self.newField()

        # UIを非表示にする
        self.ui = NoUI()
        for player in self.players :
            player.ui = NoUI()

    def newUI(self):
        '''UIを作成する'''

        return NoUI()

    def showResult(self):
        '''最終結果を表示する'''

        # 統計に合計点を追加
        self.statistics.sum(self.players)

    def selectAboveOrBelow(self):
        '''カードの上下を選択する'''

        for player in self.players :
            if player.id == 0 :
                print(player.name+"test")
                player.selectAboveOrBelow_test()
            else :
                player.selectAboveOrBelow()

class NoUI(UI) :

    def showMessage(self, message, end='\n') :
        '''メッセージ出力'''

        return

class Statistics():

    def __init__(self):
        self.sum_point = {}

    def sum(self, players):
        for player in players :
            if player.name in self.sum_point.keys() :
                self.sum_point[player.name] += player.totalpoint
            else :
                self.sum_point[player.name] = player.totalpoint


if __name__ == "__main__":
    # パーサを作成
    parser = argparse.ArgumentParser(description=__doc__)
    # 受け取る引数を追加していく
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Show version of this game and exit.')
    parser.add_argument('-d', '--debug', action='store_true', help='Show debug log.')
    parser.add_argument('-p', '--player', required=True, type=int, help='Specify number of players.')
    parser.add_argument('-g', '--games', type=int, default=1, help='Specify number of games to play.')
    # 引数を解析
    args = parser.parse_args()

    statistics = Statistics()

    print("ゲーム数:"+str(args.games))
    for i in range(args.games):
        cpu_simulation(args,statistics).main_processing()

    for key in statistics.sum_point :
        print(key+" Total:"+str(statistics.sum_point[key])+"点, average:"+str(statistics.sum_point[key]/args.games))

