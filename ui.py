

class UI():

    def showMessage(self, message, end='\n') :
        '''メッセージ出力'''

        print(message,end=end)

    def showErrorMessage(self, message) :
        '''エラーメッセージ出力'''

        print("エラー："+message)

    def playError(self,sent) :
        '''プレイのエラー'''

        self.showErrorMessage("場にカードを出せません！"+sent)

    def showCards(self, cards, name):
        '''カード配列（選択前）を表示する'''

        # Cardオブジェクトのリストを文字列に変換して表示
        if len(cards) == 0 :
            self.showMessage("カードがありません")
        else :
            cards_str = ""
            i = 1
            for card in cards:
                cards_str += str(i) + self.getCardStr(card)
                i+=1

            self.showMessage(name + "のカード：" + cards_str)

    def showCardsTop(self, cards, name):
        '''カード配列（選択後）を表示する'''

        # Cardオブジェクトのリストを文字列に変換して表示
        if len(cards) == 0 :
            self.showMessage("カードがありません")
        else :
            cards_str = ""
            i = 1
            for card in cards:
                cards_str += str(i) + self.getCardsTopStr(card.top_number)
                i+=1

            self.showMessage(name + "のカード：" + cards_str)

    def showPlayerInfo(self, player) :
        '''プレーヤーの情報を表示する'''

        self.showMessage(player.name+" ショーポイント:"+str(player.showpoint)+" スカウトポイント:"+str(player.scoutpoint)+" 手札枚数："+str(len(player.cards)))

    def showField(self, field) :
        '''場の情報を表示する'''

        if field.state == "blank" :
            cards_str = "なし"
        else :
            cards_str = ""
            i = 0
            for card in field.cards:
                i += 1
                cards_str += str(i) + self.getCardStr(card)

        self.showMessage("場札:"+cards_str)

    def showRoundResult(self, players, round_count):
        '''ゲームの結果を表示する'''

        self.showMessage("\nラウンド"+str(round_count)+"結果")
        for player in players :
            self.showMessage(player.name + " : ",end='')
            for i in range(len(player.point)) :
                if player.point[i] < 10 :
                    self.showMessage(str(player.point[i])+"点,  ",end='')
                else :
                    self.showMessage(str(player.point[i])+"点, ",end='')
            self.showMessage("計"+str(player.totalpoint)+"点")

    def showResult(self, players):
        '''ゲームの結果を表示する'''

        self.showMessage("\n最終結果")
        i = 0
        for player in players :
            i += 1
            if player.totalpoint < 10 :
                point_str = "0" + str(player.totalpoint)
            else :
                point_str = str(player.totalpoint)
            self.showMessage(str(i) + "位:" + player.name + "(" + point_str + "点)")

    def getCardStr(self, card):
        '''Cardオブジェクトを文字列に変換'''

        return "[" + str(card.top_number) + ":" + str(card.bottom_number) + "]"

    def getCardsTopStr(self, number):
        '''Cardオブジェクト（選択後）を文字列に変換'''

        return "[" + str(number) + "]"

    def getNumberOfPlayers(self):
        '''プレイヤー人数の設定'''
        while True :
            val = input("プレイヤー人数（3-5）->")
            try:
                num_players = int(val, 10)  # 試しにint関数で文字列を変換
                if num_players > 2 and num_players < 6 :
                    return num_players
                else:
                    self.showErrorMessage("プレイヤー人数は3-5で入力してください")
            except ValueError:
                self.showErrorMessage("プレイヤー人数は3-5の整数で入力してください")

    def getNumberOfCPU(self, num_players):
        '''プレイヤー人数の設定'''
        while True :
            val = input("CPU人数->")
            try:
                num_cpus = int(val, 10)  # 試しにint関数で文字列を変換
                if num_cpus > num_players:
                    self.showErrorMessage("CPU人数がプレイヤー人数より多いです")
                else:
                    return num_cpus
            except ValueError:
                self.showErrorMessage("CPU人数は整数で入力してください")

    def getPlayerAction(self, player):
        '''プレイヤーアクションの入力'''

        while True :
            val = input("アクションを選択してください（A:Show B:Scout C:Scout&Show!）->")

            if val == "A" or val == "a" or val == "show" or val == "ショー" or val == "しょー" :
                return "A"
            elif val == "B" or val == "b" or val == "scout" or val == "スカウト" or val == "すかうと" :
                return "B"
            elif val == "C" or val == "c" or val == "scout&show" or val == "スカウトアンドショー" or val == "すかうとあんどしょー" :
                return "C"
            else :
                self.showErrorMessage("正しく入力してください")

    def showPlayerAction(self, player, action, cards):
        '''プレイヤーアクションの出力'''

        if action == "show" :
            action = "ショー"
        elif action == "scout" :
            action = "スカウト"
        cards_str = ""
        for card in cards:
            cards_str += self.getCardStr(card)
        self.showMessage(player.name+"は"+cards_str+"を"+action+"しました。")
        self.showPlayerInfo(player)

    def getShowCards(self,player):
        '''プレイヤー（人間）がショーするカードを取得'''

        self.showCards(player.cards, player.name)

        while True :
            val = input("ショーするカードを選択してください（単出し：[index] 複数出し：[start_index end_index] キャンセル：C）->")
            if val == "C" or val == "c" or val == "cancel" or val == "キャンセル" or val == "きゃんせる" :
                return []
            try :
                vals =  [int(s, 10)  for s in val.split()]
                vals.sort()
            except ValueError:
                self.showErrorMessage("正しく入力してください")
                continue
            if len(vals) > 2 :
                self.showErrorMessage("正しく入力してください")
                continue
            choise_nums = []
            error = False
            if len(vals) == 1 :
                choise_num = vals[0] - 1
                if choise_num >= 0 and choise_num < len(player.cards) :
                    choise_nums.append(choise_num)
                    return choise_nums
                else:
                    self.showErrorMessage("正しく入力してください")
            else :
                for val in range(vals[0],vals[1]+1) :
                    choise_num = val - 1
                    if choise_num >= 0 and choise_num < len(player.cards) :
                        choise_nums.append(choise_num)
                    else:
                        error = True
                if error :
                    self.showErrorMessage("正しく入力してください")
                else :
                    return choise_nums

    def getScoutCards(self,field):
        '''プレイヤー（人間）がスカウトするカードを取得'''

        while True :
            val = input("スカウトするカードを選択してください（スカウトカード指定：[index] [向き A:順 B:逆] キャンセル：C）->")
            if val == "C" or val == "c" or val == "cancel" or val == "キャンセル" or val == "きゃんせる" :
                return None
            vals =  val.split()
            if len(vals) != 2 :
                self.showErrorMessage("正しく入力してください")
                continue
            try:
                choise_num = int(vals[0], 10) -1
                if choise_num >= 0 and choise_num < len(field.cards) :
                    pass
                else:
                    self.showErrorMessage("正しく入力してください")
                if vals[1] == "A" or vals[1] == "a" :
                    return choise_num, "A"
                elif vals[1] == "B" or vals[1] == "b" :
                    return choise_num, "B"
                else :
                    self.showErrorMessage("正しく入力してください")
            except ValueError:
                self.showErrorMessage("正しく入力してください")

    def getScoutIndex(self,player):
        '''プレイヤー（人間）がスカウトするカードの位置を取得'''

        self.showCards(player.cards, player.name)

        while True :
            val = input("スカウトする手札位置を選択してください（スカウト位置指定：[index]）->")
            try:
                index = int(val, 10) - 1
                if index >= 0 and index <= len(player.cards) :
                    return index
                else :
                    self.showErrorMessage("正しく入力してください")
            except ValueError:
                self.showErrorMessage("正しく入力してください")

    def getAboveOrBelow(self, player) :
        cards_str = ""
        i = 1
        for card in player.cards:
            cards_str += str(i) + self.getCardsTopStr(card.top_number)
            i+=1

        self.showMessage(player.name + "のカード（A:上）：" + cards_str)
        cards_str = ""
        i = 1
        for card in player.cards:
            cards_str += str(i) + self.getCardsTopStr(card.bottom_number)
            i+=1

        self.showMessage(player.name + "のカード（B:下）：" + cards_str)

        while True :
            val = input("1:上 2:下 を選択してください->")

            if val == "A" or val == "a" or val == "top" or val == "上" or val == "うえ" :
                self.showMessage("上が選択されました")
                return "top"
            elif val == "B" or val == "b" or val == "bottom" or val == "下" or val == "した" :
                self.showMessage("下が選択されました")
                return "bottom"
            else :
                self.showErrorMessage("正しく入力してください")


