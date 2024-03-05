from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass

if TYPE_CHECKING:
    from models.army import Army


class LighterFighter(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 111
        self.classes = [MinionClass.Mech]
        self.level = 4
        self.base_attack_value = 4
        self.base_health_value = 1
        self.enemy_army = None
        self.hooks["on_defence_pre"].append(self.put_army)
        self.hooks["deathrattle"].append(self.damage_enemies)

    def put_army(self, attacker):
        self.enemy_army = attacker.army

    def damage_enemies(self, position):
        if self.triplet:
            damage = 8
        else:
            damage = 4
        for _ in range(2):
            targets: list[Minion] = sorted(self.enemy_army.cards, key=lambda targ: targ.health_value)
            if len(targets) == 0:
                return
            targets[0].health_temp_boost -= damage
