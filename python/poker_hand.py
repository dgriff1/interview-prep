

import functools

# Write some code that will evaluate a set of cards and determine the best possible poker hand.

class Card:
  HEARTS = "hearts"
  SPADES = "spades"
  DIAMONDS = "diamonds"
  CLUBS = "clubs"

  ACE = "a"
  KING = "k"
  QUEEN = "q"
  JACK = "j"
  def __init__(self, suit, rank):
    self.suit = suit
    self.rank = rank

  def suit_rank(self):
    if isinstance(self.rank, int):
      return self.rank
    elif self.rank == Card.ACE:
      return 14
    elif self.rank == Card.KING:
      return 13
    elif self.rank == Card.QUEEN:
      return 12
    elif self.rank == Card.JACK:
      return 11
  def __repr__(self):
    return "Suit " + str(self.suit) + " Rank " + str(self.rank)


def same_suit(hand):
  for h in hand:
    if h.suit != hand[0].suit:
      return False
  return True

def sequential(hand):
  for idx, h in enumerate(hand[:-1]):
    if h.suit_rank() - hand[idx + 1].suit_rank() != 1:
      return False
  return True


def highest_card(v, hand):
  return hand[0].rank == v

def royal_flush(hand):
  if same_suit(hand) and sequential(hand) and highest_card(Card.ACE, hand):
    return "Royal Flush"
  else:
    return None

def straight_flush(hand):
  if same_suit(hand) and sequential(hand):
    return "Straight Flush"
  else:
    return None


def create_ranks(hand):
  ranks = {}
  for h in hand:
    if h.rank in ranks:
      ranks[h.rank] = ranks[h.rank] + 1
    else:
      ranks[h.rank] = 1
  return ranks

def of_a_kind(count, hand):
  ranks = create_ranks(hand)
  for k,v in ranks.items():
    if v == count:
      return str(count) + " of a Kind"

def full_house(hand):
  if of_a_kind(3, hand) and of_a_kind(2, hand):
    return "Full House"

def flush(hand):
  if same_suit(hand):
    return "Flush"

def straight(hand):
  if sequential(hand):
    return "Straight"

def two_pair(hand):
  pairs = []
  ranks = create_ranks(hand)
  for k,v in ranks.items():
    if v == 2:
      pairs.append(k)
  if len(pairs) == 2:
    return "Two Pair"



def high_card(hand):
  return str(hand[0])

evaluators = [royal_flush,
              straight_flush,
              functools.partial(of_a_kind,4),
              full_house,
              flush,
              straight,
              functools.partial(of_a_kind,3),
              two_pair,
              functools.partial(of_a_kind,2),
              high_card
              ]

def evaluate_hand(hand):
  for e in evaluators:
    ret = e(hand)
    if ret != None:
      return ret


assert(evaluate_hand([ Card(Card.HEARTS, Card.ACE),
                       Card(Card.HEARTS, Card.KING),
                       Card(Card.HEARTS, Card.QUEEN),
                       Card(Card.HEARTS, Card.JACK),
                       Card(Card.HEARTS, 10) ]) == "Royal Flush")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.HEARTS, 9),
                       Card(Card.HEARTS, 8),
                       Card(Card.HEARTS, 7),
                       Card(Card.HEARTS, 6) ]) == "Straight Flush")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.SPADES, 10),
                       Card(Card.CLUBS, 10),
                       Card(Card.DIAMONDS, 10),
                       Card(Card.HEARTS, 6) ]) == "4 of a Kind")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.SPADES, 10),
                       Card(Card.CLUBS, 10),
                       Card(Card.DIAMONDS, Card.ACE),
                       Card(Card.HEARTS, 6) ]) == "3 of a Kind")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.SPADES, 10),
                       Card(Card.CLUBS, 10),
                       Card(Card.DIAMONDS, 6),
                       Card(Card.HEARTS, 6) ]) == "Full House")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.HEARTS, 9),
                       Card(Card.HEARTS, 8),
                       Card(Card.HEARTS, 2),
                       Card(Card.HEARTS, 6) ]) == "Flush")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.DIAMONDS, 9),
                       Card(Card.HEARTS, 8),
                       Card(Card.SPADES, 7),
                       Card(Card.HEARTS, 6) ]) == "Straight")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.DIAMONDS, 10),
                       Card(Card.HEARTS, 8),
                       Card(Card.SPADES, 8),
                       Card(Card.HEARTS, 6) ]) == "Two Pair")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.DIAMONDS, 10),
                       Card(Card.HEARTS, 7),
                       Card(Card.SPADES, 8),
                       Card(Card.HEARTS, 6) ]) == "2 of a Kind")
assert(evaluate_hand([ Card(Card.HEARTS, 10),
                       Card(Card.DIAMONDS, 4),
                       Card(Card.HEARTS, 7),
                       Card(Card.SPADES, 8),
                       Card(Card.HEARTS, 6) ]) == "Suit hearts Rank 10")

print("Works as Intended")
