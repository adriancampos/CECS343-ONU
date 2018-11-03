class Card:
    curID = 0
    def __init__(self):
        self.id = Card.curID
        Card.curID += 1

a = Card()
b = Card()
print(a.id)
print(b.id)
