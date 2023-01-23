from ui import UI

class Field():

    def __init__(self):
        self.cards = []  # 場札
        self.state = "blank" # 場の状態 ["blank", "single", "multi_same", "multi_steps"]
        self.owner = None
        self.ui = UI()