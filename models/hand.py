from .cardset import CardSet


class Hand(CardSet):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.max_len = 10