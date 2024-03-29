from cards.minion import Minion
from cards.spell import Spell
from .cardset import CardSet


class Hand(CardSet):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.max_len = 10
        self.hooks = {
            "on_turn_start": [self.reset_summons],  # (self)
            "on_turn_end": [self.remove_spellcraft],  # (self)
        }

    def reset_summons(self) -> None:
        for c in self.cards:
            if isinstance(c, Minion):
                c.reset_turn_start()
                c.clean_overrides()
                if c.summoned:
                    c.summoned = False
    
    def remove_spellcraft(self):
        for c in list(self.cards):
            if isinstance(c, Spell):
                if c.spellcraft:
                    self.cards.remove(c)
