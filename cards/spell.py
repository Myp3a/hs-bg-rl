from __future__ import annotations
from typing import TYPE_CHECKING

from models.card import Card

if TYPE_CHECKING:
    from cards.minion import Minion
    from models.player import Player


class Spell(Card):
    def __init__(self, player, triplet=False) -> None:
        super().__init__()
        self.player: Player = player
        self.level = 0
        self.spellcraft = False
        self.triplet = triplet

    def play(self, target: None) -> None:
        raise NotImplementedError
    
class TargetedSpell(Spell):
    def __init__(self, player, triplet=False) -> None:
        super().__init__(player, triplet)

    def play(self, target: Minion) -> None:
        raise NotImplementedError