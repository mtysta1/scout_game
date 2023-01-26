import random

from ui import UI
from card import Card

class PlayerHuman():

    def __init__(self, id, name):
        self.id = id  # プレイヤーのID
        self.name = name #プレイヤーの名前
        self.cards = []  # プレイヤーの手札
        self.point = [] #ラウンド毎の得点
        self.totalpoint = 0 # プレイヤーの総得点
        self.showpoint = 0 # プレーヤーのショーポイント
        self.scoutpoint = 0 # プレーヤーのスカウトポイント
        self.scout_and_show_chip = True # スカウト&ショーチップ、これがないとできない
        self.ui = UI()
        self.win = False # ラウンドで勝ったかどうか
        self.type = "hum"

    def playersAction(self, field):
        '''アクション'''

        action = self.ui.getPlayerAction(self)

        if action == "A" :
            self.show(field)
            return "show"
        elif action == "B" :
            if not field.state == "blank" :
                self.scout(field)
                return "scout"
            else :
                self.ui.showErrorMessage("場札がないとスカウトできません")
                return self.playersAction(field)
        elif action == "C" :
            if not field.state == "blank" :
                if self.scout_and_show_chip :
                    self.ui.showMessage("スカウト&ショー！")
                    self.scout(field)
                    self.show(field)
                    self.scout_and_show_chip = False
                    return "scout&show"
                else :
                    self.ui.showErrorMessage("既にスカウト&ショーを行っております")
                    return self.playersAction(field)
            else :
                self.ui.showErrorMessage("場札がないとスカウト&ショーできません")
                return self.playersAction(field)

    def show(self, field):
        '''ショー'''

        cards = self.choiseShowCards(field)
        if cards :
            self.playCards(cards, field)
            self.ui.showPlayerAction(self, "show", cards)
        else :
            self.playersAction(field)

    def choiseShowCards(self, field) :
        '''ショーカードの選択（人間）'''

        while True :

            # Humanが場に出すカードを取得するようにuiに依頼（カードインデックスの配列 or キャンセル（[]））
            choise_nums = self.ui.getShowCards(self)

            # キャンセルの場合Noneを返す
            if choise_nums == [] :
                return None
            else :
                # カードインデックスの配列をCardオブジェクトのリストに変換
                played_cards = []
                for choise_num in  choise_nums :
                    card = self.cards[choise_num]
                    played_cards.append(card)

                # カード整列
                sorted_field_cards = sorted(field.cards, key=lambda x:(x.top_number))
                sorted_played_cards = sorted(played_cards, key=lambda x:(x.top_number))

                # 複数出しの時出せるかチェック
                if len(played_cards) > 1 :
                    i = 0
                    check = True
                    cards_type = ""
                    for i in range(len(played_cards)-1) :
                        if played_cards[i].top_number == played_cards[i+1].top_number and (cards_type == "" or cards_type == "multi_same"):
                            cards_type = "multi_same"
                        elif played_cards[i].top_number + 1 == played_cards[i+1].top_number and (cards_type == "" or cards_type == "multi_steps_up"):
                            cards_type = "multi_steps_up"
                        elif played_cards[i].top_number - 1 == played_cards[i+1].top_number and (cards_type == "" or cards_type == "multi_steps_down"):
                            cards_type = "multi_steps_down"
                        else :
                            check = False
                    if not check :
                        self.ui.playError("出せない組み合わせです")
                        continue
                    if cards_type == "multi_steps_up" or  cards_type == "multi_steps_down" :
                        cards_type = "multi_steps"
                else :
                    cards_type = "single"

                # 場がブランクだったら問答無用で出す
                if field.state == "blank" :
                    return played_cards

                # 場がブランクでなかったら強さチェック
                check_strength = True

                # 枚数比較
                # 多ければ出せる
                if len(played_cards) > len(field.cards) :
                    return played_cards
                # 少なければ出せない
                elif len(played_cards) < len(field.cards) :
                    self.ui.playError("ショーカードの枚数は場札の枚数以上でないと出せません")
                    continue
                # 同じであれば後続のチェックへ
                else :
                    pass

                # タイプ比較
                # シングルだったら通過
                if cards_type == "single" :
                    pass
                else :
                    # 階段に対して同数は強く出せる
                    if field.state == "multi_steps" and cards_type == "multi_same" :
                        return played_cards
                    # 同数に対して階段は弱く出せない
                    elif field.state == "multi_same" and cards_type == "multi_steps" :
                        self.ui.playError("場札が同数カードの時階段のショーカードは出せません")
                        continue
                    # 同じタイプ同士であれば後続のチェックへ
                    else :
                        pass

                # 数字比較
                # １番小さい数字が大きければ出せる
                if sorted_played_cards[0].top_number > sorted_field_cards[0].top_number :
                    return played_cards
                else :
                    self.ui.playError("場札より大きくないと出せません")
                    continue

    def playCards(self, played_cards, field):
        '''カードを場に出す'''

        # カード判定
        if len(played_cards) == 1 :
            state = "single"
        else :
            if played_cards[0].top_number == played_cards[1].top_number :
                state = "multi_same"
            else :
                state = "multi_steps"

        # 場札を会得する
        self.showpoint += len(field.cards)

        # 場を更新する
        field.cards = played_cards
        field.state = state
        field.owner = self

        # 手札からカードを削除する
        for played_card in played_cards :
            for card in self.cards :
                if card.top_number == played_card.top_number and card.bottom_number == played_card.bottom_number :
                    self.releaseCard(self.cards.index(card))
                    break

    def scout(self, field):
        '''スカウト'''

        owner = field.owner
        card = self.choiseScoutCards(field)
        if card :
            index = self.ui.getScoutIndex(self)
            if index == len(self.cards):
                self.addCard(card)
            else :
                self.insertCard(card,index)
            self.ui.showPlayerAction(self, "scout", [card])
        else :
            self.playersAction(field)
        owner.scoutpoint += 1

    def choiseScoutCards(self, field) :
        '''スカウトカードの選択（人間）'''

        while True :
            # Humanが場から取得するカードを取得するようにuiに依頼（カードインデックス or キャンセル（[]））
            choise = self.ui.getScoutCards(field)

            # キャンセルの場合Noneを返す
            if not choise :
                return None
            else :
                # 両端か判断
                if choise[0] == 0 or choise[0] == len(field.cards)-1 :

                    # カードインデックスをCardオブジェクトに変換
                    card = field.cards[choise[0]]

                    # 場札からカードを削除する
                    field.cards.pop(choise[0])
                    # 場の状態を変更する
                    if len(field.cards) == 0 :
                        field.state = "blank"
                        field.owner = None
                    elif len(field.cards) == 1 :
                        field.state = "single"


                    # 逆指定だったらカードを反転
                    if choise[1] == "B" :
                        tmp = card.top_number
                        card.top_number = card.bottom_number
                        card.bottom_number = tmp

                    # カードインデックスをCardオブジェクトに変換
                    return card

                else :
                    self.ui.playError("両端以外はスカウトできません")
                    continue

    def addCard(self, card):
        '''カードを手札に加える'''

        self.cards.append(card)

    def insertCard(self, card, index):
        '''カードを手札に挿入'''

        self.cards.insert(index, card)

    def releaseCard(self, num):
        '''カードを手放す'''

        return self.cards.pop(num)

    def selectAboveOrBelow(self) :
        '''カードの上下を選択'''

        top_or_bottom = self.ui.getAboveOrBelow(self)
        if top_or_bottom == "top" :
            pass
        elif top_or_bottom == "bottom" :
            for card in self.cards :
                tmp = card.top_number
                card.top_number = card.bottom_number
                card.bottom_number = tmp


