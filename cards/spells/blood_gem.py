from __future__ import annotations
from typing import TYPE_CHECKING

from cards.spell import TargetedSpell

if TYPE_CHECKING:
    from models.player import Player
    from cards.minion import Minion

class BloodGem(TargetedSpell):
    def __init__(self, player) -> None:
        super().__init__(player)
        self.spell_id = 0

    def play(self, target: Minion) -> None:
        target.attack_value += self.player.blood_gem_attack
        target.health_value += self.player.blood_gem_health