
class Card:
    def __init__(self, rank, color):
        self.rank = rank
        self.color = color

    def __str__(self):
        return "<Card rank={0}, color={1}>".format(self.rank, self.color)

    def clickEvent(self):
        print("Card clicked: {0}".format(self))

c = Card(4,4)
c.clickEvent()