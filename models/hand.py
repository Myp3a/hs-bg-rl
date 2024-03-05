from cards.minion import Minion
from .cardset import CardSet


class Hand(CardSet):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.max_len = 10
        self.hooks = {
            "on_turn_start": [self.reset_summons],  # (self)
        }

    def reset_summons(self) -> None:
        for c in self.cards:
            if isinstance(c, Minion):
                if c.summoned:
                    c.summoned = False
                    c.attack_temp_boost = 0
                    c.health_temp_boost = 0