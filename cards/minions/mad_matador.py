from __future__ import annotations
import random
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class MadMatador(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 159
        self.classes = []
        self.level = 5
        self.base_attack_value = 0
        self.base_health_value = 8
        self.base_taunt = True
        self.redirects_left = 0
        self.hooks["on_defence_pre"].append(self.redirect_attack)
        self.hooks["on_turn_start"].append(self.reset_redirects)
        self.hooks["on_play"].append(self.reset_redirects)

    def reset_redirects(self):
        if self.triplet:
            self.redirects_left = 2
        else:
            self.redirects_left = 1

    def redirect_attack(self, attacker: Minion) -> None:
        if self.redirects_left > 0:
            self.redirects_left -= 1
            target = random.choice(self.enemy_army.cards)
            self.log.debug(f"{self} redirecting {attacker} to {target}")
            attacker.attack(target)
            return True  # Prevent existing attack
