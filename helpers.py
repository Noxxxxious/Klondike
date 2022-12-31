def number_to_rank(number):
    if 1 < number < 11:
        return str(number)
    if number == 1:
        return "ace"
    if number == 11:
        return "jack"
    if number == 12:
        return "queen"
    if number == 13:
        return "king"
    return "unidentified card"


def suit_to_color(suit):
    if suit in ("clubs", "spades"):
        return "black"
    if suit in ("hearts", "diamonds"):
        return "red"
    return "unknown"