class PlayerCPU(PlayerHuman):

    def __init__(self, id, name):
        super().__init__(id, name)
        self.type = "cpu"

    def playersAction(self, field):
        '''アクション'''

        # とりあえずショー
        show = self.show(field)
        if show :
            return "show"

        # ランダムでスカウト&ショー
        if self.scout_and_show_chip :
            if random.random() >= 0.8:
                self.ui.showMessage("スカウト&ショー！")
                self.scout(field)
                self.show(field)
                self.scout_and_show_chip = False
                return "scout&show"

        #できなければスカウト
        self.scout(field)
        return "scout"

    def show(self, field):
        '''ショー'''

        cards = self.choiseShowCards(field)
        if cards :
            self.playCards(cards, field)
            self.ui.showPlayerAction(self, "show", cards)
            return True
        else :
            return False

    def choiseShowCards(self, field) :
        '''ショーカードの選択（AI）'''

        # 場が空であれば
        if field.state == "blank" :

            # 最小カードを1枚出す
            played_cards = []
            sorted_self_cards = sorted(self.cards, key=lambda x:(x.top_number))
            played_cards.append(sorted_self_cards[0])
            return played_cards

        # 場があるとき
        else :

            # 場の数以上の数で手札を分割
            split_cards_list = []
            for field_number in range(len(field.cards),len(self.cards)) :
                for i in range(0,len(self.cards)-field_number+1):
                    split_cards=[]
                    for j in range(i,i+field_number):
                        split_cards.append(self.cards[j])
                    split_cards_list.append(split_cards)

            # リストを判定していく
            for played_cards in split_cards_list :

                # カード整列
                sorted_field_cards = sorted(field.cards, key=lambda x:(x.top_number))
                sorted_played_cards = sorted(played_cards, key=lambda x:(x.top_number))

                # 複数出しの時出せるかチェック
                if len(played_cards) > 1 :
                    i = 0
                    check = True
                    cards_type = ""
                    for i in range(len(played_cards)-1) :
                        if played_cards[i].top_number == played_cards[i+1].top_number and (cards_type == "" or cards_type == "multi_same"):
                            cards_type = "multi_same"
                        elif played_cards[i].top_number + 1 == played_cards[i+1].top_number and (cards_type == "" or cards_type == "multi_steps_up"):
                            cards_type = "multi_steps_up"
                        elif played_cards[i].top_number - 1 == played_cards[i+1].top_number and (cards_type == "" or cards_type == "multi_steps_down"):
                            cards_type = "multi_steps_down"
                        else :
                            check = False
                    if not check :
                        continue
                    if cards_type == "multi_steps_up" or  cards_type == "multi_steps_down" :
                        cards_type = "multi_steps"
                else :
                    cards_type = "single"

                # 枚数比較
                # 多ければ出せる
                if len(played_cards) > len(field.cards) :
                    return played_cards
                # 少なければ出せない
                elif len(played_cards) < len(field.cards) :
                    continue
                # 同じであれば後続のチェックへ
                else :
                    pass

                # タイプ比較
                # シングルだったら通過
                if cards_type == "single" :
                    pass
                else :
                    # 階段に対して同数は強く出せる
                    if field.state == "multi_steps" and cards_type == "multi_same" :
                        return played_cards
                    # 同数に対して階段は弱く出せない
                    elif field.state == "multi_same" and cards_type == "multi_steps" :
                        continue
                    # 同じタイプ同士であれば後続のチェックへ
                    else :
                        pass

                # 数字比較
                # １番小さい数字が大きければ出せる
                if sorted_played_cards[0].top_number > sorted_field_cards[0].top_number :
                    return played_cards
                else :
                    continue

            return None

    def scout(self, field):
        '''スカウト'''

        owner = field.owner
        card = self.choiseScoutCards(field)
        # 同数があれば挿入
        for self_card in self.cards :
            if self_card.top_number == card.top_number :
                self.insertCard(card,self.cards.index(self_card))
                self.ui.showPlayerAction(self, "scout", [card])
                owner.scoutpoint += 1
                return
        # 隣の数字があれば挿入
        for self_card in self.cards :
            if self_card.top_number + 1  == card.top_number or self_card.top_number -1  == card.top_number :
                self.insertCard(card,self.cards.index(self_card))
                self.ui.showPlayerAction(self, "scout", [card])
                owner.scoutpoint += 1
                return
        # なければ0に
        self.insertCard(card,0)
        self.ui.showPlayerAction(self, "scout", [card])
        owner.scoutpoint += 1
        return

    def choiseScoutCards(self, field) :
        '''スカウトカードの選択（AI）'''

        # 1番大きい数字を選択
        max = field.cards[0].top_number
        index = 0
        tb = "t"
        if field.cards[len(field.cards)-1].top_number > max :
            max = field.cards[len(field.cards)-1].top_number
            index = len(field.cards)-1
            tb = "t"
        if field.cards[0].bottom_number > max :
            max = field.cards[0].bottom_number
            index = 0
            tb = "b"
        if field.cards[len(field.cards)-1].bottom_number > max :
            max = field.cards[len(field.cards)-1].bottom_number
            index = len(field.cards)-1
            tb = "b"

        card = field.cards[index]

        # 場札からカードを削除する
        field.cards.pop(index)
        # 場の状態を変更する
        if len(field.cards) == 0 :
            field.state = "blank"
            field.owner = None
        elif len(field.cards) == 1 :
            field.state = "single"

        # bottomの数字を選んだら反転
        if tb == "b":
            tmp = card.top_number
            card.top_number = card.bottom_number
            card.bottom_number = tmp

        return card

    def selectAboveOrBelow(self) :
        '''カードの上下を選択'''

        top_sum = 0
        card_numbers_top = []
        bottom_sum = 0
        card_numbers_bottom = []
        for card in self.cards :
            top_sum += card.top_number
            bottom_sum += card.bottom_number
        if top_sum >= bottom_sum :
            pass
        else :
            for card in self.cards :
                tmp = card.top_number
                card.top_number = card.bottom_number
                card.bottom_number = tmp

