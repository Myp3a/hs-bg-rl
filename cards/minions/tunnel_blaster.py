from __future__ import annotations
from typing import TYPE_CHECKING

from cards.minion import Minion, MinionClass
from cards.minions.game_entity import GameEntity

if TYPE_CHECKING:
    from models.army import Army


class TunnelBlaster(Minion):
    def __init__(self, army: Army) -> None:
        super().__init__(army)
        self.minion_id = 135
        self.classes = []
        self.level = 4
        self.base_attack_value = 3
        self.base_health_value = 7
        self.taunt = True
        self.friendly_army = None
        self.hooks["deathrattle"].append(self.damage_on_death)
        self.hooks["on_fight_start"].append(self.set_friendly_army)

    def set_friendly_army(self):
        self.friendly_army = self.army

    def damage_all(self):
        targets = [t for t in self.friendly_army.cards + self.enemy_army.cards]
        for t in targets:
            tnt = GameEntity(self.friendly_army)
            tnt.base_attack_value = 3
            tnt.attack(t)

    def damage_on_death(self, position):
        if self.triplet:
            self.damage_all()
        self.damage_all()