from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.minions.game_entity import GameEntity

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
        self.hooks["deathrattle"].append(self.damage_enemies)

    def damage_enemies(self, position):
        if self.triplet:
            damage = 8
        else:
            damage = 4
        for _ in range(2):
            targets: list[Minion] = sorted(self.enemy_army.cards, key=lambda targ: targ.health_value)
            if not targets:
                self.log.debug(f"{self} found no targets")
                return
            laser = GameEntity(self.army)
            laser.base_attack_value = damage
            self.log.debug(f"{self} attacking {targets[0]}")
            laser.attack(targets[0])