# 以下はロジック検証用

    def playersAction_test(self, field):
        '''アクション'''

        # とりあえずショー
        show = self.show(field)
        if show :
            return "show"

        # ランダムでスカウト&ショー
        if self.scout_and_show_chip :
            if random.random() >= 0.8:
                self.ui.showMessage("スカウト&ショー！")
                self.scout(field)
                self.show(field)
                self.scout_and_show_chip = False
                return "scout&show"

        #できなければスカウト
        self.scout(field)
        return "scout"

    def selectAboveOrBelow_test(self) :
        '''カードの上下を選択（ロジック検証用）'''

        top_sum = 0
        card_numbers_top = []
        bottom_sum = 0
        card_numbers_bottom = []
        for card in self.cards :
            top = card.top_number
            bottom = card.bottom_number
            if not self.cards.index(card) == 0 :
                # 前
                pre_card = self.cards[self.cards.index(card)-1]
                # 同数だったら2倍
                if pre_card.top_number == card.top_number :
                    top = top*2
                if pre_card.bottom_number == card.bottom_number :
                    bottom = bottom*2
                # 階段だったら1.5倍
                if pre_card.top_number + 1 == card.top_number or pre_card.top_number - 1 == card.top_number :
                    top = top*1.5
                if pre_card.bottom_number + 1 == card.bottom_number or pre_card.bottom_number - 1 == card.bottom_number:
                    bottom = bottom*1.5
            if not self.cards.index(card) == len(self.cards)-1 :
                # 後
                post_card = self.cards[self.cards.index(card)+1]
                # 同数だったら2倍
                if post_card.top_number == card.top_number :
                    top = top*2
                if post_card.bottom_number == card.bottom_number :
                    bottom = bottom*2
                # 階段だったら1.5倍
                if post_card.top_number + 1 == card.top_number or post_card.top_number - 1 == card.top_number :
                    top = top*1.5
                if post_card.bottom_number + 1 == card.bottom_number or post_card.bottom_number - 1 == card.bottom_number:
                    bottom = bottom*1.5
            top_sum += top
            bottom_sum += bottom

        if top_sum >= bottom_sum :
            pass
        else :
            for card in self.cards :
                tmp = card.top_number
                card.top_number = card.bottom_number
                card.bottom_number = tmp