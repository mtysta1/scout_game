import random

class Dealer():

    def __init__(self):
        self.cards = []  # 配るカード
        self.players = []  # 配る相手

    def dealCards(self):
        '''カードを配る'''

        # カードをシャッフルする
        random.shuffle(self.cards)

        player_num = len(self.players)

        i = 0

        while self.cards:
            player = self.players[i % player_num]

            # 先頭のカードを取り出し、そのカードをプレイヤーの手札に加えてもらう
            card = self.cards.pop(0)
            if random.random() >= 0.5:
                player.addCard(card)
            else:
                tmp = card.top_number
                card.top_number = card.bottom_number
                card.bottom_number = tmp
                player.addCard(card)

            i += 1
