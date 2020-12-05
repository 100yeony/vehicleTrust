import collections
from pprint import pprint
from random import choice

class FrenchDeck:
  ranks = [str(n) for n in range(2, 11)] + list('JQKA')  # (2)
  suits = 'spades diamonds clubs hearts'.split()         # (3)

  def __init__(self):
    self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks] # (4)

  def __len__(self):
    return len(self._cards)                              # (5)

  def __getitem__(self, position):
    return self._cards[position]


Card = collections.namedtuple('Card', ['rank', 'suit'])  # (1)

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    print(rank_value)
    return rank_value * len(suit_values) + suit_values[card.suit]

# https://www.python2.net/questions-298273.htm

deck = FrenchDeck()
# print(deck.ranks)
# print(deck.__len__())
#
# print(deck[1])
# print(choice(deck))

# deck[1].rank = 3
# print(deck[1])

for card in sorted(deck, key=spades_high):
    print(card)
#
# print(deck[:3])
# print(deck[12::13])




# len(deck)
# print(deck)
# print(Card)
# deck.__len__()

# deck[0]
# deck[-1]
# choice(deck)



#
#
# class Position:
#     def __init__(self):
#         self.x = 0
#         self.y = 0
#
# class Player:
#     def __init__(self, x, y):
#         self.__position = Position()
#         self.__position.x = x
#         self.__position.y = y
#
#     @property
#     def position(self):
#         return self.__position
#
#     @position.setter
#     def position(self, value):
#         print('Position changed')
#         self.__position = value
#
#     # def printData(self):
#     #     temp = dict({
#     #         'x' : __position.x,
#     #         'y' : __position.y
#     #     })
#     #     return pprint(temp, width=20, indent=2)
#
# player = Player(5, 10)
# player.position = Position() # Setter gets called
# player.position.x = 10 # Setter doesn't get called
#
# # player.printData()
